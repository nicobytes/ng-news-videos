#!/usr/bin/env node
// Scaffold an NG News episode in videos/<slug>/ from templates/ng-news/.
// Usage: pnpm new-ng <slug> [--en <file.mp4>] [--es <file.mp4>]
// Without flags it expects videos/<slug>/assets/ng-news-<slug>-en.mp4 to be there already, so the
// folder may exist. The ES recording comes later, after /ng-news-guion. Files passed with flags are copied there.
import { copyFileSync, cpSync, existsSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const slug = args[0];
const flag = (n) => { const i = args.indexOf(n); return i < 0 ? null : args[i + 1]; };
const fail = (m) => { console.error(`new-ng: ${m}`); process.exit(1); };

if (!slug || slug.startsWith("--") || !/^[a-z0-9][a-z0-9_-]*$/.test(slug)) fail("usage: pnpm new-ng <slug> [--en <file.mp4>] [--es <file.mp4>]");
const dir = join(root, "videos", slug);
if (existsSync(join(dir, "index.html"))) fail(`videos/${slug} is already composed`);

cpSync(join(root, "templates", "ng-news"), dir, { recursive: true, force: false });
for (const d of ["assets/en", "assets/es", "assets/audio", "data", "renders/review"]) mkdirSync(join(dir, d), { recursive: true });

for (const lang of ["en", "es"]) {
  const src = flag(`--${lang}`);
  const dest = join(dir, "assets", `ng-news-${slug}-${lang}.mp4`);
  if (src && !existsSync(dest)) copyFileSync(resolve(src), dest);
  if (!existsSync(dest) && lang === "en") fail(`missing ${dest}`);
}
const episode = join(dir, "data/episode.json");
if (!existsSync(episode)) writeFileSync(episode, `${JSON.stringify({ slug }, null, 2)}\n`);
console.log(`Ready: videos/${slug}. Next: scripts/ng/fetch.sh videos/${slug}`);
