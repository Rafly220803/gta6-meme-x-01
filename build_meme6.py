#!/usr/bin/env python3
"""Candidate J -> meme11.png — "DAY 2 IN LEONIDA" clip-show recap poster.

Built ONLY from the fresh day-2 research in
~/workspace/makefun/runs/meme-x/RESEARCH2.md (researched 2026-11-20):
the literal Easter egg on the tower (xGarbett), IShowSpeed's Hulk,
N3on's contested 7-hour "world first", the 10-hours-0%-story tribe,
Bigfoot the Skunk Ape, NPCs fighting back, the Vanoss Crew stopping
the train, the jet-ski dog, petting the cat, sideways swimming, the
beloved VRR bug, the titanium basketball, and the map-fall prison
speedrun. ZERO jokes from entries #1/#2 are reused (checked against
the banned list in RESEARCH2.md).

KIWI-format density (hero + 3 middle panels + 6-panel grid + ticker +
footer), chaotic "day 2 recap" energy — a different flavour from G
(cream satire), H (dark hero) and I (newspaper). Real photos in
assets/photos/ (fetched + verified 2026-11-20): communications tower,
bodybuilder, cypress swamp, freight train, jet ski, cat, tropical
beach, city traffic, streamer, plus the official GTA VI key art.
The make.fun ghost is integrated as a cutout character climbing out
of the hero art; the footer carries the two pitch lines verbatim.
1024x1280, fixed constants, deterministic.

Usage: python3 build_meme6.py   (writes meme11.png)
"""

import os

from PIL import Image, ImageDraw

from build_meme5 import (BLACK, CYAN, GOLD, INK, PINK, SUB, WHITE, H, W,
                         cover, ctext, footer, grid_panel, ltext,
                         paste_ghost_cutout, photo)

HERE = os.path.dirname(os.path.abspath(__file__))
XS = (16, 351, 686)
PW = 322
BG = (12, 12, 22)
PANEL = (20, 20, 34)


