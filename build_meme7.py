#!/usr/bin/env python3
"""Candidates K/L -> meme12.png / meme13.png — the proven winner class.

Built from TOP_ANALYSIS.md (ranks 1-10 of gta6-meme-x-01 all share one
class) and RESEARCH2.md (fresh day-2 references):

  CLASS: ONE fake official document fills the whole frame. The wait is
  itemised as deadpan bureaucracy in form fields. The make.fun pitch is
  a big PAID stamp that IS the punchline. The ghost has a job inside
  the document (large, structural). Flat vector, 2-4 colours, big type,
  at-a-glance read. NOT a poster, NOT a collage, NOT a panel grid.

  K (meme12.png) "LEONIDA AIR — BOARDING PASS": the 13-year wait as a
  flight. Passenger EVERY GAMER, departed 2013, flight time 13 years,
  baggage 212 GB, seat neighbour a Hulk (hug optional), connection
  TRAIN — STOPPED, pet on board a petted cat. Ghost = the gate agent.
  Stamp: BOARDED & PAID — BY MY AI AGENT ON make.fun.
  (Top 20 used an arrivals board and, at #56, a boarding pass about
  the delay only — K's document is the full journey itemised with
  day-2 in-flight events; no line is copied from any winner.)

  L (meme13.png) "LEONIDA GENERAL HOSPITAL — DISCHARGE SUMMARY": the
  launch as a hospital stay. Diagnosis TERMINAL HYPE; treatment log =
  day-2 events (Hulk hug, the stopped train, the egged car, the petted
  cat); prognosis 0% story after 10 hours. Ghost = the attending
  nurse holding a clipboard. Stamp: BILL PAID IN FULL — BY MY AI
  AGENT ON make.fun. (A "Discharge Bill" exists at #16 by title only;
  L is a clinical summary, not a bill — no charges, no amounts.)

Jokes all trace to RESEARCH2.md. 1024x1280, deterministic.

Usage: python3 build_meme7.py   (writes meme12.png, meme13.png)
"""

import os
import random

from PIL import Image, ImageDraw, ImageFont

from build_meme5 import paste_ghost_cutout

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1280

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
MONO_R = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

NAVY = (18, 40, 75)
NAVY_D = (10, 24, 48)
PAPER = (248, 246, 238)
CREAM = (245, 239, 226)
INK = (22, 26, 34)
GRAY = (104, 110, 120)
LINE = (196, 200, 208)
MAGENTA = (205, 30, 125)
GOLD = (255, 196, 64)
TEAL = (14, 122, 134)


def F(size, path=SANS):
    return ImageFont.truetype(path, size)


def fit(d, s, maxw, size, path=SANS):
    while size > 10 and d.textlength(s, font=F(size, path)) > maxw:
        size -= 1
    return size


def lt(d, x, y, s, size, fill, path=SANS, maxw=None):
    if maxw:
        size = fit(d, s, maxw, size, path)
    d.text((x, y), s, font=F(size, path), fill=fill, anchor="la")
    return size


def ct(d, cx, y, s, size, fill, path=SANS, maxw=None):
    if maxw:
        size = fit(d, s, maxw, size, path)
    d.text((cx, y), s, font=F(size, path), fill=fill, anchor="ma")
    return size


def field(d, x, y, label, value, w, vsize=36, vcol=INK, vpath=SANS):
    lt(d, x, y, label, 19, GRAY, path=SANS)
    lt(d, x, y + 25, value, vsize, vcol, path=vpath, maxw=w)


