#!/usr/bin/env python3
"""
Crowquill Mono — build engine.

Base: a custom Iosevka build (see iosevka/private-build-plans.toml).
Signature feature: language keywords render BOLD automatically, via an
OpenType `calt` (contextual alternates) feature with word-boundary guards.
The base font's native code ligatures are PRESERVED (GSUB lookups are merged,
not replaced).

The font cannot know the language semantically — it matches exact character
sequences. Word-boundary guards (ignore rules on identifier characters) prevent
false positives like `const` inside `constante` or `myconst`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeatures
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import DecomposingRecordingPen

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
BUILD = ROOT / "build"
DIST = ROOT / "dist"

FAMILY = "Crowquill Mono"
PS_FAMILY = "CrowquillMono"
VERSION = "0.4.0"

BASE_TTF = SRC / "jbmono" / "fonts" / "ttf" / "JetBrainsMono-Regular.ttf"
BOLD_TTF = SRC / "jbmono" / "fonts" / "ttf" / "JetBrainsMono-Bold.ttf"
KEYWORDS_JSON = SRC / "keywords.json"

# Fallback keyword set if keywords.json isn't present yet.
FALLBACK_KEYWORDS = [
    "const", "let", "var", "function", "return", "if", "else", "for", "while",
    "do", "switch", "case", "default", "break", "continue", "class", "new",
    "import", "export", "from", "async", "await", "yield", "try", "catch",
    "finally", "throw", "typeof", "instanceof", "in", "of", "delete", "void",
    "this", "super", "extends", "static", "get", "set", "def", "elif", "lambda",
    "pass", "raise", "with", "as", "and", "or", "not", "is", "None", "True",
    "False", "func", "fn", "impl", "trait", "struct", "enum", "match", "mut",
    "pub", "use", "mod", "where", "type", "interface", "public", "private",
    "protected", "namespace", "using", "nil", "end", "module", "defmodule",
    "defp", "when", "cond", "unless", "begin", "rescue", "ensure", "select",
    "insert", "update", "goto",
]


def load_keywords() -> list[str]:
    if KEYWORDS_JSON.exists():
        data = json.loads(KEYWORDS_JSON.read_text())
        master = data.get("master")
        if master:
            print(f"  keywords.json: {len(master)} palavras")
            return sorted(set(master), key=lambda w: (-len(w), w))
    print("  keywords.json ausente — usando fallback embutido")
    return sorted(set(FALLBACK_KEYWORDS), key=lambda w: (-len(w), w))


def char_to_glyph_map(font: TTFont) -> dict[str, str]:
    cmap = font.getBestCmap()
    return {chr(cp): name for cp, name in cmap.items()}


def add_bold_variants(base: TTFont, bold: TTFont, needed_chars: set[str]) -> dict[str, str]:
    """Copy bold outlines for each needed letter into base as `<glyph>.kw`.

    Returns a map char -> kw-glyph-name. Advance widths are copied verbatim
    (both faces are 600u monospace, so no scaling is required).
    """
    base_cmap = char_to_glyph_map(base)
    bold_cmap = char_to_glyph_map(bold)
    bold_gs = bold.getGlyphSet()

    glyf = base["glyf"]
    hmtx = base["hmtx"]
    order = base.getGlyphOrder()

    ch_to_kw: dict[str, str] = {}
    for ch in sorted(needed_chars):
        if ch not in base_cmap or ch not in bold_cmap:
            continue
        bname = bold_cmap[ch]
        kwname = f"{base_cmap[ch]}.kw"
        if kwname in glyf.glyphs:
            ch_to_kw[ch] = kwname
            continue
        # Decompose (flatten components) then re-record into a fresh TT glyph.
        rec = DecomposingRecordingPen(bold_gs)
        bold_gs[bname].draw(rec)
        pen = TTGlyphPen(None)
        rec.replay(pen)
        glyf.glyphs[kwname] = pen.glyph()
        hmtx.metrics[kwname] = bold["hmtx"].metrics[bname]
        order.append(kwname)
        ch_to_kw[ch] = kwname
    base.setGlyphOrder(order)
    glyf.glyphOrder = order  # keep glyf table's own order in sync
    return ch_to_kw


def build_feature(base: TTFont, keywords: list[str], ch_to_kw: dict[str, str]) -> tuple[str, int]:
    """Return (FEA text, kept-keyword-count)."""
    base_cmap = char_to_glyph_map(base)

    # identifier characters: letters + digits + underscore that exist in the font
    ident_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
    word_glyphs = sorted({base_cmap[c] for c in ident_chars if c in base_cmap})
    # the bold variants are also identifier-like: guard against double matches
    word_glyphs += sorted(set(ch_to_kw.values()))

    lines: list[str] = []
    lines.append("@word = [" + " ".join(word_glyphs) + "];")
    lines.append("")

    # One single-substitution lookup per glyph (base -> bold .kw). These are
    # standalone: they only fire when invoked inline from the contextual rules,
    # so plain letters elsewhere stay regular.
    per_glyph_lookup: dict[str, str] = {}
    for ch, kwname in sorted(ch_to_kw.items()):
        gname = base_cmap[ch]
        lk = f"KW_{gname}"
        if lk in per_glyph_lookup.values():
            continue
        per_glyph_lookup[ch] = lk
        lines.append(f"lookup {lk} {{ sub {gname} by {kwname}; }} {lk};")
    lines.append("")

    lines.append("feature calt {")
    kept = 0
    for kw in keywords:
        if any(c not in base_cmap or c not in ch_to_kw for c in kw):
            continue
        base_seq = [base_cmap[c] for c in kw]
        marked = " ".join(f"{g}'" for g in base_seq)
        sub_inline = " ".join(f"{base_cmap[c]}' lookup {per_glyph_lookup[c]}" for c in kw)
        tag = "kw_" + "".join(f"{ord(c):x}" for c in kw)
        lines.append(f"  lookup {tag} {{")
        lines.append(f"    ignore sub @word {marked};")
        lines.append(f"    ignore sub {marked} @word;")
        lines.append(f"    sub {sub_inline};")
        lines.append(f"  }} {tag};")
        kept += 1

    lines.append("} calt;")
    return "\n".join(lines) + "\n", kept


def _remap_lookup_refs(lookup, offset: int) -> None:
    """Offset every child-lookup reference inside a GSUB lookup."""
    for st in lookup.SubTable:
        # Extension wrapper (LookupType 7)
        ext = getattr(st, "ExtSubTable", None)
        target = ext if ext is not None else st
        recs = getattr(target, "SubstLookupRecord", None)
        if recs:
            for r in recs:
                r.LookupListIndex += offset


def merge_gsub(dst: TTFont, src: TTFont) -> None:
    """Append src GSUB lookups into dst and wire src `calt` lookups into dst `calt`."""
    d = dst["GSUB"].table
    s = src["GSUB"].table
    offset = d.LookupList.LookupCount

    for lk in s.LookupList.Lookup:
        _remap_lookup_refs(lk, offset)
        d.LookupList.Lookup.append(lk)
    d.LookupList.LookupCount = len(d.LookupList.Lookup)

    src_calt: list[int] = []
    for fr in s.FeatureList.FeatureRecord:
        if fr.FeatureTag == "calt":
            src_calt.extend(i + offset for i in fr.Feature.LookupListIndex)

    wired = False
    for fr in d.FeatureList.FeatureRecord:
        if fr.FeatureTag == "calt":
            fr.Feature.LookupListIndex.extend(src_calt)
            fr.Feature.LookupCount = len(fr.Feature.LookupListIndex)
            wired = True
    if not wired:
        raise RuntimeError("base GSUB has no calt feature to wire into")


def rename(base: TTFont, style: str, is_bold: bool, is_italic: bool) -> None:
    name = base["name"]
    ps = f"{PS_FAMILY}-{style.replace(' ', '')}"
    full = f"{FAMILY} {style}" if style != "Regular" else FAMILY
    values = {
        1: FAMILY, 2: style,  # RIBBI subfamily: Regular/Bold/Italic/Bold Italic
        3: f"{ps};{VERSION}", 4: full, 6: ps,
        16: FAMILY, 17: style,
    }
    for nid, val in values.items():
        name.setName(val, nid, 3, 1, 0x409)
        name.setName(val, nid, 1, 0, 0)

    os2 = base["OS/2"]
    head = base["head"]
    os2.usWeightClass = 700 if is_bold else 400
    sel = os2.fsSelection & ~(0x01 | 0x20 | 0x40)  # clear ITALIC, BOLD, REGULAR
    mac = head.macStyle & ~0x3                      # clear bold+italic mac bits
    if is_bold:
        sel |= 0x20; mac |= 0x1
    if is_italic:
        sel |= 0x01; mac |= 0x2
    if not is_bold and not is_italic:
        sel |= 0x40                                 # REGULAR
    os2.fsSelection = sel
    head.macStyle = mac


def build_face(base_ttf: Path, kw_ttf: Path, keywords: list[str],
               style: str, is_bold: bool, is_italic: bool = False) -> Path:
    print(f"\n[{FAMILY} {style}]  base={base_ttf.name}  keyword-source={kw_ttf.name}")
    base = TTFont(base_ttf)
    kwfont = TTFont(kw_ttf)

    needed = {c for kw in keywords for c in kw}
    ch_to_kw = add_bold_variants(base, kwfont, needed)
    print(f"  variantes .kw criadas: {len(ch_to_kw)}")

    fea, kept = build_feature(base, keywords, ch_to_kw)
    fea_path = BUILD / f"keywords-{style.lower()}.fea"
    fea_path.write_text(fea)
    print(f"  keywords cobertas: {kept}")

    stash = base["GSUB"]
    del base["GSUB"]
    addOpenTypeFeatures(base, str(fea_path))
    mine = base["GSUB"]
    base["GSUB"] = stash          # restore native ligatures
    holder = TTFont()
    holder["GSUB"] = mine
    merge_gsub(base, holder)      # append keyword lookups, wire into calt

    rename(base, style, is_bold, is_italic)

    out = DIST / f"{PS_FAMILY}-{style.replace(' ', '')}.ttf"
    base.save(out)
    print(f"  salvo: {out.relative_to(ROOT)}")
    return out


def main() -> int:
    BUILD.mkdir(exist_ok=True)
    DIST.mkdir(exist_ok=True)

    ttf_dir = SRC / "iosevka"   # build custom do Iosevka (Curly + manuscrito)
    reg = ttf_dir / "Crowquill-Regular.ttf"
    bold = ttf_dir / "Crowquill-Bold.ttf"
    heavy = ttf_dir / "Crowquill-Heavy.ttf"
    ital = ttf_dir / "Crowquill-Italic.ttf"
    bital = ttf_dir / "Crowquill-BoldItalic.ttf"
    hital = ttf_dir / "Crowquill-HeavyItalic.ttf"
    for f in (reg, bold, heavy, ital, bital, hital):
        if not f.exists():
            print(f"ERRO: fonte-fonte ausente: {f}", file=sys.stderr)
            return 1

    keywords = load_keywords()
    print(f"Crowquill Mono {VERSION} — build ({len(keywords)} keywords)")

    # Keyword-bold vem do Heavy (900) -> keyword salta forte contra o corpo.
    build_face(reg, heavy, keywords, "Regular", is_bold=False)
    build_face(bold, heavy, keywords, "Bold", is_bold=True)
    build_face(ital, hital, keywords, "Italic", is_bold=False, is_italic=True)
    build_face(bital, hital, keywords, "Bold Italic", is_bold=True, is_italic=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
