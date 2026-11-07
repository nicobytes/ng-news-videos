"""Measure the beat grid of an audio track so animations can lock to it.

Usage (from the workspace root):
    uv run python scripts/beats.py path/to/track.wav > path/to/beats.json

Output JSON:
    bpm        estimated tempo
    beats      beat times in seconds (state changes go here)
    downbeats  every 4th beat (big moments go here)
    hits       onset peaks in seconds (SFX go here)
"""

import json
import sys

import librosa
import numpy as np


def measure(path: str) -> dict:
    y, sr = librosa.load(path, sr=None, mono=True)
    tempo, frames = librosa.beat.beat_track(y=y, sr=sr, units="frames")
    beats = librosa.frames_to_time(frames, sr=sr).round(3).tolist()

    onset = librosa.onset.onset_strength(y=y, sr=sr)
    peaks = librosa.util.peak_pick(
        onset, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.5, wait=10
    )
    hits = librosa.frames_to_time(peaks, sr=sr).round(3).tolist()

    return {
        "bpm": float(np.atleast_1d(tempo)[0]),
        "beats": beats,
        "downbeats": beats[::4],
        "hits": hits,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: uv run python scripts/beats.py <audio-file>")
    json.dump(measure(sys.argv[1]), sys.stdout, indent=1)
    print()
