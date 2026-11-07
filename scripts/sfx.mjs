#!/usr/bin/env node
// Synthesize UI sound effects in code: deterministic and license-free.
//
// Usage (from the workspace root):
//   node scripts/sfx.mjs --kit <out-dir>          one WAV per sound, to place as audio clips
//   node scripts/sfx.mjs <cues.json> <out.wav>    one mixed track from a cue list
//   node scripts/sfx.mjs <cues.json> <out.wav> --peak   same, but each cue's t marks the sound's
//                                                       peak (its hit), not the start of the file
//
// cues.json: [{ "t": 0.5, "type": "click", "gain": 1 }, ...]
//   t     start time in seconds
//   type  click | tick | pop | thump | chime | whoosh
//   gain  optional multiplier (default 1)

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const SR = 48000;
const TAU = 2 * Math.PI;

// Seeded noise (LCG): the same input always produces the same file.
function noiseSource(seed = 42) {
  let s = seed >>> 0;
  return () => (s = (s * 1664525 + 1013904223) >>> 0) / 2147483648 - 1;
}

// Each voice has a length in seconds and a factory that returns a sample
// function of time. Factories let a voice keep state (the whoosh filter).
const VOICES = {
  click: { len: 0.05, make: () => (t) => Math.sin(TAU * 1800 * t) * Math.exp(-t * 90) * 0.5 },
  tick: { len: 0.03, make: () => (t) => Math.sin(TAU * 4200 * t) * Math.exp(-t * 160) * 0.35 },
  pop: { len: 0.15, make: () => (t) => Math.sin(TAU * (600 + 900 * t) * t) * Math.exp(-t * 30) * 0.4 },
  thump: { len: 0.5, make: () => (t) => Math.sin(TAU * (90 - 60 * t) * t) * Math.exp(-t * 9) * 0.9 },
  chime: {
    len: 0.6,
    make: () => (t) => {
      const first = Math.sin(TAU * 880 * t) * Math.exp(-t * 6);
      const second = t < 0.08 ? 0 : Math.sin(TAU * 1320 * t) * Math.exp(-(t - 0.08) * 6);
      return (first + second) * 0.25;
    },
  },
  whoosh: {
    len: 0.4,
    make: (noise) => {
      let y = 0; // one-pole low-pass whose cutoff sweeps up and back down
      return (t) => {
        const swell = Math.sin((Math.PI * t) / 0.4);
        const cutoff = 300 + 2700 * swell;
        y += (1 - Math.exp((-TAU * cutoff) / SR)) * (noise() - y);
        return y * swell * 0.6;
      };
    },
  },
};

function fail(message) {
  console.error(`sfx: ${message}`);
  process.exit(1);
}

function renderVoice(type, noise) {
  const voice = VOICES[type];
  const sample = voice.make(noise);
  const out = new Float32Array(Math.ceil(voice.len * SR));
  for (let i = 0; i < out.length; i++) out[i] = sample(i / SR);
  return out;
}

// Where a sound hits hardest: the loudest 5 ms window (RMS), in seconds from its start.
function peakOffset(samples) {
  const win = Math.round(0.005 * SR);
  let best = 0;
  let bestAt = 0;
  let acc = 0;
  for (let i = 0; i < samples.length; i++) {
    acc += samples[i] * samples[i];
    if (i >= win) acc -= samples[i - win] * samples[i - win];
    if (acc > best) {
      best = acc;
      bestAt = Math.max(0, i - win / 2);
    }
  }
  return bestAt / SR;
}

function writeWav(path, samples) {
  const n = samples.length;
  const b = Buffer.alloc(44 + n * 2); // 16-bit mono PCM
  b.write("RIFF", 0);
  b.writeUInt32LE(36 + n * 2, 4);
  b.write("WAVEfmt ", 8);
  b.writeUInt32LE(16, 16);
  b.writeUInt16LE(1, 20);
  b.writeUInt16LE(1, 22);
  b.writeUInt32LE(SR, 24);
  b.writeUInt32LE(SR * 2, 28);
  b.writeUInt16LE(2, 32);
  b.writeUInt16LE(16, 34);
  b.write("data", 36);
  b.writeUInt32LE(n * 2, 40);
  for (let i = 0; i < n; i++) {
    b.writeInt16LE(Math.round(Math.max(-1, Math.min(1, samples[i])) * 32767), 44 + i * 2);
  }
  writeFileSync(path, b);
}

const args = process.argv.slice(2);

if (args[0] === "--kit") {
  const dir = args[1];
  if (!dir) fail("--kit needs an output directory");
  mkdirSync(dir, { recursive: true });
  for (const type of Object.keys(VOICES)) {
    writeWav(join(dir, `${type}.wav`), renderVoice(type, noiseSource()));
  }
  console.log(`wrote ${Object.keys(VOICES).length} sounds to ${dir}`);
} else {
  const peak = args.includes("--peak");
  const [cuesPath, outPath] = args.filter((a) => a !== "--peak");
  if (!cuesPath || !outPath) {
    fail("usage: node scripts/sfx.mjs --kit <out-dir> | node scripts/sfx.mjs <cues.json> <out.wav> [--peak]");
  }
  const cues = JSON.parse(readFileSync(cuesPath, "utf8"));
  if (!Array.isArray(cues) || cues.length === 0) fail("cues.json must be a non-empty array");
  for (const cue of cues) {
    if (!VOICES[cue.type]) fail(`unknown type "${cue.type}". Use: ${Object.keys(VOICES).join(", ")}`);
    if (!(cue.t >= 0)) fail(`cue time must be >= 0 (got ${cue.t})`);
  }

  const end = Math.max(...cues.map((c) => c.t + VOICES[c.type].len)) + 0.1;
  const mix = new Float32Array(Math.ceil(end * SR));
  const noise = noiseSource();
  for (const cue of cues) {
    const voice = renderVoice(cue.type, noise);
    const at = peak ? Math.max(0, cue.t - peakOffset(voice)) : cue.t;
    const start = Math.floor(at * SR);
    const gain = cue.gain ?? 1;
    for (let i = 0; i < voice.length && start + i < mix.length; i++) mix[start + i] += voice[i] * gain;
  }
  writeWav(outPath, mix);
  console.log(`wrote ${cues.length} cues (${end.toFixed(2)}s) to ${outPath}${peak ? ", aligned by peak" : ""}`);
}
