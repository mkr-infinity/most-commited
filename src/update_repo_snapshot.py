#!/usr/bin/env python3
"""Generate a stable src-only repository snapshot.

The snapshot intentionally excludes this script and the generated output file so
running the tool repeatedly does not create commits from its own metadata.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
from pathlib import Path


OUTPUT_PATH = Path("src/repo_snapshot.md")
EXCLUDED_PATHS = {
    Path("src/repo_snapshot.md"),
    Path("src/update_repo_snapshot.py"),
}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=check,
        capture_output=True,
        text=True,
    )


def tracked_src_files() -> list[Path]:
    result = git("ls-files", "src")
    files = [Path(line) for line in result.stdout.splitlines() if line]
    return sorted(path for path in files if path not in EXCLUDED_PATHS)


def file_row(path: Path) -> str:
    data = path.read_bytes()
    line_count = data.count(b"\n") + (0 if not data or data.endswith(b"\n") else 1)
    digest = hashlib.sha256(data).hexdigest()[:16]
    return f"| `{path.as_posix()}` | {len(data)} | {line_count} | `{digest}` |"


def build_snapshot() -> str:
    files = tracked_src_files()
    total_bytes = sum(path.stat().st_size for path in files)
    total_lines = 0
    for path in files:
        data = path.read_bytes()
        total_lines += data.count(b"\n") + (0 if not data or data.endswith(b"\n") else 1)

    rows = [file_row(path) for path in files]
    if not rows:
        rows = ["| _No tracked source files_ | 0 | 0 | `n/a` |"]

    return "\n".join(
        [
            "# Repo Source Snapshot",
            "",
            "This file is generated from tracked files in `src/`.",
            "It changes only when source inputs change.",
            "",
            "## Summary",
            "",
            f"- Tracked source files: {len(files)}",
            f"- Total source bytes: {total_bytes}",
            f"- Total source lines: {total_lines}",
            "",
            "## Files",
            "",
            "| File | Bytes | Lines | SHA-256 Prefix |",
            "|---|---:|---:|---|",
            *rows,
            "",
        ]
    )


def output_changed(content: str) -> bool:
    return not OUTPUT_PATH.exists() or OUTPUT_PATH.read_text() != content


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate src/repo_snapshot.md and optionally commit it."
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Create a signed commit only when the generated snapshot changes.",
    )
    parser.add_argument(
        "--message",
        default="update repo source snapshot",
        help="Commit message to use with --commit.",
    )
    args = parser.parse_args()

    repo_root = Path(git("rev-parse", "--show-toplevel").stdout.strip())
    original_cwd = Path.cwd()
    try:
        os.chdir(repo_root)
        content = build_snapshot()
        if not output_changed(content):
            print("src/repo_snapshot.md is already up to date")
            return 0

        OUTPUT_PATH.write_text(content)
        print("updated src/repo_snapshot.md")

        if args.commit:
            git("add", "--", OUTPUT_PATH.as_posix())
            git("commit", "-S", "-m", args.message)
            print("created signed snapshot commit")
        return 0
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    raise SystemExit(main())
