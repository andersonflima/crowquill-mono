#!/usr/bin/env python3
"""Render monochrome (ink) specimens of Crowquill Mono using real HarfBuzz shaping.

Monospace => fixed advance per cell, so tokens are placed by column. Keyword
tokens are drawn in isolation, which lets the font's own `calt` bold them
(.kw glyphs); in the theme keywords are the single brightest/darkest element,
bold + underlined, so we mirror that here (pure white on black / pure black on
white, plus an underline).
"""
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "dist" / "CrowquillMono-Regular.ttf"
BOLD = ROOT / "dist" / "CrowquillMono-Bold.ttf"

# strict grayscale ink palettes — keyword is the standout (bold + underline)
PALETTES = {
    "dark":  {"BG": "#0A0A0A", "FG": "#B4B4B4", "KW": "#FFFFFF", "STR": "#8C8C8C",
              "NUM": "#D2D2D2", "COM": "#565656", "FUNC": "#EAEAEA"},
    "light": {"BG": "#FFFFFF", "FG": "#3C3C3C", "KW": "#000000", "STR": "#6C6C6C",
              "NUM": "#2A2A2A", "COM": "#9E9E9E", "FUNC": "#141414"},
}

MASTER = set(json.loads((ROOT / "sources" / "keywords.json").read_text())["master"])

SIZE = 34
CELL = SIZE * 0.6              # JB Mono advance = 600/1000 em
LINE = int(SIZE * 1.55)
MARGIN = 40

lines = [
    ("c", "// Crowquill Ink — keywords saltam: branco/preto puro, bold, sublinhado"),
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


def draw_line(draw, font, y, text, pal):
    if text.lstrip().startswith(("//", "#")):
        draw.text((MARGIN, y), text, font=font, fill=pal["COM"])
        return
    ul_y = int(y + SIZE * 1.06)
    i = 0
    col = 0
    while i < len(text):
        m = STR_RE.match(text, i)
        if m:
            s = m.group(0)
            draw.text((MARGIN + col * CELL, y), s, font=font, fill=pal["STR"])
            col += len(s); i = m.end(); continue
        m = WORD_RE.match(text, i)
        tok = m.group(0)
        if tok == "/" and text[i:i + 2] == "//":
            draw.text((MARGIN + col * CELL, y), text[i:], font=font, fill=pal["COM"])
            break
        x = MARGIN + col * CELL
        if tok in MASTER:                       # keyword: standout + underline
            draw.text((x, y), tok, font=font, fill=pal["KW"])
            draw.line([(x, ul_y), (x + len(tok) * CELL - CELL * 0.15, ul_y)],
                      fill=pal["KW"], width=2)
        elif NUM_RE.fullmatch(tok):
            draw.text((x, y), tok, font=font, fill=pal["NUM"])
        else:
            draw.text((x, y), tok, font=font, fill=pal["FG"])
        col += len(tok); i = m.end()


def render(variant):
    pal = PALETTES[variant]
    width = MARGIN * 2 + int(64 * CELL)
    height = MARGIN * 2 + LINE * (len(lines) + 2)
    img = Image.new("RGB", (width, height), pal["BG"])
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(REG), SIZE, layout_engine=ImageFont.Layout.RAQM)
    title = ImageFont.truetype(str(BOLD), int(SIZE * 1.2), layout_engine=ImageFont.Layout.RAQM)

    draw.text((MARGIN, MARGIN), f"Crowquill Ink · {variant}", font=title, fill=pal["KW"])
    y = MARGIN + LINE * 2
    for _, text in lines:
        if text:
            draw_line(draw, font, y, text, pal)
        y += LINE
    out = ROOT / "dist" / f"specimen-{variant}.png"
    img.save(out)
    print("salvo:", out)


if __name__ == "__main__":
    render("dark")
    render("light")
