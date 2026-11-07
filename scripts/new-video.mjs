#!/usr/bin/env node
// Scaffold a new HyperFrames video under videos/<slug>.
//
// Usage: pnpm new-video <slug> [--video path/to/footage.mp4]
//
// 1. Runs `hyperframes init` (the root-pinned CLI) with the blank example.
// 2. Drops the per-video CLAUDE.md / AGENTS.md that init generates, because the
//    root CLAUDE.md is the single source of workspace rules.
// 3. Rewrites the generated package.json scripts to use the root CLI instead of
//    `npx hyperframes@<version>`, so every video renders with the same version.
//
// It deliberately writes no BRIEF.md or STORYBOARD.md. The /hyperframes router
// treats an existing BRIEF.md as a confirmed brief and stops asking questions,
// so the intent interview writes it (or you copy templates/video/BRIEF.md and
// fill every key). The workflow writes STORYBOARD.md in its own format.

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, writeFileSync, rmSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const videosDir = join(root, "videos");
const hyperframesBin = join(root, "node_modules", ".bin", "hyperframes");

const args = process.argv.slice(2);
const slug = args[0];

function flagValue(name) {
  const index = args.indexOf(name);
  if (index === -1) return null;
  const value = args[index + 1];
  if (!value || value.startsWith("--")) fail(`${name} needs a value`);
  return value;
}

const footage = flagValue("--video");
// Owning workflow (e.g. general-video), stamped into hyperframes.json by init.
const skill = flagValue("--skill");

function fail(message) {
  console.error(`new-video: ${message}`);
  process.exit(1);
}

if (!slug || slug.startsWith("--")) {
  fail("missing <slug>. Usage: pnpm new-video <slug> [--skill <workflow>] [--video footage.mp4]");
}
if (!/^[a-z0-9][a-z0-9_-]*$/.test(slug)) {
  fail(`invalid slug "${slug}". Use lowercase letters, digits, "-" or "_".`);
}
if (!existsSync(hyperframesBin)) fail("hyperframes is not installed. Run `pnpm install` at the root first.");

const projectDir = join(videosDir, slug);
if (existsSync(projectDir)) fail(`videos/${slug} already exists.`);

const initArgs = ["init", slug, "--non-interactive", "--example", "blank"];
if (footage) initArgs.push("--video", footage);
if (skill) initArgs.push("--skill", skill);

const init = spawnSync(hyperframesBin, initArgs, { cwd: videosDir, stdio: "inherit" });
if (init.status !== 0) fail("hyperframes init failed. See the output above.");

// The root CLAUDE.md is the single source of rules; per-video copies drift.
for (const generated of ["CLAUDE.md", "AGENTS.md"]) {
  rmSync(join(projectDir, generated), { force: true });
}

// Use the root-pinned CLI, not `npx hyperframes@<version>`.
const pkgPath = join(projectDir, "package.json");
const pkg = JSON.parse(readFileSync(pkgPath, "utf8"));
pkg.scripts = {
  dev: "hyperframes preview",
  check: "hyperframes check",
  render: "hyperframes render",
  publish: "hyperframes publish",
};
writeFileSync(pkgPath, `${JSON.stringify(pkg, null, 2)}\n`);

console.log(`
Created videos/${slug}.

Next:
  1. Put footage and audio in videos/${slug}/assets/.
  2. cd videos/${slug}, start Claude Code and ask with /hyperframes.
     Its interview writes BRIEF.md (style is decided per video).
  3. Follow NUEVO_VIDEO.md at the workspace root.
`);
