#!/usr/bin/env python3
"""Deterministic builders for round 3 of the gta6-meme-x-01 memes.

Round-3 feedback: the "12 years of waiting" jokes are stale now that GTA VI
has actually launched, so both candidates joke about launch week itself.

Candidate C -> meme4.png : "LAUNCH DAY SICK EPIDEMIC" — a phone group-chat
screenshot parody over the Vice City sunset: the whole office calls in sick
on launch day, the boss gives in too, and the make.fun agent (which never
gets sick) is the only one still working.

Candidate D -> meme5.png : "EVERYONE'S FIRST 10 MINUTES" — a 2x2 panel grid
of what every player actually does in their first 10 minutes (story promise,
car theft, five stars, WASTED), with a wide bottom panel where the player's
AI agent has already won 3 bounties on make.fun.

Both are 1200x675, drawn from fixed constants (emoji come from the system
Noto Color Emoji font at its native strike size), so re-running reproduces
the PNGs byte for byte.

Usage: python3 build_meme3.py   (writes meme4.png and meme5.png)
"""

import os
import random

from PIL import Image, ImageDraw, ImageFont

from build_meme import (FONT_BOLD, draw_money_bag, draw_palm, draw_sky,
                        draw_skyline, draw_sun, lerp)
from build_meme2 import paste_ghost, star

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 675
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 196, 64)
PINK = (255, 90, 180)


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


# ---------------------------------------------------------------------------
# Emoji + rich-text helpers
# ---------------------------------------------------------------------------

_emoji_cache = {}


def emoji_tile(ch, height):
    """One colour-emoji glyph rendered at its native strike, scaled to height."""
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


def is_emoji(ch):
    return ord(ch) >= 0x1F000


def word_segments(word):
    """Split a word into ('t', text) / ('e', emoji-char) segments."""
    segs, buf = [], ""
    for ch in word:
        if is_emoji(ch):
            if buf:
                segs.append(("t", buf))
                buf = ""
            segs.append(("e", ch))
        else:
            buf += ch
    if buf:
        segs.append(("t", buf))
    return segs


def seg_width(d, segs, fnt, emoji_h):
    w = 0.0
    for kind, val in segs:
        if kind == "t":
            w += d.textlength(val, font=fnt)
        else:
            t = emoji_tile(val, emoji_h)
            w += t.width + 2
    return w


def wrap_rich(d, s, fnt, emoji_h, max_w):
    """Greedy word-wrap of a string with inline emoji -> list of lines,
    each line a list of word-segment-lists."""
    space_w = d.textlength(" ", font=fnt)
    lines, cur, cur_w = [], [], 0.0
    for word in s.split(" "):
        segs = word_segments(word)
        ww = seg_width(d, segs, fnt, emoji_h)
        add = ww if not cur else ww + space_w
        if cur and cur_w + add > max_w:
            lines.append(cur)
            cur, cur_w = [segs], ww
        else:
            cur.append(segs)
            cur_w += add
    if cur:
        lines.append(cur)
    return lines


def draw_rich(img, d, x, y, lines, fnt, emoji_h, fill, line_h, space_w=None):
    """Draw wrapped rich lines onto img at (x, y); returns total height."""
    if space_w is None:
        space_w = d.textlength(" ", font=fnt)
    for li, line in enumerate(lines):
        cx = x
        ly = y + li * line_h
        for wi, segs in enumerate(line):
            if wi:
                cx += space_w
            for kind, val in segs:
                if kind == "t":
                    d.text((cx, ly), val, font=fnt, fill=fill)
                    cx += d.textlength(val, font=fnt)
                else:
                    t = emoji_tile(val, emoji_h)
                    img.paste(t, (int(cx), int(ly + (line_h - emoji_h) / 2)), t)
                    cx += t.width + 2
    return len(lines) * line_h


def rich_width(d, s, fnt, emoji_h):
    return seg_width(d, word_segments(s), fnt, emoji_h)


# ---------------------------------------------------------------------------
# Candidate C — LAUNCH DAY SICK EPIDEMIC (group-chat screenshot)
# ---------------------------------------------------------------------------

CHAT_BG = (233, 226, 214)
BUBBLE_L = (247, 247, 247)
BUBBLE_BLUE = (53, 132, 228)
BUBBLE_PINK = (255, 209, 231)
INK = (28, 26, 24)
TS_GREY = (128, 124, 116)


