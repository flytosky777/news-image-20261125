#!/usr/bin/env python3
"""Compose the 25 November 2026 front page (1024x1024) from generated art.

Reads the six pictures in assets/, draws a newspaper front page with PIL,
and writes entry.png next to this script. Deterministic: same inputs give
the same bytes every run (PIL writes no timestamps into the PNG).
"""

import hashlib
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

PAGE = 1024
MARGIN = 36
CONTENT = PAGE - 2 * MARGIN
PAPER = (246, 241, 229)
INK = (25, 23, 19)
MUTED = (107, 98, 87)
RULE_RED = (163, 22, 33)
HAIRLINE = (180, 172, 155)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: load("DejaVuSerif-Bold.ttf", s)  # noqa: E731
F_SERIF = lambda s: load("DejaVuSerif.ttf", s)  # noqa: E731
F_SANS_B = lambda s: load("DejaVuSans-Bold.ttf", s)  # noqa: E731
F_SANS = lambda s: load("DejaVuSans.ttf", s)  # noqa: E731


# (kicker, kicker colour, headline, deck, picture file)
STORIES = [
    (
        "TOP STORY  •  UKRAINE WAR",
        RULE_RED,
        "Zelensky confirms Ukraine's sea war on Russian ships",
        "Kyiv claims drone strikes on the Sparta II in the Baltic and the "
        "Merkury off Libya; Norway urges caution.",
        "hero.png",
    ),
    (
        "U.S. – CHINA",
        (31, 78, 121),
        "Huawei guilty on 10 of 12 counts in U.S. trial",
        "Brooklyn jury convicts on fraud and trade-secret theft; acquitted "
        "of racketeering.",
        "court.webp",
    ),
    (
        "MIDDLE EAST",
        (138, 90, 0),
        "Houthi drone hits Riyadh's tallest tower, 11 hurt",
        "Second strike on the PIF Tower in a week; the 385-metre skyscraper "
        "crowns the financial district.",
        "tower.webp",
    ),
    (
        "U.S. SECURITY",
        (20, 83, 45),
        "CIA and ODNI hit by cyber breach",
        "Unclassified information exposed, NYT reports; the agencies found "
        "the intrusion.",
        "cyber.webp",
    ),
    (
        "AFRICA",
        (91, 45, 142),
        "WHO evacuates Ebola staff from Congo hospital",
        "Team sheltered three days in a maternity ward in Ituri amid "
        "fighting; 5,775 dead in the outbreak.",
        "hospital.webp",
    ),
    (
        "RUSSIA – UKRAINE",
        (122, 59, 0),
        "Putin vows retaliation for refinery strikes",
        "Calls the response 'inevitable' as drone attacks cut Russian "
        "refining by 45% since late October.",
        "refinery.webp",
    ),
]


def cover(im, width, height):
    """Centre-crop im to exactly width x height."""
    tw, th = im.size
    scale = max(width / tw, height / th)
    nw, nh = round(tw * scale), round(th * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - width) // 2
    y = (nh - height) // 2
    return im.crop((x, y, x + width, y + height))


def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, text, font_name, start, floor, width):
    """Largest font size in [floor, start] making text fit width on one line.

    Returns (font, text); ellipsises the text if it still overflows at floor.
    """
    size = start
    while size > floor:
        font = load(font_name, size)
        if draw.textlength(text, font=font) <= width:
            return font, text
        size -= 1
    font = load(font_name, floor)
    while text and draw.textlength(text + "…", font=font) > width:
        text = text[:-1].rstrip()
    return font, text + "…" if text else text


def draw_front_page():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)
    y = 30

    masthead = " ".join(list("THE WORLD IN ONE DAY"))
    draw.text((MARGIN, y), masthead, font=F_SANS_B(24), fill=MUTED)
    y += 34
    draw.text((MARGIN, y), "TUESDAY 25 NOVEMBER 2026",
              font=F_SERIF_B(56), fill=INK)
    y += 70
    draw.rectangle([MARGIN, y, MARGIN + CONTENT, y + 5], fill=RULE_RED)
    y += 14

    top = STORIES[0]
    hero = Image.open(os.path.join(ASSETS, top[4])).convert("RGB")
    page.paste(cover(hero, CONTENT, 248), (MARGIN, y))
    y += 248 + 10

    draw.text((MARGIN, y), top[0], font=F_SANS_B(19), fill=top[1])
    y += 26
    head_font = F_SERIF_B(40)
    for line in wrap(draw, top[2], head_font, CONTENT)[:2]:
        draw.text((MARGIN, y), line, font=head_font, fill=INK)
        y += 47
    deck_font = F_SANS(21)
    for line in wrap(draw, top[3], deck_font, CONTENT)[:2]:
        draw.text((MARGIN, y), line, font=deck_font, fill=INK)
        y += 26
    y += 8
    draw.line([MARGIN, y, MARGIN + CONTENT, y], fill=HAIRLINE, width=1)
    y += 12

    rows_top = y
    footer_rule = 986
    row_h = (footer_rule - 14 - rows_top) // 5
    for kicker, colour, headline, deck, pic in STORIES[1:]:
        thumb = Image.open(os.path.join(ASSETS, pic)).convert("RGB")
        page.paste(cover(thumb, 70, 70), (MARGIN, y + 2))
        tx = MARGIN + 84
        tw = CONTENT - 84
        draw.text((tx, y), kicker, font=F_SANS_B(16), fill=colour)
        h_font, h_text = fit_one_line(draw, headline, "DejaVuSerif-Bold.ttf",
                                      25, 20, tw)
        draw.text((tx, y + 22), h_text, font=h_font, fill=INK)
        d_font, d_text = fit_one_line(draw, deck, "DejaVuSans.ttf",
                                      18, 15, tw)
        draw.text((tx, y + 50), d_text, font=d_font, fill=(60, 56, 48))
        y += row_h

    draw.rectangle([MARGIN, footer_rule, MARGIN + CONTENT, footer_rule + 3],
                   fill=RULE_RED)
    foot = ("All events reported on Tuesday 25 November 2026  —  Sources: "
            "Reuters  •  AP  •  CNN  •  The Hindu  •  Dawn  •  UN News")
    f_font, f_text = fit_one_line(draw, foot, "DejaVuSans.ttf", 15, 12,
                                  CONTENT)
    draw.text((MARGIN, footer_rule + 10), f_text, font=f_font, fill=MUTED)
    return page


def main():
    page = draw_front_page()
    page.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    digest = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print(f"wrote {OUT} ({size} bytes) sha256 {digest}")
    if size > 1048576:
        print("ERROR: over the 1 MiB cap", file=sys.stderr)
        sys.exit(1)
    if page.size != (1024, 1024):
        print("ERROR: not 1024x1024", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
