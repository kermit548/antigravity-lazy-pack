"""Transcribe a video locally with faster-whisper (Windows 11 / PowerShell ready).

Extracts mono 16kHz audio via ffmpeg, runs local faster-whisper with
word-level timestamps, and writes a Scribe-compatible JSON response to
<edit_dir>/transcripts/<video_stem>.json.

Cached: if the output file already exists, transcription is skipped.

Usage:
    python helpers/transcribe.py <video_path>
    python helpers/transcribe.py <video_path> --edit-dir ./edit
    python helpers/transcribe.py <video_path> --language zh
    python helpers/transcribe.py <video_path> --model small --device auto
"""

from __future__ import annotations

import argparse
import array
import json
import math
import os
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path

from faster_whisper import WhisperModel

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_MODEL_CACHE: dict[tuple[str, str, str], WhisperModel] = {}


def load_api_key() -> str:
    """Compatibility stub (no API key needed for local faster-whisper)."""
    return "local_faster_whisper"


def get_whisper_model(
    model_size: str | None = None,
    device: str | None = None,
    compute_type: str | None = None,
) -> WhisperModel:
    """Load and cache faster-whisper model with automatic CUDA -> CPU fallback."""
    model_size = model_size or os.environ.get("WHISPER_MODEL", "small")
    device = device or os.environ.get("WHISPER_DEVICE", "auto")
    compute_type = compute_type or os.environ.get("WHISPER_COMPUTE_TYPE", "default")

    key = (model_size, device, compute_type)
    if key in _MODEL_CACHE:
        return _MODEL_CACHE[key]

    try:
        if compute_type == "default":
            ct = "float16" if device == "cuda" else "int8"
        else:
            ct = compute_type
        model = WhisperModel(model_size, device=device, compute_type=ct)
    except Exception:
        # Fallback to CPU int8 if CUDA/auto fails on Windows without CUDA DLLs
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

    _MODEL_CACHE[key] = model
    return model


def count_audio_tracks(video_path: Path) -> int:
    """How many audio streams the container holds."""
    out = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "a",
            "-show_entries", "stream=index", "-of", "csv=p=0", str(video_path),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return len([ln for ln in out.stdout.splitlines() if ln.strip()])


def peak_dbfs(wav_path: Path) -> float:
    """Peak level of a 16-bit PCM wav, in dBFS. -inf for digital silence."""
    peak = 0
    with wave.open(str(wav_path), "rb") as w:
        while frames := w.readframes(1 << 16):
            samples = array.array("h", frames)
            peak = max(peak, max(samples), -min(samples))
    return 20 * math.log10(peak / 32768) if peak > 0 else float("-inf")


def extract_audio(video_path: Path, dest: Path, audio_track: int = 0) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-map", f"0:a:{audio_track}",
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(dest),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def call_faster_whisper(
    audio_path: Path,
    language: str | None = None,
    model_size: str | None = None,
    device: str | None = None,
    compute_type: str | None = None,
) -> dict:
    """Run local faster-whisper and return Scribe-compatible word-level JSON."""
    model = get_whisper_model(model_size=model_size, device=device, compute_type=compute_type)

    # Retain verbatim speech & filler timing by requesting word_timestamps
    segments, info = model.transcribe(
        str(audio_path),
        beam_size=5,
        language=language,
        word_timestamps=True,
        condition_on_previous_text=False,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=400),
    )

    words_list: list[dict] = []
    full_text_parts: list[str] = []
    prev_end: float | None = None

    for seg in segments:
        if not seg.words:
            continue
        for w in seg.words:
            raw_word = (w.word or "").strip()
            if not raw_word:
                continue
            w_start = round(float(w.start), 3)
            w_end = round(float(w.end), 3)

            if prev_end is not None and (w_start - prev_end) > 0.01:
                words_list.append({
                    "type": "spacing",
                    "text": " ",
                    "start": prev_end,
                    "end": w_start,
                })

            words_list.append({
                "type": "word",
                "text": raw_word,
                "start": w_start,
                "end": w_end,
                "speaker_id": "speaker_0",
                "probability": round(float(getattr(w, "probability", 1.0)), 4),
            })
            full_text_parts.append(raw_word)
            prev_end = w_end

    return {
        "language_code": info.language,
        "language_probability": round(float(info.language_probability), 4),
        "text": " ".join(full_text_parts),
        "words": words_list,
    }


