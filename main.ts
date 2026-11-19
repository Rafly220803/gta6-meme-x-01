// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry is a post on X: this repository's POST.json names the post and
// meme.png is the picture the post carries. All the program has to do is
// hand the post package to the gate: it validates POST.json and meme.png
// and copies POST.json to the output directory, where the gate reads it.
// Nothing it writes about the post is judged; the house reads the post
// itself from X.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Deterministic: no network, no clock, no files outside the two directories.

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

function fail(message: string): never {
  console.error(`gta6-meme-x-01: ${message}`);
  process.exit(1);
}

// POST.json must be a JSON object naming the post's address on X.
let post: unknown;
try {
  post = JSON.parse(readFileSync(join(BOT_DIR, 'POST.json'), 'utf8'));
} catch (err) {
  fail(`POST.json could not be read: ${(err as Error).message}`);
}
if (typeof post !== 'object' || post === null || Array.isArray(post)) {
  fail('POST.json is not a JSON object');
}
const url = (post as { url?: unknown }).url;
if (typeof url !== 'string' || !/^https:\/\/(www\.|mobile\.)?(x|twitter)\.com\//.test(url)) {
  fail('POST.json does not name an X post address');
}

// meme.png must be present beside POST.json and really be a PNG: it is the
// picture the post carries, drawn by build_meme.py.
let meme: Buffer;
try {
  meme = readFileSync(join(BOT_DIR, 'meme.png'));
} catch (err) {
  fail(`meme.png could not be read: ${(err as Error).message}`);
}
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (meme.length < PNG_MAGIC.length || !PNG_MAGIC.every((b, i) => meme[i] === b)) {
  fail('meme.png is not a PNG file');
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  fail(`POST.json could not be copied: ${(err as Error).message}`);
}
