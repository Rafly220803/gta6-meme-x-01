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