def transcript_path(edit_dir: Path, video: Path, audio_track: int = 0) -> Path:
    """Where a video's transcript lands."""
    suffix = "" if audio_track == 0 else f".track{audio_track}"
    return edit_dir / "transcripts" / f"{video.stem}{suffix}.json"


def transcribe_one(
    video: Path,
    edit_dir: Path,
    api_key: str = "local_faster_whisper",
    language: str | None = None,
    num_speakers: int | None = None,
    verbose: bool = True,
    audio_track: int = 0,
    model_size: str | None = None,
    device: str | None = None,
    compute_type: str | None = None,
) -> Path:
    """Transcribe a single video using local faster-whisper. Returns path to transcript JSON."""
    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    out_path = transcript_path(edit_dir, video, audio_track)

    if out_path.exists():
        if verbose:
            print(f"cached: {out_path.name}")
        return out_path

    if verbose:
        print(f"  extracting audio from {video.name}", flush=True)

    n_tracks = count_audio_tracks(video)
    if n_tracks > 1 and verbose:
        print(
            f"  note: {video.name} has {n_tracks} audio tracks, using track "
            f"{audio_track + 1} (--audio-track to change)",
            flush=True,
        )

    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / f"{video.stem}.wav"
        extract_audio(video, audio, audio_track)

        peak = peak_dbfs(audio)
        if peak < -60.0:
            raise RuntimeError(
                f"track {audio_track + 1} of {video.name} is silent "
                f"(peak {peak:.1f} dBFS) - skipping transcription. "
                + (
                    f"The file has {n_tracks} audio tracks; try --audio-track "
                    + " or ".join(str(i) for i in range(n_tracks) if i != audio_track)
                    + "."
                    if n_tracks > 1
                    else "Check the source audio."
                )
            )

        size_mb = audio.stat().st_size / (1024 * 1024)
        if verbose:
            print(f"  transcribing {video.stem}.wav ({size_mb:.1f} MB) with faster-whisper...", flush=True)
        payload = call_faster_whisper(
            audio_path=audio,
            language=language,
            model_size=model_size,
            device=device,
            compute_type=compute_type,
        )

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    dt = time.time() - t0

    if verbose:
        kb = out_path.stat().st_size / 1024
        print(f"  saved: {out_path.name} ({kb:.1f} KB) in {dt:.1f}s")
        if isinstance(payload, dict) and "words" in payload:
            word_count = sum(1 for w in payload["words"] if w.get("type") == "word")
            print(f"    words: {word_count} (lang: {payload.get('language_code')})")

    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Transcribe a video locally with faster-whisper")
    ap.add_argument("video", type=Path, help="Path to video file")
    ap.add_argument(
        "--edit-dir",
        type=Path,
        default=None,
        help="Edit output directory (default: <video_parent>/edit)",
    )
    ap.add_argument(
        "--language",
        type=str,
        default=None,
        help="Optional ISO language code (e.g., 'zh', 'en'). Omit to auto-detect.",
    )
    ap.add_argument(
        "--num-speakers",
        type=int,
        default=None,
        help="Retained for CLI compatibility.",
    )
    ap.add_argument(
        "--audio-track",
        type=int,
        default=0,
        help="Zero-based audio track to transcribe (default: 0).",
    )
    ap.add_argument(
        "--model",
        type=str,
        default=None,
        help="Whisper model size: tiny, base, small, medium, large-v3 (default: small or WHISPER_MODEL env).",
    )
    ap.add_argument(
        "--device",
        type=str,
        default=None,
        help="Device for CTranslate2: auto, cpu, cuda (default: auto).",
    )
    ap.add_argument(
        "--compute-type",
        type=str,
        default=None,
        help="Compute type: int8, float16, float32 (default: auto-selected).",
    )
    args = ap.parse_args()

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"video not found: {video}")

    edit_dir = (args.edit_dir or (video.parent / "edit")).resolve()

    transcribe_one(
        video=video,
        edit_dir=edit_dir,
        language=args.language,
        num_speakers=args.num_speakers,
        audio_track=args.audio_track,
        model_size=args.model,
        device=args.device,
        compute_type=args.compute_type,
    )


if __name__ == "__main__":
    main()
