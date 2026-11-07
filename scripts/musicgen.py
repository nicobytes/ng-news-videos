"""Generate a music bed locally with MusicGen, on the GPU when there is one.

Usage (from the workspace root):
    uv run python scripts/musicgen.py "warm minimal piano, light percussion, 100 BPM" \
        --duration 48 --out videos/<slug>/assets/music/track.wav

    # several candidates to listen to (one file per seed: track-s1.wav, track-s2.wav, ...)
    uv run python scripts/musicgen.py "<prompt>" -d 48 -o .../track.wav --seeds 1,2,3

    # change the mood at a given second (problem -> solution)
    uv run python scripts/musicgen.py "<tense prompt>" --section "15=<warm prompt>" -d 48 -o ...

MusicGen hears ~30 s at a time, so a longer track is continued from its last
--context seconds: one piece, no loop, no seam. Prompts work best in English.

Writes the WAV (48 kHz, 16-bit) plus <out>.json with the model, prompts and seed,
so the same track can be generated again.

The model weights are CC-BY-NC 4.0 (non-commercial). Fine for drafts and temp
tracks; check the license before publishing a commercial piece with the result.
"""

import argparse
import json
import time
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
import torch
import transformers
from transformers import AutoProcessor, MusicgenForConditionalGeneration

FRAME_RATE = 50  # MusicGen tokens per second of audio
OUT_RATE = 48000  # matches scripts/sfx.mjs
SPLICE_FADE_S = 0.2
MIN_NEW_S = 1.0  # never ask for a sliver; the tail is trimmed at the end
SNAP_S = 0.25  # a window may end a hair short: a section this close counts as reached


def parse_sections(prompt: str, raw: list[str]) -> list[tuple[float, str]]:
    sections = [(0.0, prompt)]
    for item in raw:
        at, _, text = item.partition("=")
        if not text.strip():
            raise SystemExit(f"--section expects SECONDS=PROMPT, got {item!r}")
        sections.append((float(at), text.strip()))
    return sorted(sections)


def prompt_at(sections: list[tuple[float, str]], t: float) -> str:
    return [text for start, text in sections if start <= t + 1e-6][-1]


def next_boundary(sections: list[tuple[float, str]], t: float, total: float) -> float:
    later = [start for start, _ in sections if start > t + 1e-6]
    return min(later[0], total) if later else total


class MusicGen:
    def __init__(self, model_id: str, device: str, half: bool):
        self.device = device
        self.dtype = torch.float16 if half and device == "cuda" else torch.float32
        if device == "cuda":
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = MusicgenForConditionalGeneration.from_pretrained(model_id, dtype=self.dtype)
        self.model.to(device).eval()
        self.rate = int(self.model.config.audio_encoder.sampling_rate)
        self.hop = self.rate // FRAME_RATE

    def generate(self, prompt: str, seconds: float, context: np.ndarray | None, opts) -> np.ndarray:
        """One window of audio, shape (channels, samples). With a context, the
        result starts with that context (re-decoded) followed by the new audio."""
        kwargs = {"text": [prompt], "padding": True, "return_tensors": "pt"}
        if context is not None:
            # The feature extractor takes (samples,) for mono and (2, samples) for stereo.
            kwargs["audio"] = context[0] if context.shape[0] == 1 else context
            kwargs["sampling_rate"] = self.rate
        inputs = self.processor(**kwargs).to(self.device)
        if "input_values" in inputs:
            inputs["input_values"] = inputs["input_values"].to(self.dtype)
        with torch.inference_mode():
            audio = self.model.generate(
                **inputs,
                do_sample=True,
                guidance_scale=opts.guidance,
                temperature=opts.temperature,
                top_k=opts.top_k,
                max_new_tokens=max(1, round(seconds * FRAME_RATE)),
            )
        return audio[0].float().cpu().numpy()


