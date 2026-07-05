#!/usr/bin/env python3
"""Cascade hero image (Catppuccin-style): 3 code cards stacked diagonally.

Each card is a rounded window with a code snippet rendered in Crowquill Mono +
the Ink theme colors (real HarfBuzz shaping). Cards fan out back-to-front with
soft shadows.
"""
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "dist" / "CrowquillMono-Regular.ttf"
ITAL = ROOT / "dist" / "CrowquillMono-Italic.ttf"
BOLD = ROOT / "dist" / "CrowquillMono-Bold.ttf"

# Ink dark palette
BG_CANVAS = "#050505"
CARD_BG = "#0C0C0C"
CARD_BORDER = "#242424"
FG = "#B8B8B8"; BRIGHT = "#FFFFFF"; STR = "#8C8C8C"; NUM = "#D2D2D2"; COM = "#6A6A6A"
DOTS = ["#3A3A3A", "#565656", "#8C8C8C"]

MASTER = set(json.loads((ROOT / "sources" / "keywords.json").read_text())["master"])
PUNCT = set("{}[]()<>:;,.=+-*/|&!?%^~")

SIZE = 26
R = ImageFont.Layout.RAQM
reg = ImageFont.truetype(str(REG), SIZE, layout_engine=R)
ital = ImageFont.truetype(str(ITAL), SIZE, layout_engine=R)
CELL = reg.getlength("m")
LINE = int(SIZE * 1.5)
PAD = 30
BAR = 46  # window title bar

SNIPPETS = [
    ["// fibonacci", "def fib(n):", "    if n <= 1:", "        return n",
     "    return fib(n-1) + fib(n-2)"],
    ["const greet = async (name) => {", "  await log(`ola ${name}`)", "  return name != null",
     "}", "// => -> != >= <="],
    ["pub fn main() {", "  let mut xs = vec![1, 2, 3];", "  for x in xs.iter() {",
     "    match x { _ => print(x) }", "  }", "}"],
]

STR_RE = re.compile(r'"[^"]*"|\'[^\']*\'|`[^`]*`')
NUM_RE = re.compile(r'\b\d+\b')
WORD_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_]*|.')


def draw_code_line(d, x0, y, text):
    if text.lstrip().startswith(("//", "#")):
        d.text((x0, y), text, font=ital, fill=COM); return
    i = col = 0
    while i < len(text):
        m = STR_RE.match(text, i)
        if m:
            d.text((x0 + col * CELL, y), m.group(0), font=reg, fill=STR)
            col += len(m.group(0)); i = m.end(); continue
        m = WORD_RE.match(text, i); tok = m.group(0); x = x0 + col * CELL
        if (tok == "/" and text[i:i+2] == "//") or tok == "#":
            d.text((x, y), text[i:], font=ital, fill=COM); break
        if tok in MASTER: d.text((x, y), tok, font=reg, fill=BRIGHT)
        elif tok in PUNCT: d.text((x, y), tok, font=reg, fill=BRIGHT)
        elif NUM_RE.fullmatch(tok): d.text((x, y), tok, font=reg, fill=NUM)
        else: d.text((x, y), tok, font=reg, fill=FG)
        col += len(tok); i = m.end()


def make_card(lines):
    w = PAD * 2 + int(46 * CELL)
    h = BAR + PAD + LINE * len(lines) + PAD
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)
    for i, c in enumerate(DOTS):
        d.ellipse([PAD + i * 26, BAR // 2 - 7, PAD + i * 26 + 14, BAR // 2 + 7], fill=c)
    y = BAR + PAD // 2
    for ln in lines:
        draw_code_line(d, PAD, y, ln); y += LINE
    return img


def main():
    cards = [make_card(s) for s in SNIPPETS]
    dx, dy = 150, 96
    cw = max(c.width for c in cards); ch = max(c.height for c in cards)
    W = cw + dx * (len(cards) - 1) + 80
    H = ch + dy * (len(cards) - 1) + 80
    canvas = Image.new("RGBA", (W, H), BG_CANVAS)
    # back -> front
    for idx in range(len(cards) - 1, -1, -1):
        card = cards[idx]
        px = 40 + dx * idx
        py = 40 + dy * idx
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle([px + 8, py + 14, px + card.width + 8, py + card.height + 14],
                             radius=16, fill=(0, 0, 0, 170))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18))
        canvas = Image.alpha_composite(canvas, shadow)
        canvas.alpha_composite(card, (px, py))
    out = ROOT / "dist" / "hero.png"
    canvas.convert("RGB").save(out)
    print("salvo:", out, canvas.size)


if __name__ == "__main__":
    main()
