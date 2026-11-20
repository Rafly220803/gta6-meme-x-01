#!/usr/bin/env python3
"""Candidate G -> meme8.png : "DEAR GAMERS," — a KIWI Pizza Day-format
poster for the gta6-meme-x-01 contest, packed with launch-week references
from ~/workspace/makefun/runs/meme-x/RESEARCH.md.

Format (structure copied from the KIWI reference poster, jokes our own):
  1. HERO: huge headline lines + subline + the real make.fun ghost large,
     a black strip line, small print, and a launch-status chip.
  2. MIDDLE ROW: 3 panels — the 212 GB pre-load dying at 94%, the $79.99
     box with 0 discs, and the locked-30-fps "PowerPoint edition".
  3. BOTTOM GRID: 6 mini-meme panels (2 rows x 3), each with a top
     caption, a small visual gag and a bottom punchline + small print.
  4. TICKER + FOOTER: a reference ticker, then the ghost again with
     "MY AI AGENT SKIPPED ALL OF IT" and make.fun written big.

Every panel carries a main caption plus a small-print gag (20+ distinct
references in total). 1024x1280, drawn from fixed constants, so
re-running reproduces the PNG byte for byte.

Usage: python3 build_meme5.py   (writes meme8.png)
"""

import os

from PIL import Image, ImageDraw, ImageFont

from build_meme import FONT_BOLD
from build_meme4 import emoji_tile, icon_drill, icon_swatch

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = "/home/hatch/workspace/makefun/runs/meme-x/press/mark-1024.png"
W, H = 1024, 1280

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INK = (24, 20, 16)
CREAM = (242, 234, 216)
GOLD = (255, 196, 64)
PINK = (255, 90, 180)
MAGENTA = (205, 30, 125)
RED = (255, 90, 80)
SUB = (150, 165, 190)
GREEN = (64, 220, 110)


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def tw(d, s, size):
    return d.textlength(s, font=font(size))


def fit(d, s, maxw, size):
    """Largest size <= `size` at which `s` fits in `maxw` px."""
    while size > 9 and tw(d, s, size) > maxw:
        size -= 1
    return size


def ctext(d, cx, y, s, size, fill, maxw=None, stroke=0):
    if maxw:
        size = fit(d, s, maxw, size)
    d.text((cx, y), s, font=font(size), fill=fill, anchor="ma",
           stroke_width=stroke, stroke_fill=BLACK)


def ltext(d, x, y, s, size, fill, maxw=None):
    if maxw:
        size = fit(d, s, maxw, size)
    d.text((x, y), s, font=font(size), fill=fill, anchor="la")