def build_j():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # HERO — key art, gradient band, recap chip, ghost climbing out
    cover(img, "keyart.jpg", [0, 0, W, 330], (0.45, 0.30))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for yy in range(110, 330):
        a = int(238 * (yy - 110) / 220)
        od.line([(0, yy), (W, yy)], fill=(5, 5, 12, a))
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([16, 14, 452, 54], radius=10, fill=(8, 8, 14),
                        outline=GOLD, width=2)
    ltext(d, 30, 25, "DAY 2 · NOV 20 · LEONIDA RECAP", 16, GOLD, maxw=410)
    ltext(d, 26, 222, "DAY 2 IN LEONIDA:", 30, GOLD, maxw=700)
    ltext(d, 26, 256, "THE CLIPS ARE UNHINGED.", 50, WHITE, maxw=760)
    paste_ghost_cutout(img, 946, 262, 118)
    d = ImageDraw.Draw(img)

    # MIDDLE ROW — yesterday's clips
    d.rectangle([16, 342, W - 16, 376], fill=PINK)
    ctext(d, W // 2, 349, "YESTERDAY'S CLIPS, TODAY'S LORE:", 24, INK,
          maxw=960)
    MY, MH = 388, 250

    def mpanel(i, outline):
        x = XS[i]
        d.rounded_rectangle([x, MY, x + PW, MY + MH], radius=14, fill=PANEL,
                            outline=outline, width=2)
        return x

    x = mpanel(0, GOLD)
    ltext(d, x + 20, MY + 12, "A REAL EASTER EGG.", 24, GOLD, maxw=282)
    photo(img, d, "tower2.jpg", [x + 14, MY + 56, x + PW - 14, MY + 138],
          (0.30, 0.45), outline=(92, 92, 122))
    ltext(d, x + 20, MY + 148, "7-MIN LADDER CLIMB. WORTH IT.", 17, PINK,
          maxw=282)
    ltext(d, x + 20, MY + 178, "nest on a tower · xGarbett found it", 13, SUB,
          maxw=282)
    ltext(d, x + 20, MY + 198, "egg'd a vice city npc · cutscene · cinema",
          13, SUB, maxw=282)
    ltext(d, x + 20, MY + 218, "vice city (2002) walked so this could splat",
          13, SUB, maxw=282)

    x = mpanel(1, PINK)
    ltext(d, x + 20, MY + 12, "SPEED MET A HULK.", 24, WHITE, maxw=282)
    photo(img, d, "hulk.jpg", [x + 14, MY + 56, x + PW - 14, MY + 138],
          (0.50, 0.28), outline=(92, 92, 122))
    ltext(d, x + 20, MY + 148, "THROWS PEOPLE AT HELIS.", 17, PINK, maxw=282)
    ltext(d, x + 20, MY + 178, "jason can talk him down · hug or decline",
          13, SUB, maxw=282)
    ltext(d, x + 20, MY + 198, "declining = ??? nobody knows yet", 13, SUB,
          maxw=282)
    ltext(d, x + 20, MY + 218, "man eats gunfire like it's cardio", 13, SUB,
          maxw=282)

    x = mpanel(2, CYAN)
    ltext(d, x + 20, MY + 12, "N3ON 'BEAT' GTA VI", 24, WHITE, maxw=282)
    photo(img, d, "streamer.jpg", [x + 14, MY + 56, x + PW - 14, MY + 138],
          (0.62, 0.40), outline=(92, 92, 122))
    ltext(d, x + 20, MY + 148, "7 HOURS. (PROLOGUE ANY%.)", 17, PINK,
          maxw=282)
    ltext(d, x + 20, MY + 178, "'world first' claim · chat said CAP", 13, SUB,
          maxw=282)
    ltext(d, x + 20, MY + 198, "donnie still alive · that was chapter 1", 13,
          SUB, maxw=282)
    ltext(d, x + 20, MY + 218, "the story is 50–130 hrs. allegedly.", 13, SUB,
          maxw=282)

    # GRID — day-2 side quest leaderboard
    d.rectangle([16, 650, W - 16, 684], fill=GOLD)
    ctext(d, W // 2, 657, "DAY-2 SIDE QUEST LEADERBOARD:", 24, INK, maxw=960)
    GH = 192
    cells = [
        ("swamp.jpg", (0.50, 0.50), "BIGFOOT IS BACK:",
         "AND HE SMELLS TERRIBLE.",
         "skunk ape · lake cottonmouth · follow the roar"),
        ("street.jpg", (0.50, 0.55), "NPCs GOT HANDS NOW:",
         "'WRONG CAR. I RUN FASTER.'",
         "carjack victim chose violence · lucia earned it"),
        ("train.jpg", (0.55, 0.50), "THE TRAIN MYTH, DEAD:",
         "VANOSS CREW STOPPED IT.",
         "'stop, in the name of the law' · it stopped."),
        ("jetski.jpg", (0.60, 0.45), "DOG. ON A JET SKI.",
         "BARKED AT A SCUBA DIVER.",
         "kreek found him · sped off · main character"),
        ("cat.jpg", (0.50, 0.45), "YOU CAN PET THE CAT:",
         "GAME OF THE YEAR. EASY.",
         "corner-store cat · 10/10 · would pet again"),
        ("beach.jpg", (0.50, 0.50), "10 HOURS IN:",
         "0% STORY. STILL IN THE KEYS.",
         "haven't reached vice city · just vibes + npcs"),
    ]
    for i, (name, foc, top, punch, small) in enumerate(cells):
        grid_panel(img, d, XS[i % 3], 696 + (i // 3) * (GH + 12), GH,
                   (22, 22, 36), name, foc, top, punch, small, False)

    # TICKER + FOOTER
    d.rectangle([0, 1104, W, 1136], fill=BLACK)
    ctext(d, W // 2, 1111,
          "• SWIMMING SIDEWAYS • THE GOOD BUG (VRR) — DO NOT PATCH • "
          "TITANIUM BASKETBALL VS PORSCHE • FELL THROUGH THE MAP, "
          "WOKE UP IN PRISON •", 15, GOLD, maxw=1000)
    footer(img, 1148, ghost="cutout")
    out = os.path.join(HERE, "meme11.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build_j()
