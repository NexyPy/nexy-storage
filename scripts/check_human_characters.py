"""Reject characters a person does not type in tracked files and commit messages.

The forbidden set is written as code points so this file follows its own rule. French accented
letters and ordinary punctuation are allowed. Run with --staged in the pre-commit hook and with
--message-file in the commit-msg hook.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

FORBIDDEN = frozenset(
    chr(code)
    for code in (
        *(0x2014, 0x2013, 0x2192, 0x2190, 0x21D2, 0x2026),
        *(0x201C, 0x201D, 0x2018, 0x2019, 0x2022, 0x00B7, 0x2248, 0x00D7),
        *(0x2713, 0x2714, 0x2717, 0x26A0, 0x2605, 0x2500, 0x2502, 0x251C, 0x2514),
        *(0x00A0, 0x200B, 0x200C, 0x200D, 0xFEFF),
    )
)

TEXT_SUFFIXES = frozenset(
    {".md", ".py", ".toml", ".ts", ".json", ".yml", ".yaml", ".txt", ".sh", ".lock"}
)
TEXT_NAMES = frozenset({".gitignore", ".python-version"})


def found(text: str) -> list[str]:
    """The forbidden code points in a piece of text, sorted and without duplicates."""
    return sorted({f"U+{ord(char):04X}" for char in text if char in FORBIDDEN})


def is_text(path: Path) -> bool:
    """Whether a tracked path is a text file this gate reads."""
    return path.name in TEXT_NAMES or path.suffix in TEXT_SUFFIXES


def git_files(root: Path, staged: bool) -> list[Path]:
    """Tracked files, or the files added to the index when staged is true."""
    command = (
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"]
        if staged
        else ["git", "ls-files"]
    )
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=True)
    return [Path(line) for line in result.stdout.splitlines() if line]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--message-file", type=Path)
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--message-only", action="store_true")
    args = parser.parse_args(argv)

    errors: list[str] = []
    if not args.message_only:
        for path in git_files(args.root, args.staged):
            if not is_text(path):
                continue
            full = args.root / path
            if full.is_file():
                errors.extend(f"{path}: {code}" for code in found(full.read_text(encoding="utf-8")))
    if args.message_file is not None:
        message = args.message_file.read_text(encoding="utf-8")
        errors.extend(f"commit message: {code}" for code in found(message))

    for error in errors:
        print(f"error: {error}")
    if errors:
        print(f"{len(errors)} forbidden character(s) found. Use a keyboard character.")
        return 1
    print("Every character is one a person types")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