def splice(out: np.ndarray, res: np.ndarray, ctx: int, fade: int) -> np.ndarray:
    """Join a continuation onto the track. res[:, :ctx] re-plays out[:, -ctx:], so
    cut in the middle of that shared stretch with a short crossfade. Both sides are
    the same audio, so the gains add up to 1 (linear), not equal-power."""
    at_out = out.shape[1] - ctx // 2
    at_res = ctx // 2
    half = min(fade // 2, ctx // 2)
    if half < 1:
        return np.concatenate([out[:, :at_out], res[:, at_res:]], axis=1)
    t = np.linspace(0.0, 1.0, 2 * half, dtype=np.float32)
    blend = out[:, at_out - half : at_out + half] * (1.0 - t) + res[:, at_res - half : at_res + half] * t
    return np.concatenate([out[:, : at_out - half], blend, res[:, at_res + half :]], axis=1)


def render(gen: MusicGen, sections, seed: int, opts) -> np.ndarray:
    total = opts.duration
    pos = 0.0
    out = None
    chunk = 0
    # Stop within SNAP_S of the end: the few missing samples are padded under the fade-out.
    while pos < total - SNAP_S:
        prompt = prompt_at(sections, pos + SNAP_S)
        boundary = next_boundary(sections, pos + SNAP_S, total)
        # Seed every window on its own: changing --duration keeps the earlier windows identical.
        transformers.set_seed(seed * 1000 + chunk)
        before = pos
        if out is None:
            new_s = max(MIN_NEW_S, min(opts.window, boundary - pos))
            out = gen.generate(prompt, new_s, None, opts)
        else:
            ctx_s = min(opts.context, pos)
            ctx = int(ctx_s * FRAME_RATE) * gen.hop  # whole frames, so the replay lines up
            new_s = max(MIN_NEW_S, min(opts.window - ctx_s, boundary - pos))
            res = gen.generate(prompt, new_s, out[:, -ctx:], opts)
            out = splice(out, res, ctx, int(SPLICE_FADE_S * gen.rate))
        pos = out.shape[1] / gen.rate
        if pos <= before + 0.1:
            raise SystemExit(f"MusicGen stopped adding audio at {pos:.2f}s")
        chunk += 1
        print(f"  [{seed}] {pos:5.1f}/{total:.1f}s  {prompt[:60]}", flush=True)
    want = int(round(total * gen.rate))
    if out.shape[1] < want:
        out = np.pad(out, ((0, 0), (0, want - out.shape[1])))
    return out[:, :want]


def finish(audio: np.ndarray, rate: int, opts) -> np.ndarray:
    audio = librosa.resample(audio, orig_sr=rate, target_sr=OUT_RATE, axis=-1)
    n_in = min(int(opts.fade_in * OUT_RATE), audio.shape[1] // 2)
    n_out = min(int(opts.fade_out * OUT_RATE), audio.shape[1] // 2)
    if n_in > 1:
        audio[:, :n_in] *= np.linspace(0.0, 1.0, n_in, dtype=np.float32)
    if n_out > 1:
        audio[:, -n_out:] *= np.linspace(1.0, 0.0, n_out, dtype=np.float32)
    peak = float(np.max(np.abs(audio)))
    if peak > 1e-6:
        audio = audio * (0.89 / peak)  # -1 dBFS
    return audio


def main() -> None:
    p = argparse.ArgumentParser(description="Local MusicGen music beds (GPU when available).")
    p.add_argument("prompt", help="music description, in English")
    p.add_argument("-d", "--duration", type=float, required=True, help="seconds")
    p.add_argument("-o", "--out", required=True, help="output .wav")
    p.add_argument("--model", default="facebook/musicgen-stereo-large",
                   help="any facebook/musicgen-* checkpoint (small/medium/large, stereo-*)")
    p.add_argument("--seeds", default="1", help="comma list; several seeds = several candidates")
    p.add_argument("--section", action="append", default=[], metavar="SECONDS=PROMPT",
                   help="switch to another prompt from this second on (repeatable)")
    p.add_argument("--guidance", type=float, default=3.0, help="prompt adherence (CFG)")
    p.add_argument("--temperature", type=float, default=1.0)
    p.add_argument("--top-k", type=int, default=250)
    p.add_argument("--window", type=float, default=30.0, help="seconds per generation window")
    p.add_argument("--context", type=float, default=10.0, help="seconds carried into each continuation")
    p.add_argument("--fade-in", type=float, default=0.05)
    p.add_argument("--fade-out", type=float, default=1.5)
    p.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    p.add_argument("--fp32", action="store_true",
                   help="full precision on CUDA (default is float16: ~2.5x faster, a third of the VRAM)")
    opts = p.parse_args()

    if opts.context >= opts.window:
        raise SystemExit("--context must be shorter than --window")
    device = "cuda" if opts.device == "auto" and torch.cuda.is_available() else opts.device
    device = "cpu" if device == "auto" else device
    sections = parse_sections(opts.prompt, opts.section)
    seeds = [int(s) for s in opts.seeds.split(",") if s.strip()]
    out_path = Path(opts.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    gpu = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"
    print(f"musicgen: {opts.model} on {gpu}", flush=True)
    t0 = time.time()
    gen = MusicGen(opts.model, device, half=not opts.fp32)
    print(f"  model ready in {time.time() - t0:.0f}s", flush=True)

    for seed in seeds:
        t1 = time.time()
        audio = finish(render(gen, sections, seed, opts), gen.rate, opts)
        path = out_path if len(seeds) == 1 else out_path.with_name(f"{out_path.stem}-s{seed}{out_path.suffix}")
        sf.write(path, audio.T, OUT_RATE, subtype="PCM_16")
        meta = {
            "file": path.name,
            "model": opts.model,
            "license": "CC-BY-NC-4.0 (model weights)",
            "sections": [{"at": at, "prompt": text} for at, text in sections],
            "seed": seed,
            "duration_s": opts.duration,
            "sample_rate": OUT_RATE,
            "channels": int(audio.shape[0]),
            "guidance": opts.guidance,
            "temperature": opts.temperature,
            "top_k": opts.top_k,
            "window_s": opts.window,
            "context_s": opts.context,
            "device": gpu,
            "dtype": str(gen.dtype).replace("torch.", ""),
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "elapsed_s": round(time.time() - t1, 1),
        }
        if device == "cuda":
            meta["vram_peak_gb"] = round(torch.cuda.max_memory_allocated() / 1e9, 1)
        path.with_suffix(".json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")
        print(f"  wrote {path} ({meta['elapsed_s']}s)", flush=True)


if __name__ == "__main__":
    main()
