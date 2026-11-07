#!/usr/bin/env node
// Build videos/<slug>/index.html from the episode data.
// Usage: node scripts/ng/compose.mjs videos/<slug> [--limit <seconds>]   (--limit = short test build)
//
// The EN episode is the base layer: frame, logo, right panel and screen recordings are its original
// pixels (the right panel stays in English on purpose). On top of it:
//   - #capbar hides the burned-in EN captions, the ES captions sit on it
//   - presenter clips put the ES host in the left panel
//
// Inputs (videos/<slug>/data/):
//   blocks.json            EN blocks [{id, topic, kind, en_start, en_end}]   (segment_en.py)
//   cutlist.json           [{block, es_in, es_out}] in output order          (align.py build)
//   transcript.es.json     word timestamps of the Spanish recording
//   caption_fixes.json     optional [{from, to}] word-sequence corrections (proofreading step)
//   interviews.json        optional, lines of each interview (align.py prepare)
//   episode.json           optional {es_crop:{x,y,w}, caption_font} (defaults below)
// Output: index.html, data/timeline.json and these cached media files:
//   assets/es/presenter.mp4  16:9 face crop at 2x panel size (4K-ready)
//   assets/es/voice.wav      ES audio normalized to -16 LUFS
//
// Layout constants mirror shared/brand/FRAME.md (1920x1080).
import { execFileSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const dir = resolve(process.argv[2] ?? "");
if (!process.argv[2] || !existsSync(dir)) {
  console.error("usage: node scripts/ng/compose.mjs videos/<slug> [--limit <seconds>]");
  process.exit(1);
}
const limitAt = process.argv.indexOf("--limit");
const limit = limitAt > 0 ? Number(process.argv[limitAt + 1]) : Infinity;
const data = (f) => JSON.parse(readFileSync(join(dir, "data", f), "utf8"));
const maybe = (f, d) => (existsSync(join(dir, "data", f)) ? data(f) : d);

const blocks = data("blocks.json");
const cutlist = data("cutlist.json");
const episode = maybe("episode.json", {});
const interviews = maybe("interviews.json", []);
const crop = episode.es_crop ?? { x: 559, y: 333, w: 2594 };
const font = episode.caption_font ?? "SpaceGrotesk";

// ---- ES words, proofread --------------------------------------------------------------------
const rawT = data("transcript.es.json");
const rawWords = Array.isArray(rawT) ? rawT : (rawT.words ?? rawT.segments?.flatMap((s) => s.words ?? []) ?? []);
let words = rawWords
  .map((w) => ({ t: String(w.text ?? w.word ?? "").trim(), s: Number(w.start), e: Number(w.end) }))
  .filter((w) => w.t && Number.isFinite(w.s));

// A fix replaces a word sequence and spreads the replacement over the same time span.
for (const { from, to } of maybe("caption_fixes.json", [])) {
  const a = from.split(" ");
  const b = to.split(" ");
  let hits = 0;
  for (let i = 0; i + a.length <= words.length; i++) {
    if (!a.every((w, k) => words[i + k].t === w)) continue;
    const s = words[i].s;
    const span = words[i + a.length - 1].e - s;
    const chars = b.join("").length;
    let at = 0;
    const repl = b.map((t, k) => {
      if (a.length === b.length) return { ...words[i + k], t };
      const w = { t, s: s + (span * at) / chars, e: s + (span * (at + t.length)) / chars };
      at += t.length;
      return w;
    });
    words.splice(i, a.length, ...repl);
    hits++;
  }
  if (!hits) console.warn(`caption_fixes: "${from}" not found`);
}

// ---- cached media -------------------------------------------------------------------------------
const esDir = join(dir, "assets/es");
const presenter = join(esDir, "presenter.mp4");
const stamp = join(esDir, "presenter.crop.json");
const want = JSON.stringify(crop);
if (!existsSync(presenter) || !existsSync(stamp) || readFileSync(stamp, "utf8") !== want) {
  const h = Math.round((crop.w * 9) / 16);
  execFileSync(
    "ffmpeg",
    ["-y", "-v", "error", "-i", join(esDir, "recording.mp4"), "-vf", `crop=${crop.w}:${h}:${crop.x}:${crop.y},scale=1500:844:flags=lanczos,fps=30`,
     "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-g", "30", "-an", presenter],
    { stdio: "inherit" },
  );
  writeFileSync(stamp, want);
}
const voice = join(esDir, "voice.wav");
if (!existsSync(voice)) {
  // recordings arrive around -28 LUFS, far below what YouTube plays back at
  execFileSync("ffmpeg", ["-y", "-v", "error", "-i", join(esDir, "recording.mp4"), "-vn", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", voice], { stdio: "inherit" });
}
if (!existsSync(join(dir, "assets/en/hq.mp4"))) throw new Error("assets/en/hq.mp4 is missing: run scripts/ng/fetch.sh");
mkdirSync(join(dir, "fonts"), { recursive: true });
const fontFile = `${font}-700.woff2`;
if (!existsSync(join(dir, "fonts", fontFile))) copyFileSync(join(root, "templates/ng-news/fonts", fontFile), join(dir, "fonts", fontFile));

// ---- timeline -----------------------------------------------------------------------------------
const isInterview = (c) => c.interview !== undefined;
const clipDuration = (c) => (isInterview(c) ? c.en_out - c.en_in : c.es_out - c.es_in);
let t = 0;
const entries = [];
for (const c of cutlist) {
  if (t >= limit) break;
  const b = blocks.find((x) => x.id === c.block);
  if (!b) throw new Error(`cutlist references unknown block ${c.block}`);
  const dur = +clipDuration(c).toFixed(3);
  entries.push({ ...c, kind: b.kind, topic: b.topic, start: +t.toFixed(3), dur, block: b });
  t += dur;
}
const total = +t.toFixed(3);

const blockTotals = new Map();
for (const c of cutlist) blockTotals.set(c.block, (blockTotals.get(c.block) ?? 0) + clipDuration(c));

const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const used = new Map();
let baseHtml = "";
let hostHtml = "";
let audioHtml = "";
entries.forEach((e, i) => {
  if (isInterview(e)) {
    // the guest keeps their voice: EN picture and audio at normal speed, at the level of the ES host
    const wav = `assets/en/interview-${e.interview}.wav`;
    execFileSync("ffmpeg", ["-y", "-v", "error", "-ss", String(e.en_in), "-t", String(e.dur), "-i", join(dir, "assets/en/source.mp4"), "-vn", "-af", `loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:d=0.03,afade=t=out:st=${e.dur - 0.03}:d=0.03`, "-ar", "48000", join(dir, wav)], { stdio: "inherit" });
    baseHtml += `      <video id="b${i}" class="clip base" src="assets/en/hq.mp4" data-start="${e.start}" data-duration="${e.dur}" data-media-start="${e.en_in}" data-track-index="0" muted playsinline></video>\n`;
    audioHtml += `      <audio id="a${i}" src="${wav}" data-start="${e.start}" data-duration="${e.dur}" data-track-index="20" data-volume="1"></audio>\n`;
    return;
  }
  const b = e.block;
  const enLen = b.en_end - b.en_start - 0.07; // 2 frames of margin before the next shot
  const blockTotal = blockTotals.get(b.id);
  const before = used.get(b.id) ?? 0;
  used.set(b.id, before + e.dur);
  // never overrun the block (next shot would flash in); speed up at most 1.25x, trim the rest
  const rate = Math.min(1.25, enLen / blockTotal);
  const enIn = +(b.en_start + before * rate).toFixed(3);
  baseHtml += `      <video id="b${i}" class="clip base" src="assets/en/hq.mp4" data-start="${e.start}" data-duration="${e.dur}" data-media-start="${enIn}" data-playback-rate="${rate.toFixed(3)}" data-track-index="0" muted playsinline></video>\n`;
  if (e.kind === "presenter") {
    hostHtml += `        <video id="h${i}" class="clip host" src="assets/es/presenter.mp4" data-start="${e.start}" data-duration="${e.dur}" data-media-start="${e.es_in}" data-track-index="1" muted playsinline></video>\n`;
  }
  audioHtml += `      <audio id="a${i}" src="assets/es/voice.wav" data-start="${e.start}" data-duration="${e.dur}" data-media-start="${e.es_in}" data-track-index="20" data-volume="1"></audio>\n`;
});

// ---- captions: one phrase on screen, <= 2 balanced lines, cut at clause boundaries ---------------
const MAX_CHARS = 80;
const LINK = /^(y|e|o|u|que|pero|para|mientras|sin|con|como|porque|aunque|si|cuando|donde|lo|la|el|los|las|un|una|a|de|del|en|por|sobre)$/i;
const NO_END = /^(y|e|o|u|que|para|sin|con|como|si|lo|la|el|los|las|un|una|unos|unas|a|al|de|del|en|por|su|sus|es|son|se|ha|no|más)$/i;
const textOf = (ws) => ws.map((w) => w.t).join(" ");
function split(ws) {
  if (textOf(ws).length <= MAX_CHARS) return [ws];
  const half = textOf(ws).length / 2;
  let best = 1;
  let bestScore = Infinity;
  for (let i = 2; i < ws.length - 1; i++) {
    const left = textOf(ws.slice(0, i)).length;
    let score = Math.abs(left - half);
    if (/[,;:]$/.test(ws[i - 1].t)) score -= 24;
    else if (LINK.test(ws[i].t)) score -= 10;
    if (NO_END.test(ws[i - 1].t)) score += 60; // never end a phrase on "de", "la", "es"...
    if (score < bestScore) [best, bestScore] = [i, score];
  }
  return [...split(ws.slice(0, best)), ...split(ws.slice(best))];
}

const glossary = JSON.parse(readFileSync(join(root, ".agents/skills/ng-news-es/references/glossary.json"), "utf8"));
const bare = (s) => s.replace(/[^\p{L}\p{N}$-]/gu, "").toLowerCase();
const emphasisTerms = new Set(glossary.keep_english.map(bare));
for (const common of ["angular", "ai", "pullrequest"]) emphasisTerms.delete(common);
const isEmphasis = (w) => /\d/.test(w) || emphasisTerms.has(bare(w));

// Words on the output timeline. Clips that continue the same take form a run: a phrase may cross
// a shot change there, otherwise the cut would chop it mid-sentence.
const runs = [];
entries.forEach((e, i) => {
  if (isInterview(e)) {
    runs.push({ interview: e });
    return;
  }
  const prev = entries[i - 1];
  if (!prev || isInterview(prev) || Math.abs(prev.es_out - e.es_in) > 0.05) runs.push({ from: e.start, limit: e.start, words: [] });
  const run = runs[runs.length - 1];
  run.limit = e.start + e.dur;
  const toOut = (x) => e.start + x - e.es_in;
  for (const w of words) {
    if (w.s >= e.es_in - 0.03 && w.s < e.es_out - 0.01) run.words.push({ ...w, s: toOut(w.s), e: Math.min(toOut(w.e), e.start + e.dur) });
  }
});
const caps = [];
for (const run of runs) {
  if (run.interview) {
    const e = run.interview;
    for (const line of interviews[e.interview].lines) {
      const s = e.start + line.start - e.en_in;
      const end = e.start + line.end - e.en_in;
      const ws = line.text.split(" ").map((t, k, all) => ({ t, s: s + ((end - s) * k) / all.length, e: s + ((end - s) * (k + 1)) / all.length }));
      caps.push({ ws, from: e.start, limit: e.start + e.dur, interview: true });
    }
    continue;
  }
  let sentence = [];
  const flush = () => {
    for (const g of sentence.length ? split(sentence) : []) caps.push({ ws: g, from: run.from, limit: run.limit });
    sentence = [];
  };
  run.words.forEach((w) => {
    sentence.push(w);
    if (/[.?!…]$/.test(w.t)) flush();
  });
  flush();
}

let capHtml = "";
const tweens = [];
// the line lands before its first word is spoken, but never takes time from the previous word
const LEAD = 0.14;
const startOf = (i) => Math.max(caps[i].ws[0].s - LEAD, caps[i].from, i ? caps[i - 1].ws[caps[i - 1].ws.length - 1].e : 0);
caps.forEach((c, i) => {
  const s = startOf(i);
  const next = caps[i + 1] ? startOf(i + 1) : Infinity;
  const last = c.ws[c.ws.length - 1].e;
  // hold through short pauses so captions do not strobe, clear on long ones
  const end = Math.min(next - last < 0.5 ? next : last + 0.4, c.limit, total);
  const dur = Math.max(end - s, 0.5);
  let emphasized = 0;
  const spans = c.ws
    .map((w, k) => {
      const e = isEmphasis(w.t) && emphasized < 2; // rail rule: 1-2 punch words per phrase
      emphasized += e;
      return `<span id="c${i}w${k}" class="w${e ? " e" : ""}">${esc(w.t)}</span>`;
    })
    .join(" ");
  capHtml += `      <div id="c${i}" class="clip cap" data-start="${s.toFixed(3)}" data-duration="${dur.toFixed(3)}" data-track-index="4"><p id="c${i}p">${spans}</p></div>\n`;
  tweens.push(`tl.fromTo("#c${i}p", { y: 12, opacity: 0 }, { y: 0, opacity: 1, duration: 0.18, ease: "power2.out", immediateRender: false }, ${s.toFixed(3)});`);
  c.ws.forEach((w, k) => {
    const id = `#c${i}w${k}`;
    const fill = Math.min(0.5, Math.max(0.14, w.e - w.s));
    tweens.push(`tl.fromTo("${id}", { backgroundPosition: "100% 0" }, { backgroundPosition: "0% 0", duration: ${fill.toFixed(3)}, ease: "none", immediateRender: false }, ${w.s.toFixed(3)});`);
    tweens.push(`tl.fromTo("${id}", { y: 0 }, { y: -5, duration: 0.09, ease: "power2.out", immediateRender: false }, ${w.s.toFixed(3)});`);
    tweens.push(`tl.fromTo("${id}", { y: -5 }, { y: 0, duration: 0.18, ease: "power2.inOut", immediateRender: false }, ${(w.s + 0.09).toFixed(3)});`);
  });
});

const html = `<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>NG News ${esc(episode.slug ?? "")} ES</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Caption"; font-weight: 700; src: url("fonts/${fontFile}") format("woff2"); }
      html, body { margin: 0; background: #000; }
      #root { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #000; }
      .base { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
      /* left panel and caption bar rects: shared/brand/FRAME.md */
      #left { position: absolute; left: 110px; top: 174px; width: 750px; height: 422px; overflow: hidden; }
      .host { position: absolute; left: 0; top: 0; width: 750px; height: 422px; object-fit: cover; }
      #capbar { position: absolute; left: 72px; top: 700px; width: 1610px; height: 308px; background: #000; }
      .cap { position: absolute; left: 146px; top: 735px; width: 1454px; height: 235px; display: flex; align-items: center; justify-content: center; }
      .cap p { margin: 0; max-width: 1400px; font-family: "Caption", sans-serif; font-size: 48px; font-weight: 700; line-height: 1.28; word-spacing: 0.06em; text-align: center; text-wrap: balance; }
      /* word fill, as shared/blocks/caption-gradient-fill.html: the gradient slides from dim to final
         as the word is spoken, so a magenta edge sweeps through it */
      .w { display: inline-block; color: transparent; -webkit-background-clip: text; background-clip: text; background-size: 350% 100%; background-position: 100% 0;
           background-image: linear-gradient(90deg, #fff 0%, #fff 30%, #f433de 42%, #ef1452 52%, #8b8b99 64%, #8b8b99 100%); }
      .w.e { background-image: linear-gradient(90deg, #ff4f9e 0%, #ff4f9e 30%, #f433de 42%, #ef1452 52%, #8b8b99 64%, #8b8b99 100%); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="${total}">
${baseHtml}      <div id="left">
${hostHtml}      </div>
      <div id="capbar"></div>
${capHtml}${audioHtml}    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      ${tweens.join("\n      ")}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;
writeFileSync(join(dir, "index.html"), html);
writeFileSync(join(dir, "data/timeline.json"), JSON.stringify({ total, entries: entries.map((e) => ({ block: e.block.id, topic: e.topic, kind: e.kind, start: e.start, dur: e.dur, es_in: e.es_in })), captions: caps.map((c) => c.ws.map((w) => ({ t: w.t, s: +w.s.toFixed(3), e: +w.e.toFixed(3), ...(c.interview && { interview: true }) }))) }, null, 1));
console.log(`index.html: ${entries.length} clips, ${caps.length} captions, ${words.length} words, ${total}s`);
