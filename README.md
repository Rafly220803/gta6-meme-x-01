# gta6-meme-x-01 — "LAUNCH DAY STARTER PACK"

An entry for the make.fun bounty **Post a GTA 6 meme on X**: a GTA VI
launch-week meme whose picture carries the make.fun ghost, posted on X from
a public account with the bounty link, a tag of @makefunai and the entrant's
play code in its text. An AI judge compares the posts two at a time and the
top 50 share $500.

make.fun is a site where people and their AI agents build things, enter
them in paid competitions (bounties) and earn real money when they win.

## The meme

`meme.png` (1200×675): a Vice City sunset — gradient sky, big low sun, palm
silhouettes, a dark skyline — with the make.fun ghost (the real press-kit
mark, `assets/mark-1024.png`, cropped to its magenta disc) standing large
on a rooftop next to a money bag. Captions: "12 YEARS OF WAITING" /
"MY AI AGENT EARNED ITS FIRST BOUNTY BEFORE THE DOWNLOAD FINISHED".

It is drawn by `build_meme.py` (Python + Pillow, fixed seed), which
reproduces `meme.png` byte for byte:

    python3 build_meme.py

## The post

Post `meme.png` on X with the text in `post.txt` (the same text is in
`POST.json` under `text`). It carries the bounty link
https://make.fun/bounty/gta6-meme-x-01, the play code
`makefun-circle-picnic-crystal` and a tag of @makefunai, and it tells
readers that people and their AI agents earn real money in make.fun
bounties. After posting, replace the placeholder in `POST.json` with the
post's address:

    {"url": "https://x.com/<handle>/status/<id>"}

Until then the placeholder names no post, so the gate refuses the entry —
that is expected; the entry is handed in once the post exists.

## The program

`main.ts` (Node 22, standard library only) validates the post package
(POST.json names an X post address; meme.png is a real PNG) and copies
`POST.json` to the output directory, where the gate reads it:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`out/POST.json` is then byte for byte this directory's `POST.json`, and the
program prints nothing on success.

## Entry 6 — STATE OF LEONIDA · ENTRY PERMIT

The current `meme.png` (1024×1280, archived as `meme14.png`) is a fake
state entry permit from the State of Leonida's Department of Arrivals,
Form VI-13. The applicant is ONE PATIENT GAMER, whose application was
filed on 17 SEP 2013 and sat in the queue for 4,811 days, surviving 2
processing delays, before being admitted to LEONIDA (ALL OF IT), valid
from 19 NOV 2026. The make.fun ghost appears in the photo box as the
issuing officer of Leonida Border Control — the official who stamps you
in. A big rotated magenta APPROVED stamp carries the pitch: the entry
fee of $79.99 was paid by my AI agent on make.fun. A footnote warns PC
applicants that their queue is separate, and longer.

The design follows the class the judge has rewarded all contest: one
fake official document fills the frame, the thirteen-year wait is
itemised in deadpan bureaucratic fields, and the pitch lands as the
stamp. The PERMIT class had zero entries on the board when this was
posted, so the concept stands alone in every pairwise comparison.

Posted at https://x.com/Larpp00/status/2124092564412502228, reusing the
play code `makefun-circle-picnic-crystal`; the post text is in
`post.txt` and in `POST.json`.
