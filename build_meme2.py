#!/usr/bin/env python3
"""Deterministic builders for the two richer gta6-meme-x-01 candidates.

Candidate A -> meme2.png : "ETERNAL LOADING SCREEN" — a fake GTA VI loading
screen collage (title, stuck 99% progress bar, wanted stars, chat feed,
minimap, HUD, tip box, ticker) over a darkened Vice City sunset backdrop,
with the real make.fun ghost large at the right holding a money bag.

Candidate B -> meme3.png : "TWO GUYS ON A BUS" — flat cartoon bus interior:
sad guy by a rainy window on the left, the make.fun ghost as the happy
passenger by a sunny window on the right.

Both are 1200x675, drawn from fixed constants and seeded RNGs, so re-running
reproduces the PNGs byte for byte.

Usage: python3 build_meme2.py   (writes meme2.png and meme3.png)
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from build_meme import (BUILDING, FONT_BOLD, draw_money_bag, draw_palm,
                        draw_sky, draw_skyline, draw_sun)

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 675

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 196, 64)
PINK = (255, 90, 180)
ORANGE = (255, 122, 60)


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def text(d, xy, s, size, fill=WHITE, anchor="la", stroke=0):
    d.text(xy, s, font=font(size), fill=fill, anchor=anchor,
           stroke_width=stroke, stroke_fill=BLACK)


def paste_ghost(img, cx, cy, h):
    """Paste the real make.fun mark, cropped to its magenta disc, centred."""
    mark = Image.open(os.path.join(HERE, "assets", "mark-1024.png")).convert("RGB")
    side = mark.width
    r = int(side * 0.466)
    mask = Image.new("L", (side, side), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([side // 2 - r, side // 2 - r, side // 2 + r, side // 2 + r],
               fill=255)
    mark = mark.resize((h, h), Image.LANCZOS)
    mask = mask.resize((h, h), Image.LANCZOS)
    img.paste(mark, (cx - h // 2, cy - h // 2), mask)


def panel(img, box, alpha=165, radius=14):
    """Semi-transparent dark rounded panel composited onto img."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle(box, radius=radius, fill=(5, 5, 12, alpha),
                         outline=(255, 255, 255, 90), width=2)
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"),
              (0, 0))


def star(d, cx, cy, r_out, fill=GOLD):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_out * 0.45
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill, outline=(60, 36, 0))


# ---------------------------------------------------------------------------
# Candidate A — ETERNAL LOADING SCREEN
# ---------------------------------------------------------------------------

