#!/usr/bin/env python3
"""Verify Crowquill Mono: .kw glyphs present + real HarfBuzz shaping of keywords."""
from pathlib import Path
from fontTools.ttLib import TTFont
import uharfbuzz as hb

ROOT = Path(__file__).resolve().parent.parent
TTF = ROOT / "dist" / "CrowquillMono-Regular.ttf"

font = TTFont(TTF)
order = font.getGlyphOrder()
kw_glyphs = [g for g in order if g.endswith(".kw")]
print(f"glyphs total: {len(order)}")
print(f".kw glyphs:   {len(kw_glyphs)}  e.g. {kw_glyphs[:8]}")

blob = hb.Blob.from_file_path(str(TTF))
face = hb.Face(blob)
hbfont = hb.Font(face)


def shaped_names(text: str) -> list[str]:
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    # calt is on by default; keep liga/calt explicitly on
    hb.shape(hbfont, buf, {"calt": True, "liga": True})
    return [font.getGlyphName(i.codepoint) for i in buf.glyph_infos]


def kw_count(text: str) -> int:
    return sum(1 for n in shaped_names(text) if n.endswith(".kw"))


cases = [
    # (text, how many chars should be bold, why)
    ("const",        5, "keyword sozinha -> tudo bold"),
    ("const x = 1",  5, "keyword + codigo -> so a keyword"),
    ("myconst",      0, "keyword como sufixo -> nada bold"),
    ("constante",    0, "keyword como prefixo -> nada bold"),
    ("const_val",    0, "colada em _ -> nada bold"),
    ("return foo",   6, "return sozinho -> 6 bold (r,e,t,u,r,n)"),
    ("returned",     0, "return dentro de palavra -> nada"),
    ("if (x) {}",    2, "if sozinho -> 2 bold"),
    ("iffy",         0, "if como prefixo -> nada"),
    ("None",         4, "Python True/False/None capitalizado"),
    ("none",         0, "minusculo nao e keyword Python"),
    ("async await",  10, "duas keywords -> 5+5 bold"),
]

print("\n== shaping ==")
ok = True
for text, expected, why in cases:
    got = kw_count(text)
    mark = "OK " if got == expected else "XX "
    if got != expected:
        ok = False
    print(f"  {mark} {got}=={expected}  {text!r:20} {why}")

# ligature preserved? '->' should form one glyph (fewer glyphs than chars)
lig = shaped_names("a -> b")
print(f"\nligadura '->' : {lig}  (esperado: contem um glifo de seta, < 6 glifos)")

print("\nRESULTADO:", "TUDO OK" if ok else "FALHOU")
