#!/usr/bin/env python3
"""Render a colored specimen PNG of Crowquill Mono using real HarfBuzz shaping.

Monospace => fixed advance per cell, so tokens are placed by column. Keyword
tokens are drawn in isolation, which lets the font's own `calt` bold them
(.kw glyphs). Colors come from the Crowquill dark theme palette.
"""
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "dist" / "CrowquillMono-Regular.ttf"
BOLD = ROOT / "dist" / "CrowquillMono-Bold.ttf"
OUT = ROOT / "dist" / "specimen.png"

# theme palette
BG = "#1B1E2B"; FG = "#E4E6F1"; KW = "#FF6B9D"; STR = "#A5E075"
NUM = "#F5A25C"; COM = "#6C7392"; FUNC = "#6BC1FF"; TYPE = "#FFD166"; ACC = "#C792EA"

MASTER = set(json.loads((ROOT / "sources" / "keywords.json").read_text())["master"])

SIZE = 34
CELL = SIZE * 0.6              # JB Mono advance = 600/1000 em
LINE = int(SIZE * 1.55)
MARGIN = 40

lines = [
    ("c", "// Crowquill Mono — keywords ficam bold sozinhas"),
    ("", ""),
    ("py", "def fibonacci(n):"),
    ("py", "    if n <= 1:"),
    ("py", "        return n"),
    ("py", "    return fibonacci(n - 1) + fibonacci(n - 2)"),
    ("", ""),
    ("ts", 'const greet = async (name: string): Promise<void> => {'),
    ("ts", '    await log(`ola ${name}`)   // => -> != >= <= === |>'),
    ("ts", "}"),
    ("", ""),
    ("rs", "pub fn main() {"),
    ("rs", '    let mut xs = vec![1, 2, 3];'),
    ("rs", "    for x in xs.iter() { match x { _ => println(x) } }"),
    ("rs", "}"),
    ("", ""),
    ("c", "// fronteira: nada disso bolda ->"),
    ("id", "constante  myconst  returned  iffy  none"),
]

STR_RE = re.compile(r'"[^"]*"|\'[^\']*\'|`[^`]*`')
NUM_RE = re.compile(r'\b\d+\b')
WORD_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_]*|.')


def classify(tok: str) -> str:
    if tok in MASTER:
        return KW
    if NUM_RE.fullmatch(tok):
        return NUM
    return FG


def draw_line(draw, font, y, text):
    # comment: whole line
    if text.lstrip().startswith(("//", "#")):
        draw.text((MARGIN, y), text, font=font, fill=COM)
        return
    col = 0
    i = 0
    while i < len(text):
        m = STR_RE.match(text, i)
        if m:
            s = m.group(0)
            draw.text((MARGIN + col * CELL, y), s, font=font, fill=STR)
            col += len(s); i = m.end(); continue
        m = WORD_RE.match(text, i)
        tok = m.group(0)
        # inline comment
        if tok == "/" and text[i:i+2] == "//":
            rest = text[i:]
            draw.text((MARGIN + col * CELL, y), rest, font=font, fill=COM)
            break
        color = classify(tok)
        draw.text((MARGIN + col * CELL, y), tok, font=font, fill=color)
        col += len(tok); i = m.end()


def main():
    width = MARGIN * 2 + int(60 * CELL)
    height = MARGIN * 2 + LINE * (len(lines) + 2)
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(REG), SIZE, layout_engine=ImageFont.Layout.RAQM)
    title = ImageFont.truetype(str(BOLD), int(SIZE * 1.2), layout_engine=ImageFont.Layout.RAQM)

    draw.text((MARGIN, MARGIN), "Crowquill Mono", font=title, fill=KW)
    y = MARGIN + LINE * 2
    for _, text in lines:
        if text:
            draw_line(draw, font, y, text)
        y += LINE
    img.save(OUT)
    print("salvo:", OUT)


if __name__ == "__main__":
    main()