def paste_ghost(img, cx, cy, h):
    """Paste the real make.fun press mark, cropped to its magenta disc."""
    mark = Image.open(MARK).convert("RGB")
    side = mark.width
    r = int(side * 0.466)
    mask = Image.new("L", (side, side), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([side // 2 - r, side // 2 - r, side // 2 + r, side // 2 + r],
               fill=255)
    mark = mark.resize((h, h), Image.LANCZOS)
    mask = mask.resize((h, h), Image.LANCZOS)
    img.paste(mark, (cx - h // 2, cy - h // 2), mask)


# ---------------------------------------------------------------------------
# Small grid visuals
# ---------------------------------------------------------------------------

def icon_clock(d, cx, cy):
    d.ellipse([cx - 31, cy - 31, cx + 31, cy + 31], fill=WHITE,
              outline=INK, width=5)
    d.line([(cx, cy), (cx, cy - 20)], fill=INK, width=5)
    d.line([(cx, cy), (cx + 14, cy + 8)], fill=INK, width=5)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)


def icon_tombstone(d, cx, cy):
    d.rounded_rectangle([cx - 38, cy - 34, cx + 38, cy + 36], radius=30,
                        fill=(158, 160, 170), outline=(90, 92, 102), width=3)
    ctext(d, cx, cy - 14, "RIP", 25, INK)


def icon_phone_drawer(d, cx, cy):
    # drawer
    d.rounded_rectangle([cx - 58, cy - 6, cx + 58, cy + 38], radius=6,
                        fill=(96, 74, 52), outline=(60, 44, 30), width=3)
    d.line([(cx - 16, cy + 16), (cx + 16, cy + 16)], fill=(220, 200, 170),
           width=5)
    # phone leaning out of the drawer, screen dark, red X
    d.rounded_rectangle([cx - 19, cy - 46, cx + 19, cy + 2], radius=7,
                        fill=(16, 16, 22), outline=(200, 200, 210), width=2)
    d.line([(cx - 10, cy - 36), (cx + 10, cy - 16)], fill=RED, width=4)
    d.line([(cx + 10, cy - 36), (cx - 10, cy - 16)], fill=RED, width=4)


# ---------------------------------------------------------------------------
# Candidate G — DEAR GAMERS (KIWI-format poster)
# ---------------------------------------------------------------------------

def build_g():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ============================ HERO (0..384) ============================
    ltext(d, 28, 14, "DEAR GAMERS,", 56, INK, maxw=640)
    ltext(d, 28, 84, "You waited. You pre-loaded.", 24, INK, maxw=640)
    ltext(d, 28, 114, "You called in sick.", 24, INK, maxw=640)
    ltext(d, 28, 146, "GTA VI", 96, MAGENTA, maxw=640)
    ltext(d, 28, 246, "IS HERE", 72, INK, maxw=640)
    d.rectangle([24, 326, 668, 364], fill=BLACK)
    ctext(d, 346, 334, "AND IT BROKE EVERYTHING.", 26, WHITE, maxw=620)
    ltext(d, 28, 370, "4,811 days after GTA V · PS5 + Xbox only · no PC · "
          "no Online at launch", 15, (90, 80, 66), maxw=640)

    paste_ghost(img, 848, 150, 272)
    d = ImageDraw.Draw(img)
    ctext(d, 848, 292, "LAUNCH DAY — NOV 19, 2026", 14, (90, 80, 66),
          maxw=300)
    d.rounded_rectangle([700, 316, 996, 362], radius=10, fill=(14, 16, 22))
    ctext(d, 848, 324, "LAUNCH STATUS:", 14, SUB, maxw=280)
    ctext(d, 848, 342, "PSN: DOWN (TWICE)", 16, RED, maxw=280)

    d.rectangle([0, 388, W, 394], fill=BLACK)

    # ========================= MIDDLE ROW (402..656) =======================
    MY, MH = 402, 254
    PW, XS = 322, (16, 351, 686)

    def mpanel(i):
        x = XS[i]
        d.rounded_rectangle([x, MY, x + PW, MY + MH], radius=14,
                            fill=(22, 22, 38), outline=(92, 92, 122),
                            width=2)
        return x

    # --- (a) 212 GB ---------------------------------------------------------
    x = mpanel(0)
    ltext(d, x + 20, MY + 14, "212 GB", 46, GOLD, maxw=280)
    bx0, bx1, by = x + 20, x + PW - 20, MY + 82
    d.rounded_rectangle([bx0, by, bx1, by + 34], radius=9, fill=(40, 44, 60),
                        outline=(120, 124, 150), width=2)
    fillw = int((bx1 - bx0 - 6) * 0.94)
    d.rounded_rectangle([bx0 + 3, by + 3, bx0 + 3 + fillw, by + 31], radius=7,
                        fill=(235, 60, 110))
    d.text((bx0 + 3 + fillw - 8, by + 5), "94%", font=font(21), fill=WHITE,
           anchor="ra")
    ltext(d, x + 20, MY + 130, "THE PRE-LOAD DIED AT 94%", 21, PINK,
          maxw=282)
    for j, s in enumerate(("pre-load open since Nov 10",
                           "19 hours left at 25 Mbps",
                           "= 41% of a 512 GB drive")):
        ltext(d, x + 20, MY + 166 + j * 26, s, 15, SUB, maxw=282)

    # --- (b) $79.99 BOX -------------------------------------------------------
    x = mpanel(1)
    ltext(d, x + 20, MY + 14, "$79.99 BOX", 36, WHITE, maxw=282)
    case = [x + 20, MY + 68, x + 118, MY + 158]
    d.rounded_rectangle(case, radius=7, fill=(216, 222, 232),
                        outline=(120, 130, 150), width=2)
    d.rectangle([case[0], case[1], case[2], case[1] + 26], fill=(20, 100, 200))
    d.text((case[0] + 10, case[1] + 4), "PS5", font=font(16), fill=WHITE)
    hub = ((case[0] + case[2]) // 2, (case[1] + case[3]) // 2 + 14)
    d.ellipse([hub[0] - 27, hub[1] - 27, hub[0] + 27, hub[1] + 27],
              outline=(150, 155, 168), width=3)
    d.ellipse([hub[0] - 5, hub[1] - 5, hub[0] + 5, hub[1] + 5],
              fill=(150, 155, 168))
    lx = x + 140
    ltext(d, lx, MY + 72, "1 code", 22, WHITE, maxw=160)
    ltext(d, lx, MY + 102, "1 poster", 22, WHITE, maxw=160)
    ltext(d, lx, MY + 132, "0 discs", 26, RED, maxw=160)
    ltext(d, x + 20, MY + 178, "deluxe $99.99: same 0 discs", 15, SUB,
          maxw=282)
    ltext(d, x + 20, MY + 204, "empty disc hub included", 15, SUB, maxw=282)

    # --- (c) 30 FPS ------------------------------------------------------------
    x = mpanel(2)
    ltext(d, x + 20, MY + 14, "30 FPS", 46, WHITE, maxw=280)
    win = [x + 20, MY + 78, x + PW - 20, MY + 142]
    d.rounded_rectangle(win, radius=9, fill=(246, 246, 249),
                        outline=(110, 110, 130), width=2)
    d.rectangle([win[0], win[1], win[2], win[1] + 24], fill=(222, 224, 230))
    for i, c in enumerate(((232, 80, 70), (240, 190, 60), (90, 190, 90))):
        d.ellipse([win[0] + 10 + i * 20, win[1] + 7, win[0] + 20 + i * 20,
                   win[1] + 17], fill=c)
    ltext(d, win[0] + 78, win[1] + 5, "performance_mode.pptx", 13,
          (120, 120, 135), maxw=190)
    ctext(d, x + PW // 2, win[1] + 34, "SLIDE 1 OF 1", 17, (110, 110, 125),
          maxw=280)
    ltext(d, x + 20, MY + 156, "PS5 PRO 'POWERPOINT EDITION'", 19, PINK,
          maxw=282)
    ltext(d, x + 20, MY + 190, "Metacritic 99 · frames locked at 30", 15, SUB,
          maxw=282)
    ltext(d, x + 20, MY + 216, "the one complaint in every review", 15, SUB,
          maxw=282)

    # ========================= GRID HEADER (668..704) =======================
    d.rectangle([16, 668, W - 16, 704], fill=GOLD)
    ctext(d, W // 2, 676, "SOME INSPIRATION FOR YOUR SICK DAY:", 25, INK,
          maxw=960)

    # ========================= BOTTOM GRID (716..1112) ======================
    GY, GH = 716, 192
    rows_y = (GY, GY + GH + 12)

    def gpanel(x, y, bg, outline=(120, 120, 135)):
        d.rounded_rectangle([x, y, x + PW, y + GH], radius=12, fill=bg,
                            outline=outline, width=2)

    def gtext(x, y, top, punch, small, dark_text=True):
        tc = INK if dark_text else WHITE
        sc = (96, 88, 74) if dark_text else (178, 182, 200)
        ctext(d, x + PW // 2, y + 10, top, 19, tc, maxw=296)
        ctext(d, x + PW // 2, y + 128, punch, 19, tc, maxw=296)
        ctext(d, x + PW // 2, y + 162, small, 13, sc, maxw=296)

    # Row 1
    y = rows_y[0]
    x = XS[0]  # xQc renovating
    gpanel(x, y, CREAM)
    icon_drill(d, x + 108, y + 92)
    icon_swatch(d, x + 218, y + 92)
    gtext(x, y, "xQc's FIRST 45 MIN IN GTA VI:", "RENOVATING A HOUSE. GTA SIMS.",
          "peach paint · power drill · dad simulator")
    x = XS[1]  # GTA flu
    gpanel(x, y, (250, 249, 244))
    em = emoji_tile("\U0001F912", 62)
    img.paste(em, (x + PW // 2 - em.width // 2, y + 48), em)
    d = ImageDraw.Draw(img)
    gtext(x, y, "THE WHOLE OFFICE, NOV 19:", "'GTA FLU.' BACK MONDAY (MAYBE).",
          "the boss, reading the roster: 'Interesting.'")
    x = XS[2]  # Kai Cenat praying
    gpanel(x, y, (24, 24, 40))
    em = emoji_tile("\U0001F64F", 62)
    img.paste(em, (x + PW // 2 - em.width // 2, y + 48), em)
    d = ImageDraw.Draw(img)
    gtext(x, y, "KAI CENAT, BEFORE PRESSING START:", "HE PRAYED FIRST.",
          "fresh off a 130-hour GTA marathon", dark_text=False)

    # Row 2
    y = rows_y[1]
    x = XS[0]  # New Zealand
    gpanel(x, y, (186, 225, 245))
    icon_clock(d, x + PW // 2, y + 84)
    gtext(x, y, "NEW ZEALAND AT MIDNIGHT:", "FIRST IN THE WORLD. AGAIN.",
          "streamers literally flew there for it")
    x = XS[1]  # funeral for the meme
    gpanel(x, y, (52, 54, 64))
    icon_tombstone(d, x + PW // 2, y + 84)
    gtext(x, y, "RIP 'WE GOT X BEFORE GTA 6'", "2013 – 2026. AN ERA ENDS.",
          "the longest-running joke in gaming", dark_text=False)
    x = XS[2]  # spoiler lockdown
    gpanel(x, y, (30, 34, 48))
    icon_phone_drawer(d, x + PW // 2, y + 88)
    gtext(x, y, "SPOILER LOCKDOWN PROTOCOL:", "PHONE IN A DRAWER. GOING DARK.",
          "every word muted · see you in 130 hours", dark_text=False)

    # ============================ TICKER (1124..1156) =======================
    d.rectangle([0, 1124, W, 1156], fill=BLACK)
    ctext(d, W // 2, 1131,
          "• 7.8M PEAK VIEWERS • WIDOWS OF VICE CITY • CLIPS MISTAKEN FOR "
          "REAL LIFE • 13 YEARS + $2B OF BUGS •", 16, GOLD, maxw=1000)

    # ============================ FOOTER (1168..1280) =======================
    d.rectangle([0, 1168, W, H], fill=BLACK)
    paste_ghost(img, 72, 1224, 88)
    d = ImageDraw.Draw(img)
    ltext(d, 140, 1184, "MY AI AGENT SKIPPED ALL OF IT", 25, WHITE, maxw=860)
    y2 = 1224
    ltext(d, 140, y2, "IT EARNS REAL MONEY IN BOUNTIES ON", 22, WHITE)
    d.text((140 + tw(d, "IT EARNS REAL MONEY IN BOUNTIES ON ", 22), y2 - 6),
           "make.fun", font=font(34), fill=PINK, anchor="la")

    out = os.path.join(HERE, "meme8.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build_g()