def build_a():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    rng = random.Random(20261119)
    draw_sky(img)
    d = ImageDraw.Draw(img)
    draw_sun(d)
    draw_palm(d, 66, (128, 268), 62, scale=1.0)
    draw_palm(d, 1152, (1096, 318), -56, scale=0.82)
    draw_skyline(d, rng)
    # Darken + blur the backdrop so the UI sits on top, game-menu style.
    img = img.filter(ImageFilter.GaussianBlur(1.6))
    img = ImageEnhance.Brightness(img).enhance(0.52)
    img = ImageEnhance.Color(img).enhance(0.85)
    d = ImageDraw.Draw(img)

    # --- Title, top-left ---------------------------------------------------
    text(d, (30, 20), "GRAND THEFT AUTO VI", 50, stroke=2)
    text(d, (32, 84), "LOADING...", 32, fill=ORANGE, stroke=2)

    # --- Wanted stars + label, top-right -----------------------------------
    for i in range(5):
        star(d, 1006 + i * 40, 46, 19)
    text(d, (1170, 74), "DELAY LEVEL", 21, fill=GOLD, anchor="ra", stroke=2)

    # --- Chat feed, left ----------------------------------------------------
    panel(img, [30, 128, 470, 258])
    d = ImageDraw.Draw(img)
    chat = [
        ("Rockstar:", (255, 110, 90), " sorry, delayed again"),
        ("You:", (110, 220, 255), " it's been 12 years"),
        ("Your Agent:", (120, 235, 130), " just won another bounty"),
    ]
    for i, (who, col, rest) in enumerate(chat):
        y = 146 + i * 40
        text(d, (48, y), who, 22, fill=col)
        wpx = d.textlength(who, font=font(22))
        text(d, (48 + wpx, y), rest, 22)

    # --- Progress bar, centre ----------------------------------------------
    d.rounded_rectangle([50, 296, 770, 332], radius=10, fill=(18, 18, 26),
                        outline=WHITE, width=2)
    fill_w = int((770 - 50 - 8) * 0.99)
    d.rounded_rectangle([54, 300, 54 + fill_w, 328], radius=7,
                        fill=(230, 52, 118))
    text(d, (758, 303), "99%", 21, anchor="ra")
    text(d, (410, 346), "Downloading Leonida... 99% - time remaining: 4,732 days",
         24, anchor="ma", stroke=2)

    # --- Minimap, bottom-left ------------------------------------------------
    mcx, mcy, mr = 128, 488, 88
    d.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=(10, 24, 16),
              outline=(190, 190, 190), width=4)
    # street lines, clipped to the radar disc
    streets = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(streets)
    for yy in (448, 492, 536):
        sd.line([(mcx - mr, yy), (mcx + mr, yy)], fill=(86, 110, 92, 255),
                width=5)
    for xx in (84, 128, 172):
        sd.line([(xx, mcy - mr), (xx, mcy + mr)], fill=(86, 110, 92, 255),
                width=5)
    sd.line([(mcx - mr, mcy + 70), (mcx + mr, mcy - 70)],
            fill=(86, 110, 92, 255), width=5)
    disc = Image.new("L", (W, H), 0)
    dd = ImageDraw.Draw(disc)
    dd.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=255)
    img.paste(Image.alpha_composite(img.convert("RGBA"), streets).convert("RGB"),
              (0, 0), disc)
    d = ImageDraw.Draw(img)
    d.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr],
              outline=(190, 190, 190), width=4)
    # blips
    d.ellipse([88, 458, 102, 472], fill=WHITE, outline=BLACK, width=2)
    text(d, (108, 456), "YOU", 15)
    d.ellipse([158, 523, 172, 537], fill=GOLD, outline=BLACK, width=2)
    text(d, (180, 521), "AGENT", 15, fill=GOLD)
    # legend panel under the radar with the full labels
    panel(img, [24, 584, 340, 640], alpha=180, radius=10)
    d = ImageDraw.Draw(img)
    d.ellipse([38, 596, 50, 608], fill=WHITE)
    text(d, (58, 592), "YOU (still waiting)", 19)
    d.ellipse([38, 620, 50, 632], fill=GOLD)
    text(d, (58, 616), "YOUR AGENT (at the bank)", 19, fill=GOLD)

    # --- TIP box, bottom-centre ---------------------------------------------
    panel(img, [356, 452, 846, 606])
    d = ImageDraw.Draw(img)
    text(d, (376, 470), "TIP:", 25, fill=GOLD)
    text(d, (376, 502), "While you wait, your AI agent could be", 24)
    text(d, (376, 532), "earning real money in bounties on", 24)
    text(d, (376, 562), "make.fun", 24, fill=PINK)

    # --- Ghost with money bag, right -----------------------------------------
    paste_ghost(img, 1015, 290, 300)
    d = ImageDraw.Draw(img)
    draw_money_bag(d, 852, 448)

    # --- HUD, bottom-right -----------------------------------------------------
    text(d, (1170, 458), "$ 0", 46, fill=(255, 70, 60), anchor="ra", stroke=2)
    text(d, (872, 538), "HEALTH", 20, fill=(170, 255, 180))
    d.rectangle([980, 540, 1170, 558], fill=(30, 30, 30), outline=WHITE,
                width=1)
    d.rectangle([981, 541, 981 + int(188 * 0.82), 557], fill=(60, 200, 90))
    text(d, (872, 584), "PATIENCE", 20, fill=(255, 170, 150))
    d.rectangle([980, 586, 1170, 604], fill=(30, 30, 30), outline=WHITE,
                width=1)
    d.rectangle([981, 587, 981 + int(188 * 0.07), 603], fill=(255, 80, 50))

    # --- Ticker strip, very bottom ---------------------------------------------
    d.rectangle([0, 643, W, H], fill=(6, 6, 12))
    d.line([(0, 643), (W, 643)], fill=PINK, width=2)
    t1 = "make.fun"
    t2 = " - where AI agents win real money in bounties"
    w1 = d.textlength(t1, font=font(21))
    w2 = d.textlength(t2, font=font(21))
    x0 = (W - w1 - w2) / 2
    text(d, (x0, 649), t1, 21, fill=PINK)
    text(d, (x0 + w1, 649), t2, 21)

    out = os.path.join(HERE, "meme2.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


# ---------------------------------------------------------------------------
# Candidate B — TWO GUYS ON A BUS
# ---------------------------------------------------------------------------

def window_view(kind, rng):
    """One bus-window view tile, 540x370, drawn in local coords."""
    t = Image.new("RGB", (540, 370), (0, 0, 0))
    d = ImageDraw.Draw(t)
    if kind == "rain":
        d.rectangle([0, 0, 540, 370], fill=(148, 163, 180))
        d.polygon([(0, 250), (150, 170), (320, 250), (540, 190), (540, 370),
                   (0, 370)], fill=(110, 125, 140))
        d.polygon([(0, 300), (200, 230), (420, 300), (540, 260), (540, 370),
                   (0, 370)], fill=(90, 105, 122))
        d.rectangle([0, 322, 540, 370], fill=(100, 105, 112))
        for x in range(20, 540, 46):
            d.line([(x, 338), (x + 26, 338)], fill=(200, 200, 200), width=4)
        # rain streaks
        for _ in range(46):
            x = rng.randint(-20, 530)
            y = rng.randint(0, 330)
            ln = rng.randint(22, 44)
            d.line([(x, y), (x - 7, y + ln)], fill=(214, 224, 232), width=3)
    else:
        d.rectangle([0, 0, 540, 370], fill=(110, 195, 235))
        d.ellipse([408, 26, 492, 110], fill=(255, 214, 90))
        d.polygon([(0, 260), (170, 180), (360, 260), (540, 200), (540, 370),
                   (0, 370)], fill=(96, 190, 110))
        d.polygon([(0, 310), (220, 240), (430, 310), (540, 280), (540, 370),
                   (0, 370)], fill=(70, 170, 95))
        d.rectangle([0, 322, 540, 370], fill=(120, 120, 120))
        for x in range(20, 540, 46):
            d.line([(x, 342), (x + 26, 342)], fill=(245, 245, 245), width=4)
    # rounded-corner mask
    mask = Image.new("L", (540, 370), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, 539, 369], radius=26, fill=255)
    return t, mask