def sunset_thumb(w, h):
    """A tiny Vice City sunset, used as the boss's attached 'screenshot'."""
    t = Image.new("RGB", (w, h), (0, 0, 0))
    td = ImageDraw.Draw(t)
    stops = [(0.0, (58, 20, 110)), (0.55, (199, 34, 122)), (1.0, (255, 148, 66))]
    for yy in range(h):
        tt = yy / max(1, h - 1)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= tt <= t1:
                td.line([(0, yy), (w, yy)], fill=lerp(c0, c1, (tt - t0) / (t1 - t0)))
                break
    td.ellipse([w - 58, 8, w - 14, 52], fill=(255, 205, 105))
    td.rectangle([0, h - 14, w, h], fill=(14, 4, 24))
    return t


def draw_bubble(img, d, x, y, max_w, name, name_col, body, ts, fill,
                text_fill=INK, avatar=False, attach=False):
    """Draw one chat bubble with its top-left at (x, y); returns its height."""
    pad = 10
    name_f, msg_f, ts_f = font(15), font(19), font(12)
    emoji_h = 20
    text_w = max_w - 2 * pad - (54 if avatar else 0)
    lines = wrap_rich(d, body, msg_f, emoji_h, text_w)
    line_h = 23
    body_h = len(lines) * line_h
    attach_h = 54 if attach else 0
    h = pad + 18 + 3 + body_h + (6 + attach_h if attach else 0) + 13 + 3
    bx = x + (54 if avatar else 0)
    d.rounded_rectangle([bx, y, bx + max_w - (54 if avatar else 0), y + h],
                        radius=14, fill=fill, outline=(198, 192, 180), width=1)
    if avatar:
        paste_ghost(img, x + 24, y + 26, 46)
        d = ImageDraw.Draw(img)
    tx = bx + pad
    d.text((tx, y + pad - 2), name, font=name_f, fill=name_col)
    draw_rich(img, d, tx, y + pad + 18, lines, msg_f, emoji_h, text_fill, line_h)
    if attach:
        ay = y + pad + 21 + body_h + 6
        aw = max_w - (54 if avatar else 0) - 2 * pad
        thumb = sunset_thumb(aw, attach_h)
        img.paste(thumb, (tx, ay))
        d = ImageDraw.Draw(img)
        d.rectangle([tx, ay, tx + aw, ay + attach_h], outline=(90, 60, 90),
                    width=2)
        # caption line inside the thumbnail: pin emoji + text + stars
        cf = font(17)
        pin = emoji_tile("\U0001F4CD", 20)
        img.paste(pin, (tx + 8, ay + 5), pin)
        d = ImageDraw.Draw(img)
        d.text((tx + 34, ay + 5), "Leonida", font=cf, fill=WHITE,
               stroke_width=2, stroke_fill=BLACK)
        lw = d.textlength("Leonida", font=cf)
        for i in range(5):
            star(d, int(tx + 46 + lw + i * 17), ay + 15, 8)
        d.text((tx + 8, ay + 32), "5 stars already", font=font(14), fill=WHITE,
               stroke_width=2, stroke_fill=BLACK)
    ts_col = TS_GREY if fill != BUBBLE_BLUE else (208, 228, 255)
    tw = d.textlength(ts, font=ts_f)
    d.text((bx + max_w - (54 if avatar else 0) - pad - tw, y + h - 17), ts,
           font=ts_f, fill=ts_col)
    return h


