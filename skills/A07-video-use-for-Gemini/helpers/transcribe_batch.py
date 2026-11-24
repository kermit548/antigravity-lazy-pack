"""Batch-transcribe every video in a directory using local faster-whisper.

Walks <videos_dir> for common video extensions, runs local faster-whisper on
each, writes transcripts to <videos_dir>/edit/transcripts/<name>.json.

Cached per-file: any source that already has a transcript is skipped.

Usage:
    python helpers/transcribe_batch.py <videos_dir>
    python helpers/transcribe_batch.py <videos_dir> --model small
    python helpers/transcribe_batch.py <videos_dir> --language zh
    python helpers/transcribe_batch.py <videos_dir> --edit-dir ./edit
"""

from __future__ import annotations

import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from transcribe import get_whisper_model, transcribe_one, transcript_path


VIDEO_EXTS = {".mp4", ".MP4", ".mov", ".MOV", ".mkv", ".MKV", ".avi", ".AVI", ".m4v"}


def find_videos(videos_dir: Path) -> list[Path]:
    # Use case-insensitive deduplication on Windows where .mp4 and .MP4 match the same file
    seen: set[Path] = set()
    videos: list[Path] = []
    for p in sorted(videos_dir.iterdir(), key=lambda x: x.name.lower()):
        if p.is_file() and p.suffix in VIDEO_EXTS:
            resolved = p.resolve()
            if resolved not in seen:
                seen.add(resolved)
                videos.append(p)
    return videos


def main() -> None:
    ap = argparse.ArgumentParser(description="Batch transcription of a videos directory with faster-whisper")
    ap.add_argument("videos_dir", type=Path, help="Directory containing source videos")
    ap.add_argument(
        "--edit-dir",
        type=Path,
        default=None,
        help="Edit output directory (default: <videos_dir>/edit)",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Parallel workers (default: 1 for local faster-whisper since CTranslate2 uses multi-threading internally)",
    )
    ap.add_argument(
        "--language",
        type=str,
        default=None,
        help="Optional ISO language code (e.g. 'zh', 'en'). Omit to auto-detect per file.",
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
        help="Zero-based audio track to transcribe (OBS: 0 = game, 1 = mic).",
    )
    ap.add_argument(
        "--model",
        type=str,
        default=None,
        help="Whisper model size: tiny, base, small, medium, large-v3 (default: small).",
    )
    ap.add_argument(
        "--device",
        type=str,
        default=None,
        help="Device: auto, cpu, cuda (default: auto).",
    )
    ap.add_argument(
        "--compute-type",
        type=str,
        default=None,
        help="Compute type: int8, float16, float32 (default: auto).",
    )
    args = ap.parse_args()

    videos_dir = args.videos_dir.resolve()
    if not videos_dir.is_dir():
        sys.exit(f"not a directory: {videos_dir}")

    edit_dir = (args.edit_dir or (videos_dir / "edit")).resolve()
    (edit_dir / "transcripts").mkdir(parents=True, exist_ok=True)

    videos = find_videos(videos_dir)
    if not videos:
        sys.exit(f"no videos found in {videos_dir}")

    already_cached = [
        v for v in videos if transcript_path(edit_dir, v, args.audio_track).exists()
    ]
    pending = [v for v in videos if v not in already_cached]

    print(f"found {len(videos)} videos ({len(already_cached)} cached, {len(pending)} to transcribe)")
    if not pending:
        print("nothing to do")
        return

    # Pre-warm model once before worker pool starts
    print("loading faster-whisper model...")
    get_whisper_model(
        model_size=args.model,
        device=args.device,
        compute_type=args.compute_type,
    )

    print(f"transcribing {len(pending)} files with {args.workers} worker(s)")
    t0 = time.time()

    errors: list[tuple[Path, str]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                transcribe_one,
                video=v,
                edit_dir=edit_dir,
                language=args.language,
                num_speakers=args.num_speakers,
                verbose=False,
                audio_track=args.audio_track,
                model_size=args.model,
                device=args.device,
                compute_type=args.compute_type,
            ): v
            for v in pending
        }
        for fut in as_completed(futures):
            v = futures[fut]
            try:
                out = fut.result()
                print(f"  + {v.stem}  ->  {out.name}")
            except Exception as e:
                errors.append((v, str(e)))
                print(f"  x {v.stem}  FAILED: {e}")

    dt = time.time() - t0
    print(f"\ndone in {dt:.1f}s")
    if errors:
        print(f"{len(errors)} failures:")
        for v, msg in errors:
            print(f"  {v.name}: {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