def stamp(lines, w=620, h=196, col=MAGENTA, angle=-9):
    """Big rotated PAID stamp; lines = [(text, size), ...]."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([6, 6, w - 6, h - 6], radius=18, outline=col + (255,),
                        width=7)
    total = sum(s for _, s in lines) + 14 * (len(lines) - 1)
    y = (h - total) // 2
    for text, size in lines:
        size = fit(d, text, w - 60, size, SANS)
        d.text((w // 2, y), text, font=F(size), fill=col + (255,),
               anchor="ma")
        y += size + 14
    return layer.rotate(angle, expand=True, resample=Image.BICUBIC)


def barcode(d, x, y, w, h, seed, col=INK):
    rng = random.Random(seed)
    cx = x
    while cx < x + w - 4:
        bw = rng.choice([3, 3, 4, 5, 7, 9])
        if rng.random() > 0.32:
            d.rectangle([cx, y, cx + bw, y + h], fill=col)
        cx += bw + rng.choice([3, 4, 5])


# ---------------------------------------------------------------- K
def build_k():
    img = Image.new("RGB", (W, H), NAVY_D)
    d = ImageDraw.Draw(img)
    d.rectangle([26, 26, W - 26, H - 26], fill=PAPER)
    d.rectangle([26, 26, W - 26, H - 26], outline=GOLD, width=3)

    # Header band
    d.rectangle([52, 52, W - 52, 200], fill=NAVY)
    lt(d, 80, 76, "LEONIDA AIR", 62, PAPER, path=SERIF)
    lt(d, 82, 150, "WE FLY WHEN IT'S READY", 19, GOLD, path=MONO_R)
    ct(d, 836, 74, "BOARDING", 40, GOLD, maxw=250)
    ct(d, 836, 122, "PASS", 40, GOLD, maxw=250)
    ct(d, 836, 168, "FLIGHT VI · GATE 13", 17, PAPER, path=MONO_R, maxw=260)

    # Perforated stub edge
    for yy in range(228, 1004, 18):
        d.line([(798, yy), (798, yy + 9)], fill=GRAY, width=3)

    MX, MW = 56, 716          # main column
    SX, SW = 826, 142         # stub column

    rows = [
        ("PASSENGER", "EVERY GAMER", None),
        ("FROM", "REAL LIFE", ("TO", "LEONIDA")),
        ("DEPARTED", "2013 (ANNOUNCED)", ("DELAYS", "2")),
        ("FLIGHT TIME", "13 YEARS", None),
        ("BAGGAGE", "212 GB (ALL OF IT)", None),
        ("SEAT", "1A (COUCH)", None),
        ("SEAT NEIGHBOUR", "A HULK — HUG = OPTIONAL", None),
        ("CONNECTIONS", "TRAIN — STOPPED", None),
        ("PET ON BOARD", "CAT — PETTED, 10/10", None),
    ]
    y = 226
    for label, value, half in rows:
        if half:
            field(d, MX, y, label, value, 400, vsize=33)
            field(d, MX + 430, y, half[0], half[1], 286, vsize=33)
        else:
            field(d, MX, y, label, value, MW, vsize=35)
        y += 86
        if (label, value, half) != rows[-1]:
            d.line([(MX, y - 12), (772, y - 12)], fill=LINE, width=2)
    # fields end ~1010

    # Stub fields
    sy = 226
    for label, value in [("FLIGHT", "VI"), ("SEAT", "1A"),
                         ("CLASS", "PATIENT"), ("GROUP", "13 YRS"),
                         ("STATUS", "BOARDED")]:
        lt(d, SX, sy, label, 16, GRAY)
        lt(d, SX, sy + 21, value, 26, NAVY, maxw=SW)
        sy += 74
        d.line([(SX, sy - 14), (SX + SW, sy - 14)], fill=LINE, width=2)
    lt(d, SX, sy + 6, "RETAIN", 16, GRAY)
    lt(d, SX, sy + 27, "FOR 13", 26, NAVY)
    lt(d, SX, sy + 57, "YEARS", 26, NAVY)
    barcode(d, SX, 884, SW, 54, seed=13, col=NAVY)
    ct(d, SX + SW // 2, 946, "VI·2013·2026", 14, GRAY, path=MONO_R,
       maxw=SW + 10)

    # Bottom: gate-agent ghost + stamp
    d.line([(56, 1036), (968, 1036)], fill=LINE, width=2)
    paste_ghost_cutout(img, 148, 1128, 185)
    d = ImageDraw.Draw(img)
    ct(d, 148, 1226, "GATE AGENT", 17, GRAY, maxw=180)
    st = stamp([("BOARDED & PAID", 54),
                ("BY MY AI AGENT ON make.fun", 29)], w=600, h=176,
               angle=-6)
    img.paste(st, (322, 1000), st)

    out = os.path.join(HERE, "meme12.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


# ---------------------------------------------------------------- L
def build_l():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([24, 24, W - 24, H - 24], outline=NAVY, width=6)
    d.rectangle([40, 40, W - 40, H - 40], outline=NAVY, width=2)

    # Hospital cross + header
    d.rectangle([90, 52, 110, 128], fill=MAGENTA)
    d.rectangle([74, 78, 126, 102], fill=MAGENTA)
    ct(d, W // 2 + 30, 56, "LEONIDA GENERAL HOSPITAL", 47, NAVY,
       path=SERIF, maxw=830)
    ct(d, W // 2, 122, "DISCHARGE SUMMARY", 74, NAVY, path=SERIF,
       maxw=900)
    ct(d, W // 2, 208, "DEPT. OF TERMINAL HYPE · WARD VI · EST. 2013",
       20, GRAY, path=MONO_R, maxw=800)
    d.line([(64, 246), (960, 246)], fill=NAVY, width=4)
    d.line([(64, 254), (960, 254)], fill=NAVY, width=1)

    MX, MW = 64, 896
    y = 276
    field(d, MX, y, "PATIENT", "A GAMER", 430, vsize=36)
    field(d, MX + 470, y, "ADMITTED", "19 NOV 2026", 426, vsize=36)
    y += 92
    d.line([(MX, y - 14), (960, y - 14)], fill=LINE, width=2)
    field(d, MX, y, "DIAGNOSIS", "TERMINAL HYPE", MW, vsize=40,
          vcol=MAGENTA)
    y += 96
    d.line([(MX, y - 14), (960, y - 14)], fill=LINE, width=2)

    lt(d, MX, y, "TREATMENT LOG", 19, GRAY)
    y += 32
    log = [
        ("HUGGED BY HULK", "RIBS: BRUISED"),
        ("TRAIN STOPPED BEFORE HIS EYES", "DISBELIEF: SEVERE"),
        ("CAR EGGED BY A STRANGER", "NOT HIS CAR"),
        ("CAT PETTED", "THERAPEUTIC"),
    ]
    for item, result in log:
        size = fit(d, item, 560, 27, MONO)
        d.text((MX, y), item, font=F(size, MONO), fill=INK, anchor="la")
        iw = d.textlength(item, font=F(size, MONO))
        rw = d.textlength(result, font=F(27, MONO))
        for dx in range(int(MX + iw + 14), int(960 - rw - 26), 12):
            d.text((dx, y), ".", font=F(27, MONO), fill=GRAY, anchor="la")
        d.text((960, y), result, font=F(27, MONO), fill=NAVY, anchor="ra")
        y += 44
    y += 8
    d.line([(MX, y - 12), (960, y - 12)], fill=LINE, width=2)
    field(d, MX, y, "PROGNOSIS", "0% STORY AFTER 10 HOURS — JUST VIBES",
          MW, vsize=33)
    y += 90
    d.line([(MX, y - 14), (960, y - 14)], fill=LINE, width=2)
    field(d, MX, y, "FOLLOW-UP", "NONE. HE LIVES THERE NOW.", MW,
          vsize=33)
    lt(d, MX, y + 66, "DISCHARGED TO: LEONIDA (PERMANENT)", 20, NAVY,
       path=MONO, maxw=600)
    # fields end ~y+90 ≈ 910

    # Bottom: nurse ghost with clipboard + stamp
    d.line([(64, 936), (960, 936)], fill=NAVY, width=2)
    paste_ghost_cutout(img, 850, 1020, 240)
    d = ImageDraw.Draw(img)
    # clipboard in front of the ghost
    cb = Image.new("RGBA", (140, 180), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cb)
    cd.rounded_rectangle([5, 13, 135, 175], radius=7, fill=(146, 106, 62, 255))
    cd.rounded_rectangle([15, 23, 125, 165], radius=4,
                         fill=(252, 252, 248, 255))
    cd.rounded_rectangle([48, 3, 92, 24], radius=5, fill=(90, 90, 98, 255))
    for i, lw in enumerate([84, 84, 56]):
        cd.line([(26, 50 + i * 28), (26 + lw, 50 + i * 28)],
                fill=(150, 155, 165, 255), width=5)
    cd.line([(26, 136), (98, 136)], fill=MAGENTA + (255,), width=5)
    cb = cb.rotate(7, expand=True, resample=Image.BICUBIC)
    cb = cb.resize((int(cb.width * 0.92), int(cb.height * 0.92)),
                   Image.LANCZOS)
    img.paste(cb, (782, 1008), cb)
    d = ImageDraw.Draw(img)
    ct(d, 850, 1202, "ATTENDING NURSE", 17, GRAY, maxw=220)

    st = stamp([("BILL PAID IN FULL", 56),
                ("BY MY AI AGENT ON make.fun", 31)], w=650, h=196,
               angle=-8)
    img.paste(st, (48, 946), st)

    out = os.path.join(HERE, "meme13.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build_k()
    build_l()
