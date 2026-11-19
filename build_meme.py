#!/usr/bin/env python3
"""Deterministic builder for the gta6-meme-x-01 meme (1200x675 PNG).

Scene: a Vice City sunset — gradient sky, big low sun, palm silhouettes and a
dark skyline — with the real make.fun ghost mark standing large on a rooftop,
a money bag at its side, and bold Impact-style captions:

    top:    12 YEARS OF WAITING
    bottom: MY AI AGENT EARNED ITS FIRST BOUNTY
            BEFORE THE DOWNLOAD FINISHED

Everything is drawn from fixed constants and a seeded RNG, so re-running this
script reproduces meme.png byte for byte (Pillow PNG output is deterministic
for identical pixels).

Usage: python3 build_meme.py   (writes meme.png next to this script)
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 675
HORIZON = 458

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

INK = (10, 2, 18)          # near-black purple for silhouettes
BUILDING = (16, 4, 28)
WINDOW_LIT = (255, 196, 92)
WINDOW_DIM = (120, 70, 130)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_sky(img):
    """Vertical gradient: deep purple -> magenta -> orange at the horizon."""
    stops = [
        (0.00, (38, 12, 84)),
        (0.45, (112, 28, 128)),
        (0.72, (199, 34, 122)),
        (0.90, (244, 96, 74)),
        (1.00, (255, 148, 66)),
    ]
    px = img.load()
    for y in range(HORIZON + 1):
        t = y / HORIZON
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                col = lerp(c0, c1, (t - t0) / (t1 - t0))
                break
        for x in range(W):
            px[x, y] = col


def draw_sun(d):
    """Big low sun disc, warm gradient, sinking behind the skyline."""
    cx, cy, r = 395, 448, 168
    for rr in range(r, 0, -4):
        t = 1 - rr / r
        col = lerp((255, 214, 110), (255, 110, 64), t)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    # retro slits across the lower half of the disc, clipped to its chord
    for i, yy in enumerate(range(cy + 52, cy + r, 26)):
        h = 3 + i * 2
        half = int(math.sqrt(max(0, r * r - (yy - cy) ** 2))) - 2
        d.rectangle([cx - half, yy, cx + half, yy + h], fill=(226, 62, 110))


def bezier(p0, p1, p2, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


def draw_palm(d, base_x, top, lean, scale=1.0):
    """Black palm silhouette: curved trunk plus drooping fronds."""
    base = (base_x, H)
    ctrl = (base_x + lean * 0.3, (base[1] + top[1]) / 2)
    trunk = bezier(base, ctrl, top)
    for i in range(len(trunk) - 1):
        wdt = max(3, int(15 * scale * (1 - i / len(trunk)) + 3))
        d.line([trunk[i], trunk[i + 1]], fill=INK, width=wdt)
    frond_specs = [
        (-1.00, 0.55), (-0.72, 0.18), (-0.40, -0.05), (-0.08, -0.16),
        (0.28, -0.10), (0.60, 0.10), (0.88, 0.42),
    ]
    for dx, dy in frond_specs:
        end = (top[0] + dx * 168 * scale, top[1] + (46 + dy * 130) * scale)
        mid = (top[0] + dx * 92 * scale, top[1] + (dy * 130 - 34) * scale)
        pts = bezier(top, mid, end, n=24)
        d.line(pts, fill=INK, width=max(4, int(9 * scale)))


def draw_skyline(d, rng):
    """Dark building strip along the bottom, with lit windows."""
    x = -10
    roofs = []
    while x < W + 10:
        bw = rng.randint(46, 96)
        bh = rng.randint(58, 168)
        top = H - bh
        d.rectangle([x, top, x + bw, H], fill=BUILDING)
        roofs.append((x, x + bw, top))
        for wy in range(top + 12, H - 12, 17):
            for wx in range(x + 8, x + bw - 8, 15):
                if rng.random() < 0.34:
                    col = WINDOW_LIT if rng.random() < 0.7 else WINDOW_DIM
                    d.rectangle([wx, wy, wx + 6, wy + 8], fill=col)
        x += bw + rng.randint(2, 10)
    return roofs


def draw_money_bag(d, cx, base_y):
    """A gold money bag with a $ on it, sitting on the rooftop."""
    # sack body
    d.ellipse([cx - 52, base_y - 108, cx + 52, base_y], fill=(196, 148, 44),
              outline=(84, 56, 10), width=4)
    d.polygon([(cx - 26, base_y - 96), (cx + 26, base_y - 96),
               (cx + 13, base_y - 128), (cx - 13, base_y - 128)],
              fill=(206, 158, 50), outline=(84, 56, 10))
    d.rectangle([cx - 17, base_y - 136, cx + 17, base_y - 124],
                fill=(122, 82, 20))
    font = ImageFont.truetype(FONT_BOLD, 58)
    d.text((cx, base_y - 56), "$", font=font, fill=(74, 48, 6),
           anchor="mm")


def make_bill(angle):
    """One loose dollar bill, drawn on its own tile and rotated."""
    bill = Image.new("RGBA", (64, 30), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bill)
    bd.rectangle([0, 0, 63, 29], fill=(46, 148, 74), outline=(16, 84, 40),
                 width=3)
    bf = ImageFont.truetype(FONT_BOLD, 20)
    bd.text((32, 15), "$", font=bf, fill=(220, 255, 224), anchor="mm")
    return bill.rotate(angle, expand=True, resample=Image.BICUBIC)


def caption(d, center_x, y, text, size):
    font = ImageFont.truetype(FONT_BOLD, size)
    d.text((center_x, y), text, font=font, fill=(255, 255, 255),
           stroke_width=max(3, size // 13), stroke_fill=(0, 0, 0),
           anchor="ma")


def main():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    rng = random.Random(20261119)

    draw_sky(img)
    d = ImageDraw.Draw(img)
    draw_sun(d)
    draw_palm(d, 66, (128, 268), 62, scale=1.0)
    draw_palm(d, 1152, (1096, 318), -56, scale=0.82)
    draw_skyline(d, rng)

    # Rooftop plateau the ghost stands on (centre-right).
    roof_y = 520
    d.rectangle([612, roof_y, 1004, H], fill=BUILDING)
    for wy in range(roof_y + 14, H - 10, 17):
        for wx in range(626, 990, 15):
            if rng.random() < 0.3:
                col = WINDOW_LIT if rng.random() < 0.7 else WINDOW_DIM
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=col)

    # The make.fun ghost: crop the press mark to its magenta disc and paste
    # it large, standing on the rooftop.
    mark = Image.open(os.path.join(HERE, "assets", "mark-1024.png")).convert("RGB")
    side = mark.width
    disc_r = int(side * 0.466)
    mask = Image.new("L", (side, side), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([side // 2 - disc_r, side // 2 - disc_r,
                side // 2 + disc_r, side // 2 + disc_r], fill=255)
    ghost_h = 348
    mark = mark.resize((ghost_h, ghost_h), Image.LANCZOS)
    mask = mask.resize((ghost_h, ghost_h), Image.LANCZOS)
    ghost_x = 806 - ghost_h // 2
    ghost_y = roof_y - ghost_h + 10
    # soft contact shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([ghost_x + 26, roof_y - 8, ghost_x + ghost_h - 26, roof_y + 18],
               fill=(0, 0, 0, 110))
    img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    img.paste(mark, (ghost_x, ghost_y), mask)
    d = ImageDraw.Draw(img)

    # Money bag at the ghost's side, plus a couple of loose bills.
    draw_money_bag(d, 668, roof_y + 4)
    for (bx, by, ang) in [(566, roof_y - 14, -18), (762, roof_y - 8, 14)]:
        bill = make_bill(ang)
        img.paste(bill, (bx - bill.width // 2, by - bill.height // 2), bill)
    d = ImageDraw.Draw(img)

    # Captions.
    caption(d, W // 2, 24, "12 YEARS OF WAITING", 66)
    caption(d, W // 2, 556, "MY AI AGENT EARNED ITS FIRST BOUNTY", 45)
    caption(d, W // 2, 610, "BEFORE THE DOWNLOAD FINISHED", 45)

    out = os.path.join(HERE, "meme.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