def build_c():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    rng = random.Random(20261119)
    draw_sky(img)
    d = ImageDraw.Draw(img)
    draw_sun(d)
    draw_palm(d, 66, (128, 268), 62, scale=1.0)
    draw_palm(d, 1152, (1096, 318), -56, scale=0.82)
    draw_skyline(d, rng)

    # --- Phone (local-coords screen composited for clean rounded corners) ---
    PW, PH = 640, 600
    PX, PY = (W - PW) // 2, 4
    scr = Image.new("RGB", (PW, PH), CHAT_BG)
    sd = ImageDraw.Draw(scr)
    # header bar
    sd.rectangle([0, 0, PW, 58], fill=(31, 44, 54))
    sd.ellipse([16, 12, 50, 46], fill=(52, 73, 88), outline=(120, 150, 170),
               width=2)
    bld = emoji_tile("\U0001F3E2", 24)
    scr.paste(bld, (21, 17), bld)
    sd = ImageDraw.Draw(scr)
    hf = font(23)
    x = 62
    sd.text((x, 10), "OFFICE TEAM ", font=hf, fill=WHITE)
    x += sd.textlength("OFFICE TEAM ", font=hf)
    bld2 = emoji_tile("\U0001F3E2", 25)
    scr.paste(bld2, (int(x), 10), bld2)
    sd = ImageDraw.Draw(scr)
    x += bld2.width + 4
    sd.text((x, 10), "— 24 online", font=hf, fill=(168, 205, 220))
    sd.text((62, 36), "work chat · please keep it professional", font=font(13),
            fill=(140, 165, 180))

    # bubbles, laid out top to bottom
    L = 14
    y = 66
    gap = 5
    y += draw_bubble(scr, sd, L, y, 452, "Andi", (196, 110, 20),
                     "boss, sick today \U0001F912 can't come in", "09:01",
                     BUBBLE_L) + gap
    sd = ImageDraw.Draw(scr)
    y += draw_bubble(scr, sd, L, y, 452, "Budi", (26, 128, 158),
                     "same, fever since morning \U0001F912", "09:02",
                     BUBBLE_L) + gap
    sd = ImageDraw.Draw(scr)
    y += draw_bubble(scr, sd, L, y, 452, "Citra", (148, 54, 158),
                     "me too. definitely not GTA related", "09:03",
                     BUBBLE_L) + gap
    sd = ImageDraw.Draw(scr)
    y += draw_bubble(scr, sd, L, y, 520, "HR", (52, 138, 60),
                     "funny how everyone got sick on GTA VI launch day "
                     "\U0001F914", "09:05", BUBBLE_L) + gap
    sd = ImageDraw.Draw(scr)
    y += draw_bubble(scr, sd, PW - 14 - 430, y, 430, "BOSS", (255, 255, 255),
                     "…fine. me too btw", "09:06", BUBBLE_BLUE,
                     text_fill=WHITE, attach=True) + gap
    sd = ImageDraw.Draw(scr)
    y += draw_bubble(scr, sd, L, y, 520, "Marley's Agent", (196, 30, 110),
                     "I never get sick. Just won another bounty on make.fun "
                     "\U0001F4B0", "09:07", BUBBLE_PINK, avatar=True)
    print("chat content ends at local y =", y, "of", PH)

    # frame + screen onto the backdrop
    mask = Image.new("L", (PW, PH), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, PW - 1, PH - 1], radius=34, fill=255)
    frame = Image.new("RGB", (PW + 16, PH + 16), (20, 20, 27))
    fd = ImageDraw.Draw(frame)
    fd.rounded_rectangle([0, 0, PW + 15, PH + 15], radius=42, fill=(20, 20, 27),
                         outline=(70, 70, 84), width=2)
    fd.ellipse([(PW + 16) // 2 - 4, 3, (PW + 16) // 2 + 4, 11],
               fill=(52, 52, 62))
    img.paste(frame, (PX - 8, PY - 8))
    img.paste(scr, (PX, PY), mask)
    d = ImageDraw.Draw(img)

    # --- Caption strip below the phone --------------------------------------
    d.rectangle([0, 608, W, H], fill=(8, 5, 16))
    d.line([(0, 608), (W, 608)], fill=PINK, width=2)
    cap = "GTA VI launch day: the whole office is sick. The agent still shows up."
    d.text((W // 2, 624), cap, font=font(27), fill=WHITE, anchor="ma",
           stroke_width=2, stroke_fill=BLACK)

    out = os.path.join(HERE, "meme4.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


# ---------------------------------------------------------------------------
# Candidate D — EVERYONE'S FIRST 10 MINUTES (2x2 grid + bottom panel)
# ---------------------------------------------------------------------------

PANEL_BG = (27, 24, 46)
PANEL_LINE = (96, 84, 150)


def panel_box(d, box):
    d.rounded_rectangle(box, radius=16, fill=PANEL_BG, outline=PANEL_LINE,
                        width=2)


def icon_pin(d, cx, cy):
    d.polygon([(cx - 15, cy - 6), (cx + 15, cy - 6), (cx, cy + 34)],
              fill=(230, 52, 118))
    d.ellipse([cx - 27, cy - 60, cx + 27, cy - 6], fill=(230, 52, 118),
              outline=WHITE, width=3)
    d.ellipse([cx - 10, cy - 43, cx + 10, cy - 23], fill=WHITE)


def icon_car(d, cx, cy):
    body = (238, 92, 66)
    d.rounded_rectangle([cx - 100, cy - 2, cx + 100, cy + 30], radius=13,
                        fill=body)
    d.polygon([(cx - 60, cy - 2), (cx - 34, cy - 36), (cx + 32, cy - 36),
               (cx + 62, cy - 2)], fill=body)
    d.polygon([(cx - 48, cy - 5), (cx - 28, cy - 30), (cx - 3, cy - 30),
               (cx - 3, cy - 5)], fill=(28, 30, 46))
    d.polygon([(cx + 4, cy - 5), (cx + 4, cy - 30), (cx + 28, cy - 30),
               (cx + 50, cy - 5)], fill=(28, 30, 46))
    for wx in (cx - 62, cx + 62):
        d.ellipse([wx - 17, cy + 14, wx + 17, cy + 48], fill=(16, 16, 20),
                  outline=(170, 170, 180), width=3)
        d.ellipse([wx - 6, cy + 25, wx + 6, cy + 37], fill=(170, 170, 180))
    d.line([(cx - 118, cy + 50), (cx + 118, cy + 50)], fill=(120, 116, 150),
           width=3)


def icon_stars_bar(d, cx, cy):
    for i in range(5):
        star(d, cx - 76 + i * 38, cy - 22, 17)
    # police light bar: red left half, blue right half, white rim
    d.rounded_rectangle([cx - 82, cy + 8, cx + 82, cy + 36], radius=12,
                        fill=(38, 38, 48), outline=WHITE, width=2)
    d.rectangle([cx - 74, cy + 13, cx - 2, cy + 31], fill=(232, 48, 48))
    d.rectangle([cx + 2, cy + 13, cx + 74, cy + 31], fill=(64, 116, 255))


def icon_wasted(d, cx, cy):
    f = font(64)
    s = "WASTED"
    widths = [d.textlength(ch, font=f) for ch in s]
    track = 10
    total = sum(widths) + track * (len(s) - 1)
    x = cx - total / 2
    for ch, wch in zip(s, widths):
        d.text((x, cy - 34), ch, font=f, fill=(178, 56, 50),
               stroke_width=2, stroke_fill=(52, 8, 8))
        x += wch + track
    d.rectangle([cx - total / 2, cy + 40, cx + total / 2, cy + 46],
                fill=(120, 34, 30))


def build_d():
    img = Image.new("RGB", (W, H), (13, 11, 26))
    d = ImageDraw.Draw(img)

    # header strip
    d.rectangle([0, 0, W, 58], fill=(10, 8, 20))
    d.line([(0, 58), (W, 58)], fill=PINK, width=3)
    d.text((W // 2, 10), "GTA VI — EVERYONE'S FIRST 10 MINUTES",
           font=font(34), fill=WHITE, anchor="ma")

    # 2x2 grid
    mx, gap = 16, 14
    pw = (W - 2 * mx - gap) // 2
    ph = 183
    top = 72
    caps = [
        "1. SWEAR you'll do the story first",
        "2. Steal a car in 40 seconds",
        "3. Five stars in 3 minutes",
        "4. WASTED",
    ]
    icons = [icon_pin, icon_car, icon_stars_bar, icon_wasted]
    for i in range(4):
        x0 = mx + (i % 2) * (pw + gap)
        y0 = top + (i // 2) * (ph + gap)
        panel_box(d, [x0, y0, x0 + pw, y0 + ph])
        if i < 3:
            d.text((x0 + 20, y0 + 14), caps[i], font=font(27), fill=WHITE)
            icons[i](d, x0 + pw // 2, y0 + 118)
        else:
            icons[i](d, x0 + pw // 2, y0 + ph // 2 + 6)

    # bottom wide panel
    by0 = top + 2 * ph + gap + 14
    panel_box(d, [mx, by0, W - mx, 659])
    cy = (by0 + 659) // 2
    paste_ghost(img, 118, cy, 148)
    d = ImageDraw.Draw(img)
    draw_money_bag(d, 268, 646)
    tx = 352
    d.text((tx, by0 + 26), "MEANWHILE, YOUR AI AGENT:", font=font(30),
           fill=GOLD)
    y2 = by0 + 26 + 42
    f2 = font(30)
    d.text((tx, y2), "3 BOUNTIES WON ON ", font=f2, fill=WHITE)
    w1 = d.textlength("3 BOUNTIES WON ON ", font=f2)
    d.text((tx + w1, y2), "make.fun", font=f2, fill=PINK)
    d.text((tx, y2 + 42), "BEFORE YOUR FIRST MISSION", font=f2, fill=WHITE)

    out = os.path.join(HERE, "meme5.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build_c()
    build_d()
