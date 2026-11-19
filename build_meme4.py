#!/usr/bin/env python3
"""Deterministic builders for round 4 of the gta6-meme-x-01 memes.

Round 4 is built from real launch-week community research
(~/workspace/makefun/runs/meme-x/RESEARCH.md), following the user's formula:
one image, many layered jokes, and the mandatory make.fun elements inside
the picture (the real ghost, large, plus the name "make.fun" in-image).

Candidate E -> meme6.png : "WHAT OTHERS DO vs WHAT I DO" — the #1 most
shared still format of launch week (9GAG 130K likes). Band 1: the crime
chaos everyone expected. Band 2: the life-sim reality — xQc's 45-minute
house renovation (drill, peach paint), TypicalGamer fixing his porch with
a nail gun, gym, hoops, cooking — "GTA Sims / dad simulator". Band 3, the
twist: the player's AI agent winning real-money bounties on make.fun.

Candidate F -> meme7.png : "LAUNCH DAY STARTER PACK" — a 2x2 collage of
the launch pain cluster from the research: the 212 GB pre-load dying at
94% (~19 hrs at 25 Mbps), the $79.99 box with no disc (1 code, 1 poster,
0 discs), the locked-30-fps "PowerPoint" on PS5 Pro, and the GTA-flu sick
note — plus the agent's launch day: no download, no queue, just bounties.

Both are 1200x675, drawn from fixed constants, so re-running reproduces
the PNGs byte for byte.

Usage: python3 build_meme4.py   (writes meme6.png and meme7.png)
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

from build_meme import FONT_BOLD, draw_money_bag
from build_meme2 import paste_ghost, star

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 675
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 196, 64)
PINK = (255, 90, 180)
INK = (38, 33, 28)


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def tw(d, s, size):
    return d.textlength(s, font=font(size))


def ctext(d, cx, y, s, size, fill, stroke=0):
    d.text((cx, y), s, font=font(size), fill=fill, anchor="ma",
           stroke_width=stroke, stroke_fill=BLACK)


# ---------------------------------------------------------------------------
# Emoji helper (same approach as build_meme3: native strike, scaled)
# ---------------------------------------------------------------------------

_emoji_cache = {}


def emoji_tile(ch, height):
    key = (ch, height)
    if key in _emoji_cache:
        return _emoji_cache[key]
    f = ImageFont.truetype(EMOJI_FONT, 109)
    tile = Image.new("RGBA", (170, 170), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.text((8, 2), ch, font=f, embedded_color=True)
    tile = tile.crop(tile.getbbox())
    w = max(1, round(tile.width * height / tile.height))
    tile = tile.resize((w, height), Image.LANCZOS)
    _emoji_cache[key] = tile
    return tile


def money_bag_tile(height):
    """draw_money_bag rendered on its own tile, scaled to `height` px."""
    tile = Image.new("RGBA", (150, 160), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    draw_money_bag(td, 75, 152)
    tile = tile.crop(tile.getbbox())
    w = max(1, round(tile.width * height / tile.height))
    return tile.resize((w, height), Image.LANCZOS)


# ---------------------------------------------------------------------------
# Small icons (fixed geometry, flat style)
# ---------------------------------------------------------------------------

def icon_supercar(d, cx, cy):
    body = (255, 84, 56)
    dark = (24, 24, 34)
    # low sleek body
    d.rounded_rectangle([cx - 95, cy - 6, cx + 95, cy + 22], radius=12,
                        fill=body)
    d.polygon([(cx - 52, cy - 6), (cx - 26, cy - 30), (cx + 30, cy - 30),
               (cx + 58, cy - 6)], fill=body)
    d.polygon([(cx - 40, cy - 8), (cx - 22, cy - 25), (cx - 2, cy - 25),
               (cx - 2, cy - 8)], fill=dark)
    d.polygon([(cx + 5, cy - 8), (cx + 5, cy - 25), (cx + 26, cy - 25),
               (cx + 44, cy - 8)], fill=dark)
    # spoiler
    d.rectangle([cx + 62, cy - 26, cx + 68, cy - 8], fill=(160, 40, 26))
    d.rounded_rectangle([cx + 48, cy - 32, cx + 92, cy - 24], radius=4,
                        fill=(200, 52, 34))
    for wx in (cx - 58, cx + 58):
        d.ellipse([wx - 16, cy + 8, wx + 16, cy + 40], fill=(14, 14, 18),
                  outline=(175, 175, 185), width=3)
        d.ellipse([wx - 5, cy + 19, wx + 5, cy + 29], fill=(175, 175, 185))
    d.line([(cx - 112, cy + 42), (cx + 112, cy + 42)], fill=(90, 30, 20),
           width=3)


def icon_explosion(d, cx, cy):
    pts = []
    for i in range(24):
        r = 62 if i % 2 == 0 else 30
        a = math.radians(i * 15)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.92))
    d.polygon(pts, fill=(255, 122, 26), outline=(150, 50, 0))
    d.ellipse([cx - 27, cy - 25, cx + 27, cy + 25], fill=(255, 205, 64))
    d.ellipse([cx - 12, cy - 11, cx + 12, cy + 11], fill=(255, 240, 180))


def icon_stopwatch_chip(d, x1, y0, y1):
    """Chip sized to its label: stopwatch icon + 'STORY MODE SPEEDRUN'."""
    label = "STORY MODE SPEEDRUN"
    x0 = x1 - (74 + tw(d, label, 24) + 20)
    d.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=(30, 16, 24),
                        outline=WHITE, width=3)
    cx, cy = x0 + 40, (y0 + y1) // 2
    d.rectangle([cx - 4, cy - 34, cx + 4, cy - 26], fill=GOLD)
    d.ellipse([cx - 21, cy - 26, cx + 21, cy + 16], outline=GOLD, width=5)
    d.line([(cx, cy - 5), (cx, cy - 18)], fill=GOLD, width=4)
    d.line([(cx, cy - 5), (cx + 10, cy - 5)], fill=GOLD, width=4)
    d.text((x0 + 74, cy), label, font=font(24), fill=WHITE, anchor="lm")


def icon_drill(d, cx, cy):
    teal = (0, 148, 158)
    dark = (30, 34, 40)
    # body + top handle
    d.rounded_rectangle([cx - 46, cy - 26, cx + 30, cy - 2], radius=8,
                        fill=teal)
    d.rounded_rectangle([cx - 40, cy - 38, cx + 6, cy - 24], radius=7,
                        fill=teal)
    # grip + battery
    d.polygon([(cx - 38, cy - 2), (cx - 14, cy - 2), (cx - 18, cy + 26),
               (cx - 34, cy + 26)], fill=dark)
    d.rounded_rectangle([cx - 42, cy + 24, cx - 8, cy + 36], radius=4,
                        fill=(52, 58, 66))
    # chuck + bit
    d.polygon([(cx + 30, cy - 22), (cx + 44, cy - 18), (cx + 44, cy - 8),
               (cx + 30, cy - 4)], fill=(120, 128, 138))
    d.line([(cx + 44, cy - 13), (cx + 62, cy - 13)], fill=(200, 205, 212),
           width=4)


def icon_swatch(d, cx, cy):
    d.rounded_rectangle([cx - 38, cy - 34, cx + 38, cy + 34], radius=8,
                        fill=WHITE, outline=(150, 140, 125), width=2)
    shades = [(255, 183, 140), (255, 203, 164), (255, 224, 198)]
    for i, c in enumerate(shades):
        y0 = cy - 26 + i * 18
        d.rounded_rectangle([cx - 30, y0, cx + 30, y0 + 14], radius=4, fill=c)


def icon_nailgun(d, cx, cy):
    orange = (242, 122, 30)
    dark = (34, 36, 42)
    # main body
    d.rounded_rectangle([cx - 48, cy - 30, cx + 40, cy - 8], radius=8,
                        fill=orange)
    d.rectangle([cx - 48, cy - 38, cx + 24, cy - 28], fill=dark)
    # nose
    d.polygon([(cx + 40, cy - 28), (cx + 54, cy - 22), (cx + 54, cy - 12),
               (cx + 40, cy - 8)], fill=(120, 126, 134))
    # grip + magazine
    d.polygon([(cx - 40, cy - 8), (cx - 18, cy - 8), (cx - 24, cy + 30),
               (cx - 40, cy + 30)], fill=dark)
    d.polygon([(cx + 8, cy - 8), (cx + 24, cy - 8), (cx + 34, cy + 28),
               (cx + 20, cy + 28)], fill=(90, 96, 104))
    d.line([(cx + 54, cy + 2), (cx + 54, cy + 14)], fill=(200, 205, 212),
           width=3)


def icon_benchpress(d, cx, cy):
    steel = (96, 104, 116)
    dark = (30, 32, 40)
    # bench
    d.rounded_rectangle([cx - 52, cy + 16, cx + 30, cy + 26], radius=5,
                        fill=(70, 74, 84))
    d.rectangle([cx - 40, cy + 26, cx - 32, cy + 38], fill=dark)
    d.rectangle([cx + 14, cy + 26, cx + 22, cy + 38], fill=dark)
    # upright + bar
    d.rectangle([cx + 34, cy - 30, cx + 40, cy + 26], fill=steel)
    d.line([(cx - 58, cy - 24), (cx + 62, cy - 24)], fill=(170, 176, 186),
           width=5)
    # plates
    for px, wdt in ((cx - 58, 9), (cx - 46, 7)):
        d.rounded_rectangle([px, cy - 42, px + wdt, cy - 6], radius=3,
                            fill=dark)
    for px, wdt in ((cx + 42, 7), (cx + 52, 9)):
        d.rounded_rectangle([px, cy - 42, px + wdt, cy - 6], radius=3,
                            fill=dark)
    # lifter: head + torso on the bench
    d.ellipse([cx - 30, cy - 2, cx - 12, cy + 16], fill=(232, 184, 148))
    d.line([(cx - 21, cy + 2), (cx - 21, cy - 20)], fill=(60, 90, 160),
           width=5)


def icon_hoop(d, cx, cy):
    d.rectangle([cx + 22, cy - 40, cx + 30, cy + 40], fill=(80, 86, 96))
    d.rectangle([cx - 34, cy - 40, cx + 24, cy - 6], fill=WHITE,
                outline=(240, 110, 40), width=3)
    d.rectangle([cx - 16, cy - 30, cx + 6, cy - 14], outline=(240, 110, 40),
                width=2)
    d.ellipse([cx - 17, cy - 8, cx + 7, cy + 2], outline=(240, 110, 40),
              width=4)
    for i in range(3):
        x = cx - 13 + i * 9
        d.line([(x, cy + 1), (x - 3 + i * 3, cy + 18)], fill=(200, 200, 205),
               width=2)


def icon_pan(d, cx, cy):
    d.ellipse([cx - 34, cy - 30, cx + 26, cy + 30], fill=(26, 26, 30),
              outline=(90, 90, 98), width=3)
    d.rounded_rectangle([cx + 24, cy - 6, cx + 62, cy + 4], radius=4,
                        fill=(26, 26, 30))
    d.ellipse([cx - 22, cy - 18, cx + 14, cy + 18], fill=(250, 246, 238))
    d.ellipse([cx - 11, cy - 9, cx + 5, cy + 9], fill=(255, 176, 32))


# ---------------------------------------------------------------------------
# Candidate E — WHAT OTHERS DO vs WHAT I DO (three bands)
# ---------------------------------------------------------------------------

def build_e():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)

    B1, B2, B3 = 205, 445, 675  # band boundaries

    # --- Band 1: chaos (red/orange gradient) --------------------------------
    for yy in range(0, B1):
        t = yy / B1
        c = tuple(int((110 + (208 - 110) * t) if i == 0 else
                      (20 + (76 - 20) * t) if i == 1 else
                      (14 + (22 - 14) * t)) for i in range(3))
        d.line([(0, yy), (W, yy)], fill=c)
    d.text((28, 12), "WHAT OTHERS DO IN GTA VI", font=font(38), fill=WHITE,
           stroke_width=2, stroke_fill=BLACK)
    items1 = [(150, "STOLEN SUPERCAR"), (430, "FIVE STARS"),
              (690, "TOTAL MAYHEM")]
    icon_supercar(d, 150, 108)
    for i in range(5):
        star(d, 318 + i * 56, 104, 26)
    icon_explosion(d, 690, 106)
    icon_stopwatch_chip(d, 1156, 76, 140)
    for cx, cap in items1:
        ctext(d, cx, 158, cap, 23, WHITE, stroke=1)

    # --- Band 2: calm life-sim (pastel) --------------------------------------
    d.rectangle([0, B1, W, B2], fill=(240, 234, 216))
    for gx in range(30, W, 76):  # faint wallpaper dots
        for gy in range(B1 + 34, B2, 76):
            d.ellipse([gx - 7, gy - 7, gx + 7, gy + 7], fill=(231, 222, 196))
    d.rectangle([0, B1, W, B1 + 5], fill=BLACK)
    d.text((28, B1 + 13), "WHAT I DO IN GTA VI", font=font(36), fill=INK)
    chip = "GTA SIMS — dad simulator"
    chw = tw(d, chip, 23) + 34
    d.rounded_rectangle([W - 28 - chw, B1 + 12, W - 28, B1 + 52], radius=12,
                        fill=WHITE, outline=INK, width=2)
    d.text((W - 28 - chw / 2, B1 + 20), chip, font=font(23), fill=INK,
           anchor="ma")
    icons2 = [icon_drill, icon_swatch, icon_nailgun, icon_benchpress,
              icon_hoop, icon_pan]
    caps2 = ["home reno", "peach paint", "fixing my porch", "bench press",
             "shooting hoops", "cooking dinner"]
    centers = [110, 305, 500, 695, 890, 1085]
    for fn, cx, cap in zip(icons2, centers, caps2):
        fn(d, cx, 348)
        ctext(d, cx, 398, cap, 24, INK)

    # --- Band 3: the agent twist (make.fun pink/black) -----------------------
    d.rectangle([0, B2, W, B3], fill=(10, 6, 14))
    d.rectangle([0, B2, W, B2 + 5], fill=PINK)
    paste_ghost(img, 128, (B2 + B3) // 2 + 4, 192)
    d = ImageDraw.Draw(img)
    bag = money_bag_tile(118)
    img.paste(bag, (252, B3 - 14 - bag.height), bag)
    d = ImageDraw.Draw(img)
    tx = 372
    d.text((tx, B2 + 26), "WHAT MY AI AGENT DOES:", font=font(30), fill=GOLD)
    d.text((tx, B2 + 70), "WINS REAL-MONEY BOUNTIES", font=font(42),
           fill=WHITE)
    y3 = B2 + 124
    d.text((tx, y3), "ON ", font=font(42), fill=WHITE)
    d.text((tx + tw(d, "ON ", 42), y3), "make.fun", font=font(42), fill=PINK)
    d.text((tx, y3 + 58), "no sick days. no 212 GB download.",
           font=font(24), fill=(216, 178, 205))

    out = os.path.join(HERE, "meme6.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


# ---------------------------------------------------------------------------
# Candidate F — LAUNCH DAY STARTER PACK (2x2 grid + bottom strip)
# ---------------------------------------------------------------------------

PANEL_BG = (24, 24, 40)
PANEL_LINE = (92, 92, 122)
SUB = (150, 165, 190)


def panel(d, box):
    d.rounded_rectangle(box, radius=14, fill=PANEL_BG, outline=PANEL_LINE,
                        width=2)


def build_f():
    img = Image.new("RGB", (W, H), (13, 11, 24))
    d = ImageDraw.Draw(img)

    # header
    d.rectangle([0, 0, W, 56], fill=(10, 8, 20))
    d.line([(0, 57), (W, 57)], fill=PINK, width=3)
    ctext(d, W // 2, 9, "GTA VI LAUNCH DAY STARTER PACK", 34, WHITE)

    mx, gap, pw, ph, top = 16, 14, 577, 228, 72
    boxes = [(mx, top), (mx + pw + gap, top), (mx, top + ph + gap),
             (mx + pw + gap, top + ph + gap)]
    for b in boxes:
        panel(d, [b[0], b[1], b[0] + pw, b[1] + ph])

    # --- P1: the pre-load ----------------------------------------------------
    x0, y0 = boxes[0]
    d.text((x0 + 24, y0 + 14), "THE PRE-LOAD", font=font(21), fill=SUB)
    bx0, bx1, by = x0 + 24, x0 + pw - 24, y0 + 66
    d.rounded_rectangle([bx0, by, bx1, by + 36], radius=10, fill=(40, 44, 60),
                        outline=(120, 124, 150), width=2)
    fillw = int((bx1 - bx0 - 6) * 0.94)
    d.rounded_rectangle([bx0 + 3, by + 3, bx0 + 3 + fillw, by + 33], radius=8,
                        fill=(235, 60, 110))
    d.text((bx0 + 3 + fillw - 10, by + 5), "94%", font=font(25), fill=WHITE,
           anchor="ra")
    ctext(d, x0 + pw // 2, y0 + 122, "212 GB — 19 hrs left (25 Mbps)", 27,
          WHITE)
    ctext(d, x0 + pw // 2, y0 + 168, "pre-load died at 94%", 21, (160, 160, 175))

    # --- P2: the empty box ----------------------------------------------------
    x0, y0 = boxes[1]
    case = [x0 + 34, y0 + 20, x0 + 174, y0 + 210]
    d.rounded_rectangle(case, radius=8, fill=(216, 222, 232),
                        outline=(120, 130, 150), width=2)
    d.rectangle([case[0], case[1], case[2], case[1] + 32], fill=(20, 100, 200))
    d.text((case[0] + 12, case[1] + 5), "PS5", font=font(19), fill=WHITE)
    hub = ((case[0] + case[2]) // 2, (case[1] + case[3]) // 2 + 16)
    d.ellipse([hub[0] - 34, hub[1] - 34, hub[0] + 34, hub[1] + 34],
              outline=(150, 155, 168), width=3)
    d.ellipse([hub[0] - 6, hub[1] - 6, hub[0] + 6, hub[1] + 6],
              fill=(150, 155, 168))
    tag = Image.new("RGBA", (132, 48), (0, 0, 0, 0))
    tgd = ImageDraw.Draw(tag)
    tgd.rounded_rectangle([0, 0, 131, 47], radius=10, fill=(255, 196, 64),
                          outline=(120, 84, 10), width=2)
    tgd.text((66, 8), "$79.99", font=font(27), fill=(74, 48, 6), anchor="ma")
    tag = tag.rotate(12, expand=True, resample=Image.BICUBIC)
    img.paste(tag, (x0 + 108, y0 + 2), tag)
    d = ImageDraw.Draw(img)
    lx = x0 + 292
    d.text((lx, y0 + 26), "IN THE BOX:", font=font(20), fill=SUB)
    d.text((lx, y0 + 58), "1 code", font=font(27), fill=WHITE)
    d.text((lx, y0 + 94), "1 poster", font=font(27), fill=WHITE)
    d.text((lx, y0 + 130), "0 discs", font=font(31), fill=(255, 90, 80))

    # --- P3: the slideshow -----------------------------------------------------
    x0, y0 = boxes[2]
    win = [x0 + 28, y0 + 20, x0 + pw - 28, y0 + ph - 20]
    d.rounded_rectangle(win, radius=10, fill=(246, 246, 249),
                        outline=(110, 110, 130), width=2)
    d.rectangle([win[0], win[1], win[2], win[1] + 28], fill=(222, 224, 230))
    for i, c in enumerate(((232, 80, 70), (240, 190, 60), (90, 190, 90))):
        d.ellipse([win[0] + 12 + i * 22, win[1] + 8, win[0] + 24 + i * 22,
                   win[1] + 20], fill=c)
    d.rounded_rectangle([win[2] - 52, win[1] + 3, win[2] - 28, win[1] + 25],
                        radius=5, fill=(230, 110, 30))
    d.text((win[2] - 40, win[1] + 4), "P", font=font(17), fill=WHITE,
           anchor="ma")
    ctext(d, x0 + pw // 2, y0 + 62, "30 FPS", 60, (30, 30, 40))
    ctext(d, x0 + pw // 2, y0 + 140, "PS5 Pro edition", 23, (110, 110, 125))
    d.text((win[0] + 16, win[3] - 30), "performance_mode.pptx", font=font(19),
           fill=(140, 140, 155))
    s = "1/1"
    d.text((win[2] - 16 - tw(d, s, 21), win[3] - 30), s, font=font(21),
           fill=(110, 110, 125))

    # --- P4: the sick note ------------------------------------------------------
    x0, y0 = boxes[3]
    paper = [x0 + 94, y0 + 16, x0 + 484, y0 + 212]
    d.rounded_rectangle(paper, radius=8, fill=(250, 249, 244),
                        outline=(160, 158, 148), width=2)
    for ly in range(paper[1] + 66, paper[3] - 10, 34):
        d.line([(paper[0] + 10, ly), (paper[2] - 10, ly)],
               fill=(196, 210, 232), width=1)
    d.line([(paper[0] + 36, paper[1] + 8), (paper[0] + 36, paper[3] - 8)],
           fill=(238, 160, 160), width=2)
    for tx0 in (paper[0] - 8, paper[2] - 62):
        d.rectangle([tx0, paper[1] - 8, tx0 + 70, paper[1] + 14],
                    fill=(238, 222, 140), outline=(200, 182, 100), width=1)
    nx = paper[0] + 52
    d.text((nx, paper[1] + 16), "Dear boss,", font=font(25), fill=INK)
    s1 = "I have the GTA flu"
    d.text((nx, paper[1] + 56), s1, font=font(27), fill=INK)
    em = emoji_tile("\U0001F912", 30)
    img.paste(em, (int(nx + tw(d, s1, 27) + 8), paper[1] + 56), em)
    d = ImageDraw.Draw(img)
    d.text((nx, paper[1] + 100), "back Monday (maybe)", font=font(25), fill=INK)
    d.text((nx, paper[1] + 142), "— the entire office", font=font(22),
           fill=(110, 105, 95))

    # --- Bottom strip: the agent ------------------------------------------------
    sy = top + 2 * ph + gap + 14
    d.rectangle([0, sy, W, H], fill=(8, 5, 14))
    d.line([(0, sy), (W, sy)], fill=PINK, width=3)
    paste_ghost(img, 74, (sy + H) // 2, 104)
    d = ImageDraw.Draw(img)
    bag = money_bag_tile(92)
    img.paste(bag, (140, H - 10 - bag.height), bag)
    d = ImageDraw.Draw(img)
    tx = 252
    d.text((tx, sy + 18), "MY AGENT'S LAUNCH DAY: NO DOWNLOAD. NO QUEUE.",
           font=font(29), fill=WHITE)
    y2 = sy + 62
    d.text((tx, y2), "JUST BOUNTIES ON ", font=font(29), fill=WHITE)
    d.text((tx + tw(d, "JUST BOUNTIES ON ", 29), y2), "make.fun",
           font=font(29), fill=PINK)

    out = os.path.join(HERE, "meme7.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build_e()
    build_f()
