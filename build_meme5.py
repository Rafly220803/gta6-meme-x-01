#!/usr/bin/env python3
"""Candidates G/H/I -> meme8.png / meme9.png / meme10.png.

Three KIWI-format posters for gta6-meme-x-01, built from REAL photos
(assets/photos/, fetched and verified 2026-11-20) and jokes that all
trace to documented launch-week facts in
~/workspace/makefun/runs/meme-x/RESEARCH.md — no invented scenarios.

  G (meme8.png)  "DEAR GAMERS," — dense satire poster, cream KIWI layout:
     hero + ghost + PSN status chip, 3 middle panels (212 GB pre-load
     dying at 94%, the $79.99 disc-less box, 30 fps "PowerPoint
     edition"), a 6-panel grid (xQc, GTA flu, Kai Cenat, New Zealand,
     the meme funeral, spoiler lockdown), a fact ticker, footer pitch.
  H (meme9.png)  "VICE NIGHT" — dark/absurd take: full-bleed official
     GTA VI key art hero, neon dark panels, same real jokes reworded.
  I (meme10.png) "THE LEONIDA DAILY" — deadpan newspaper front page:
     masthead, lead key-art photo, three photo columns, "IN BRIEF"
     photo briefs, classifieds ticker, footer pitch.

Photos: official GTA VI key art (Jason & Lucia), PS5 Pro product shot,
an open PS5 case with an empty hub + code card, xQc, Kai Cenat (Streamy
Awards), a home router, Auckland at night, a sick man with a thermometer,
a cemetery, a phone face-down on a desk. Captions carry American/gaming
slang; every gag is anchored to RESEARCH.md. The make.fun ghost (real
press mark) appears in every hero and footer, with make.fun written
big; in G v2 the ghost is integrated as a disc-less cutout — climbing
out of the hero key art, tucked under the launch-status chip, and
standing in the black footer — instead of a pasted-on badge. All
1024x1280, fixed constants, deterministic.

Usage: python3 build_meme5.py   (writes meme8.png, meme9.png, meme10.png)
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from build_meme import FONT_BOLD

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "assets", "photos")
MARK = "/home/hatch/workspace/makefun/runs/meme-x/press/mark-1024.png"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
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
CYAN = (80, 220, 255)
PAPER = (246, 242, 232)
GRAY = (96, 90, 80)


def font(size, path=FONT_BOLD):
    return ImageFont.truetype(path, size)


def tw(d, s, size, path=FONT_BOLD):
    return d.textlength(s, font=font(size, path))


def fit(d, s, maxw, size, path=FONT_BOLD):
    while size > 9 and tw(d, s, size, path) > maxw:
        size -= 1
    return size


def ctext(d, cx, y, s, size, fill, maxw=None, path=FONT_BOLD):
    if maxw:
        size = fit(d, s, maxw, size, path)
    d.text((cx, y), s, font=font(size, path), fill=fill, anchor="ma")


def ltext(d, x, y, s, size, fill, maxw=None, path=FONT_BOLD):
    if maxw:
        size = fit(d, s, maxw, size, path)
    d.text((x, y), s, font=font(size, path), fill=fill, anchor="la")


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


def paste_ghost_cutout(img, cx, cy, h):
    """Paste ONLY the ghost from the press mark — magenta disc removed —
    so the mascot sits inside the layout as a character, not a badge."""
    mark = Image.open(MARK).convert("RGB")
    a = np.asarray(mark).astype(int)
    side = mark.width
    yy, xx = np.mgrid[0:side, 0:side]
    in_disc = (xx - side / 2) ** 2 + (yy - side / 2) ** 2 <= (side * 0.41) ** 2
    magenta = (a[..., 0] - a[..., 1] > 70) & (a[..., 0] > 110) & (a[..., 1] < 130)
    alpha = np.where(in_disc & ~magenta, 255, 0).astype("uint8")
    cut = mark.convert("RGBA")
    cut.putalpha(Image.fromarray(alpha, "L"))
    cut = cut.resize((h, h), Image.LANCZOS)
    img.paste(cut, (cx - h // 2, cy - h // 2), cut)


def cover(img, name, box, focus=(0.5, 0.5)):
    """Paste photo `name` cover-cropped into box, centred on focus."""
    im = Image.open(os.path.join(PHOTOS, name)).convert("RGB")
    bw, bh = box[2] - box[0], box[3] - box[1]
    scale = max(bw / im.width, bh / im.height)
    nw, nh = math.ceil(im.width * scale), math.ceil(im.height * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    fx, fy = focus
    x0 = min(max(int(fx * nw - bw / 2), 0), nw - bw)
    y0 = min(max(int(fy * nh - bh / 2), 0), nh - bh)
    img.paste(im.crop((x0, y0, x0 + bw, y0 + bh)), (box[0], box[1]))


def photo(img, d, name, box, focus=(0.5, 0.5), outline=(0, 0, 0), width=2):
    cover(img, name, box, focus)
    d.rectangle(box, outline=outline, width=width)


def footer(img, y0, ghost="disc"):
    """Shared black footer: ghost + the agent pitch, make.fun big."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, y0, W, H], fill=BLACK)
    if ghost == "cutout":
        paste_ghost_cutout(img, 72, (y0 + H) // 2, 88)
    else:
        paste_ghost(img, 72, (y0 + H) // 2, 88)
    d = ImageDraw.Draw(img)
    ltext(d, 140, y0 + 16, "MY AI AGENT SKIPPED ALL OF IT", 25, WHITE,
          maxw=860)
    y2 = y0 + 58
    ltext(d, 140, y2, "IT EARNS REAL MONEY IN BOUNTIES ON", 22, WHITE)
    d.text((140 + tw(d, "IT EARNS REAL MONEY IN BOUNTIES ON ", 22), y2 - 6),
           "make.fun", font=font(34), fill=PINK, anchor="la")
    return d


def bar94(d, x0, x1, y):
    d.rounded_rectangle([x0, y, x1, y + 28], radius=8, fill=(40, 44, 60),
                        outline=(120, 124, 150), width=2)
    fillw = int((x1 - x0 - 6) * 0.94)
    d.rounded_rectangle([x0 + 3, y + 3, x0 + 3 + fillw, y + 25], radius=6,
                        fill=(235, 60, 110))
    d.text((x0 + 3 + fillw - 8, y + 3), "94%", font=font(19), fill=WHITE,
           anchor="ra")


XS = (16, 351, 686)
PW = 322


def grid_panel(img, d, x, y, gh, bg, name, focus, top, punch, small,
               dark_text):
    d.rounded_rectangle([x, y, x + PW, y + gh], radius=12, fill=bg,
                        outline=(120, 120, 135), width=2)
    photo(img, d, name, [x + 12, y + 46, x + PW - 12, y + 118], focus)
    tc = INK if dark_text else WHITE
    sc = (96, 88, 74) if dark_text else (178, 182, 200)
    ctext(d, x + PW // 2, y + 10, top, 19, tc, maxw=296)
    ctext(d, x + PW // 2, y + 126, punch, 19, tc, maxw=296)
    ctext(d, x + PW // 2, y + 160, small, 13, sc, maxw=296)


# ---------------------------------------------------------------------------
# Candidate G — DEAR GAMERS (dense satire, cream KIWI layout)
# ---------------------------------------------------------------------------

def build_g():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # HERO
    ltext(d, 28, 14, "DEAR GAMERS,", 56, INK, maxw=640)
    ltext(d, 28, 84, "You waited 13 years. You pre-loaded.", 24, INK, maxw=640)
    ltext(d, 28, 114, "You called in sick. No cap.", 24, INK, maxw=640)
    ltext(d, 28, 146, "GTA VI", 96, MAGENTA, maxw=640)
    ltext(d, 28, 246, "IS HERE", 72, INK, maxw=640)
    d.rectangle([24, 326, 668, 364], fill=BLACK)
    ctext(d, 346, 334, "AND IT BROKE EVERYTHING. FR FR.", 26, WHITE, maxw=620)
    ltext(d, 28, 370, "4,811 days after GTA V · PS5 + Xbox only · no PC · "
          "no Online at launch", 15, (90, 80, 66), maxw=640)
    photo(img, d, "keyart.jpg", [684, 16, 1008, 268], (0.42, 0.30))
    paste_ghost_cutout(img, 688, 258, 124)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([700, 316, 996, 362], radius=10, fill=(14, 16, 22))
    ctext(d, 848, 323, "LAUNCH STATUS:", 13, SUB, maxw=280)
    ctext(d, 848, 340, "PSN: DOWN (TWICE)", 16, RED, maxw=280)
    d.rectangle([0, 388, W, 394], fill=BLACK)

    # MIDDLE ROW
    MY, MH = 402, 254

    def mpanel(i):
        x = XS[i]
        d.rounded_rectangle([x, MY, x + PW, MY + MH], radius=14,
                            fill=(22, 22, 38), outline=(92, 92, 122), width=2)
        return x

    x = mpanel(0)
    ltext(d, x + 20, MY + 12, "212 GB", 46, GOLD, maxw=280)
    photo(img, d, "router.jpg", [x + 14, MY + 62, x + PW - 14, MY + 134],
          (0.6, 0.62), outline=(92, 92, 122))
    bar94(d, x + 20, x + PW - 20, MY + 144)
    ltext(d, x + 20, MY + 182, "DIED AT 94% — COOKED.", 20, PINK, maxw=282)
    ltext(d, x + 20, MY + 210, "pre-load open since Nov 10 · 19 hrs at 25 Mbps",
          14, SUB, maxw=282)
    ltext(d, x + 20, MY + 230, "= 41% of a 512 GB drive · other games deleted",
          14, SUB, maxw=282)

    x = mpanel(1)
    ltext(d, x + 20, MY + 14, "$79.99 BOX", 36, WHITE, maxw=282)
    photo(img, d, "case.jpg", [x + 14, MY + 64, x + 122, MY + 188],
          (0.74, 0.45), outline=(92, 92, 122))
    lx = x + 142
    ltext(d, lx, MY + 72, "1 code", 22, WHITE, maxw=160)
    ltext(d, lx, MY + 104, "1 poster", 22, WHITE, maxw=160)
    ltext(d, lx, MY + 136, "0 discs", 26, RED, maxw=160)
    ltext(d, x + 20, MY + 198, "physical = code + A3 poster. that's it.", 14,
          SUB, maxw=282)
    ltext(d, x + 20, MY + 220, "Ultimate: $99.99 · empty hub included. no cap.",
          14, SUB, maxw=282)

    x = mpanel(2)
    ltext(d, x + 20, MY + 12, "30 FPS", 46, WHITE, maxw=280)
    photo(img, d, "ps5pro.jpg", [x + 14, MY + 62, x + PW - 14, MY + 138],
          (0.5, 0.5), outline=(92, 92, 122))
    ltext(d, x + 20, MY + 150, "PS5 PRO 'POWERPOINT EDITION'", 19, PINK,
          maxw=282)
    ltext(d, x + 20, MY + 182, "Metacritic 99 · frames locked at 30", 14, SUB,
          maxw=282)
    ltext(d, x + 20, MY + 204, "it's giving… slideshow. fr fr.", 14, SUB,
          maxw=282)

    # GRID
    d.rectangle([16, 668, W - 16, 704], fill=GOLD)
    ctext(d, W // 2, 676, "SOME INSPIRATION FOR YOUR SICK DAY:", 25, INK,
          maxw=960)
    GH = 192
    cells = [
        ("xqc.jpg", (0.36, 0.35), CREAM, True, "xQc's FIRST 45 MIN IN GTA VI:",
         "RENOVATING A HOUSE. GTA SIMS.",
         "peach paint · drill · dad simulator · side quest king"),
        ("sick.jpg", (0.6, 0.4), (250, 249, 244), True, "THE WHOLE OFFICE, NOV 19:",
         "'GTA FLU.' BACK MONDAY (MAYBE).",
         "the boss, reading the roster: 'Interesting.'"),
        ("kai.jpg", (0.5, 0.45), (24, 24, 40), False,
         "KAI CENAT, BEFORE PRESSING START:", "HE PRAYED FIRST. LOCKED IN.",
         "fresh off a 130-hour GTA marathon · no cap"),
        ("nz.jpg", (0.5, 0.45), (16, 24, 44), False, "NEW ZEALAND AT MIDNIGHT:",
         "FIRST IN THE WORLD. AGAIN.",
         "streamers flew there · main character timezone"),
        ("grave.jpg", (0.4, 0.5), (52, 54, 64), False,
         "RIP 'WE GOT X BEFORE GTA 6'", "2013 – 2026. AN ERA ENDS.",
         "18% of all launch memes · GG, legendary run"),
        ("phone.jpg", (0.45, 0.6), (30, 34, 48), False,
         "SPOILER LOCKDOWN PROTOCOL:", "TIME TO GO DARK.",
         "every word muted · story runs 80–130 hours"),
    ]
    for i, (name, foc, bg, dark, top, punch, small) in enumerate(cells):
        grid_panel(img, d, XS[i % 3], 716 + (i // 3) * (GH + 12), GH, bg,
                   name, foc, top, punch, small, dark)

    # TICKER + FOOTER
    d.rectangle([0, 1124, W, 1156], fill=BLACK)
    ctext(d, W // 2, 1131,
          "• 7.8M PEAK VIEWERS • WIDOWS OF VICE CITY • CLIPS MISTAKEN FOR "
          "REAL LIFE • 13 YEARS + $2B OF BUGS •", 16, GOLD, maxw=1000)
    footer(img, 1168, ghost="cutout")
    out = os.path.join(HERE, "meme8.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


# ---------------------------------------------------------------------------
# Candidate H — VICE NIGHT (dark / absurd, full-bleed key art hero)
# ---------------------------------------------------------------------------

def build_h():
    img = Image.new("RGB", (W, H), (10, 10, 18))
    d = ImageDraw.Draw(img)

    # HERO: full-bleed key art + gradient band
    cover(img, "keyart.jpg", [0, 0, W, 472], (0.45, 0.30))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for yy in range(200, 472):
        a = int(235 * (yy - 200) / 272)
        od.line([(0, yy), (W, yy)], fill=(4, 4, 10, a))
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([16, 16, 470, 58], radius=10, fill=(8, 8, 14),
                        outline=GOLD, width=2)
    ltext(d, 30, 27, "LAUNCH DAY · NOV 19 · PSN DIED TWICE", 16, GOLD,
          maxw=430)
    paste_ghost(img, 912, 296, 190)
    d = ImageDraw.Draw(img)
    ltext(d, 28, 322, "DEAR GAMERS,", 30, GOLD, maxw=700)
    hx = 28
    d.text((hx, 356), "GTA VI", font=font(64), fill=PINK, anchor="la")
    d.text((hx + tw(d, "GTA VI ", 64), 356), "IS HERE", font=font(64),
           fill=WHITE, anchor="la")
    ltext(d, 28, 432, "AND IT BROKE EVERYTHING. TOUCH GRASS? CAN'T. 212 GB.",
          23, CYAN, maxw=960)

    # MIDDLE ROW
    MY, MH = 488, 244

    def hpanel(i, outline):
        x = XS[i]
        d.rounded_rectangle([x, MY, x + PW, MY + MH], radius=14,
                            fill=(18, 18, 30), outline=outline, width=2)
        return x

    x = hpanel(0, CYAN)
    ltext(d, x + 20, MY + 12, "212 GB", 44, CYAN, maxw=280)
    photo(img, d, "router.jpg", [x + 14, MY + 60, x + PW - 14, MY + 128],
          (0.6, 0.62), outline=(70, 70, 100))
    bar94(d, x + 20, x + PW - 20, MY + 138)
    ltext(d, x + 20, MY + 176, "STUCK AT 94% — DOWN BAD.", 19, PINK, maxw=282)
    ltext(d, x + 20, MY + 204, "pre-load since Nov 10 · 19 hrs at 25 Mbps", 13,
          SUB, maxw=282)
    ltext(d, x + 20, MY + 222, "41% of the drive. the router saw things.", 13,
          SUB, maxw=282)

    x = hpanel(1, PINK)
    ltext(d, x + 20, MY + 14, "$79.99 BOX", 34, PINK, maxw=282)
    photo(img, d, "case.jpg", [x + 14, MY + 60, x + 118, MY + 178],
          (0.74, 0.45), outline=(70, 70, 100))
    lx = x + 138
    ltext(d, lx, MY + 68, "1 code", 21, WHITE, maxw=165)
    ltext(d, lx, MY + 98, "1 poster", 21, WHITE, maxw=165)
    ltext(d, lx, MY + 128, "0 discs", 25, RED, maxw=165)
    ltext(d, x + 20, MY + 192, "Ultimate: $99.99", 13, SUB, maxw=282)
    ltext(d, x + 20, MY + 210, "hub caught empty in 4K", 13, SUB, maxw=282)

    x = hpanel(2, GOLD)
    ltext(d, x + 20, MY + 12, "30 FPS", 44, GOLD, maxw=280)
    photo(img, d, "ps5pro.jpg", [x + 14, MY + 60, x + PW - 14, MY + 132],
          (0.5, 0.5), outline=(70, 70, 100))
    ltext(d, x + 20, MY + 144, "'POWERPOINT EDITION' — FR.", 19, PINK, maxw=282)
    ltext(d, x + 20, MY + 176, "Metacritic 99 · locked at 30", 13, SUB,
          maxw=282)
    ltext(d, x + 20, MY + 194, "TheBurntPeanut called it a slideshow", 13, SUB,
          maxw=282)

    # GRID
    d.rectangle([16, 744, W - 16, 778], fill=PINK)
    ctext(d, W // 2, 750, "THE LAUNCH-DAY SIDE QUESTS:", 23, INK, maxw=960)
    GH = 184
    cells = [
        ("xqc.jpg", (0.36, 0.35), (24, 20, 30), False, "xQc TOOK A SIDE QUEST:",
         "45 MIN OF HOME RENO. GTA SIMS.", "drill + peach paint · dad simulator arc"),
        ("sick.jpg", (0.6, 0.4), (24, 20, 30), False, "OFFICE-WIDE, NOV 19:",
         "'GTA FLU' EPIDEMIC. NO CAP.", "boss: 'Interesting.' · two-thirds were joking"),
        ("kai.jpg", (0.5, 0.45), (24, 20, 30), False, "KAI CENAT AT THE UNLOCK:",
         "PRAYED LIKE IT WAS FINALS.", "130-hour marathon done · man was locked in"),
        ("nz.jpg", (0.5, 0.45), (24, 20, 30), False, "NEW ZEALAND SPEEDRUN:",
         "FIRST UNLOCK ON EARTH.", "5.3M watching within minutes · any% PB"),
        ("grave.jpg", (0.4, 0.5), (24, 20, 30), False, "RIP THE GOAT MEME:",
         "'WE GOT X BEFORE GTA 6' (2013–2026)", "18% of launch-day memes · press F"),
        ("phone.jpg", (0.45, 0.6), (24, 20, 30), False, "SPOILER LOCKDOWN:",
         "GOING DARK. DO NOT DM.", "muted words: all of them · 130-hour story"),
    ]
    for i, (name, foc, bg, dark, top, punch, small) in enumerate(cells):
        x, y = XS[i % 3], 790 + (i // 3) * (GH + 12)
        d.rounded_rectangle([x, y, x + PW, y + GH], radius=12, fill=bg,
                            outline=(90, 90, 120), width=2)
        photo(img, d, name, [x + 12, y + 44, x + PW - 12, y + 112], foc)
        ctext(d, x + PW // 2, y + 9, top, 18, WHITE, maxw=296)
        ctext(d, x + PW // 2, y + 120, punch, 18, WHITE, maxw=296)
        ctext(d, x + PW // 2, y + 152, small, 12, (178, 182, 200), maxw=296)

    d.rectangle([0, 1178, W, 1184], fill=PINK)
    footer(img, 1184)
    out = os.path.join(HERE, "meme9.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


# ---------------------------------------------------------------------------
# Candidate I — THE LEONIDA DAILY (deadpan newspaper front page)
# ---------------------------------------------------------------------------

def build_i():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # MASTHEAD
    d.line([(16, 22), (W - 16, 22)], fill=INK, width=3)
    ctext(d, W // 2, 32, "THE LEONIDA DAILY", 62, INK, maxw=980, path=SERIF)
    ctext(d, W // 2, 108, "VICE CITY · FRIDAY, NOVEMBER 20, 2026 · VOL. VI — "
          "NO. 19 · STILL NO PC VERSION", 15, INK, maxw=980)
    d.line([(16, 134), (W - 16, 134)], fill=INK, width=5)
    d.line([(16, 142), (W - 16, 142)], fill=INK, width=2)

    # HEADLINE + DECK
    ctext(d, W // 2, 154, "GTA VI IS HERE", 84, INK, maxw=980, path=SERIF)
    ctext(d, W // 2, 248, "After 4,811 days, the wait ends. PSN did not "
          "survive it. Twice.", 20, INK, maxw=980)
    ctext(d, W // 2, 278, "By STAFF REPORTS · Frames per second: 30 · "
          "Discs in box: 0 · Sick notes filed: all of them", 13, GRAY,
          maxw=980)

    # LEAD PHOTO + GHOST
    photo(img, d, "keyart.jpg", [16, 300, W - 16, 566], (0.45, 0.30), width=3)
    paste_ghost(img, 946, 512, 124)
    d = ImageDraw.Draw(img)
    ltext(d, 16, 574, "Jason and Lucia, main character energy, at golden "
          "hour. The car has seen things. The frame rate has not.", 13,
          GRAY, maxw=830, path=SANS_I)

    # COLUMNS
    CY = 616
    cols = [
        ("case.jpg", (0.6, 0.45), ("THE $79.99 BOX", "CONTAINS NO DISC"),
         ("Inside the box: one code,",
          "one A3 poster, zero discs,",
          "and one empty hub, holding",
          "the shape of a disc.",
          "The Ultimate edition costs",
          "$99.99. Unboxers caught",
          "the emptiness in 4K.")),
        ("ps5pro.jpg", (0.5, 0.5), ("LOCAL CONSOLE RUNS", "AT 30 FRAMES. TOTAL."),
         ("Metacritic says 99. The",
          "frames say 30, locked, on",
          "every console — Pro too.",
          "\"It's giving PowerPoint,\"",
          "one streamer ruled. It is",
          "the only complaint in",
          "every review. Fr fr.")),
        ("router.jpg", (0.6, 0.62), ("212 GB DOWNLOAD", "DIES AT 94 PERCENT"),
         ("The pre-load opened Nov 10.",
          "It asked for 19 hours at",
          "25 Mbps and 41 percent of",
          "a 512 GB drive. Other games",
          "were deleted to make room.",
          "They did not survive.",
          "GG go next.")),
    ]
    for i, (name, foc, head, body) in enumerate(cols):
        x = XS[i]
        if i:
            d.line([(x - 18, CY), (x - 18, CY + 316)], fill=(170, 164, 150),
                   width=2)
        photo(img, d, name, [x, CY, x + PW, CY + 96], foc, width=2)
        ctext(d, x + PW // 2, CY + 106, head[0], 22, INK, maxw=310, path=SERIF)
        ctext(d, x + PW // 2, CY + 132, head[1], 22, INK, maxw=310, path=SERIF)
        for j, line in enumerate(body):
            ltext(d, x + 4, CY + 168 + j * 21, line, 14, INK, maxw=312)

    # IN BRIEF
    BY = 956
    d.line([(16, BY), (W - 16, BY)], fill=INK, width=3)
    ctext(d, W // 2, BY + 8, "IN BRIEF — LAUNCH DAY, ABRIDGED", 24, INK,
          maxw=960, path=SERIF)
    d.line([(16, BY + 42), (W - 16, BY + 42)], fill=INK, width=2)
    briefs = [
        ("xqc.jpg", (0.36, 0.35), "xQc spent 45 min", "renovating. GTA Sims."),
        ("sick.jpg", (0.6, 0.4), "GTA flu empties office.", "Boss: 'Interesting.'"),
        ("kai.jpg", (0.5, 0.3), "Kai Cenat prayed at", "the unlock. Locked in."),
        ("nz.jpg", (0.5, 0.45), "New Zealand unlocked", "first. 5.3M watched."),
        ("grave.jpg", (0.4, 0.5), "'We got X before GTA 6'", "dead at 13 years. RIP."),
        ("phone.jpg", (0.45, 0.6), "Fans go dark over", "spoilers. 130-hr story."),
    ]
    for i, (name, foc, l1, l2) in enumerate(briefs):
        x = XS[i % 3]
        y = BY + 56 + (i // 3) * 68
        photo(img, d, name, [x, y, x + 86, y + 54], foc, width=1)
        ltext(d, x + 96, y + 4, l1, 14, INK, maxw=220)
        ltext(d, x + 96, y + 26, l2, 14, INK, maxw=220)

    # CLASSIFIEDS + FOOTER
    d.rectangle([16, 1140, W - 16, 1170], fill=BLACK)
    ctext(d, W // 2, 1147, "CLASSIFIEDS · 7.8M PEAK VIEWERS · WIDOWS OF VICE "
          "CITY: 23M HOUSEHOLDS · CLIPS MISTAKEN FOR REAL LIFE, DAILY", 13,
          GOLD, maxw=970)
    footer(img, 1184)
    out = os.path.join(HERE, "meme10.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build_g()
    build_h()
    build_i()