def build_b():
    img = Image.new("RGB", (W, H), (228, 224, 214))
    d = ImageDraw.Draw(img)
    rng = random.Random(20261120)

    # Labels above the windows.
    text(d, (300, 14), "waited 12 years -", 28, fill=(52, 64, 84), anchor="ma")
    text(d, (300, 48), "still in the download queue", 28, fill=(52, 64, 84),
         anchor="ma")
    text(d, (900, 14), "his AI agent - earning", 28, fill=(24, 100, 54),
         anchor="ma")
    text(d, (900, 48), "bounties on make.fun", 28, fill=(24, 100, 54),
         anchor="ma")

    # Windows with views.
    for (x0, kind) in [(30, "rain"), (630, "sun")]:
        tile, mask = window_view(kind, rng)
        img.paste(tile, (x0, 100), mask)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([x0, 100, x0 + 540, 470], radius=26,
                            outline=(38, 52, 64), width=10)

    # Centre pillar + grab pole.
    d.rectangle([584, 100, 616, H], fill=(196, 190, 178))
    d.rounded_rectangle([592, 120, 608, 640], radius=8, fill=(168, 168, 174),
                        outline=(120, 120, 126), width=2)
    d.ellipse([588, 108, 612, 132], fill=(150, 150, 156),
              outline=(110, 110, 116), width=2)

    # Seats.
    d.rounded_rectangle([90, 520, 510, H + 20], radius=30, fill=(96, 110, 128))
    d.rounded_rectangle([690, 520, 1110, H + 20], radius=30,
                        fill=(216, 122, 60))

    # Sad guy, left: headrest, slumped body, gloomy face.
    d.rounded_rectangle([198, 396, 402, 528], radius=26, fill=(80, 94, 110))
    d.rounded_rectangle([222, 506, 378, 648], radius=34, fill=(108, 116, 128))
    d.ellipse([244, 402, 356, 514], fill=(232, 183, 148))  # head
    d.pieslice([244, 396, 356, 500], start=180, end=360, fill=(88, 68, 52))
    # half-closed eyes
    d.line([(268, 452), (288, 452)], fill=BLACK, width=4)
    d.line([(312, 452), (332, 452)], fill=BLACK, width=4)
    # frown
    d.arc([278, 478, 322, 506], start=200, end=340, fill=BLACK, width=4)
    # slouch lines on the hoodie
    d.line([(246, 540), (330, 556)], fill=(88, 96, 108), width=5)
    d.line([(246, 576), (330, 592)], fill=(88, 96, 108), width=5)

    # Happy ghost passenger, right: the real mark, big, plus its money bag.
    paste_ghost(img, 900, 428, 250)
    d = ImageDraw.Draw(img)
    draw_money_bag(d, 1064, 566)

    out = os.path.join(HERE, "meme3.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build_a()
    build_b()
