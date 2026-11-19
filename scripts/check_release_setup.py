"""Check that the release workflow is ready for trusted publishing.

The release stays dormant until the package exists. This gate keeps the tag
trigger, the separate jobs and the publishing method in place while the module
is designed. Run from the repository root.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

WORKFLOW = Path(".github/workflows/release.yml")
REQUIRED = (
    "name: Release",
    "  push:",
    "    tags:",
    "  build:",
    "  publish:",
    "id-token: write",
)


def missing(text: str, publish_command: str) -> list[str]:
    """The required fragments absent from the release workflow."""
    fragments = (*REQUIRED, publish_command)
    return [fragment for fragment in fragments if fragment not in text]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--publish-command", required=True)
    args = parser.parse_args(argv)

    if not WORKFLOW.is_file():
        print(f"error: {WORKFLOW} is missing")
        return 1

    gaps = missing(WORKFLOW.read_text(encoding="utf-8"), args.publish_command)
    for fragment in gaps:
        print(f"error: {WORKFLOW} does not contain {fragment!r}")
    if gaps:
        return 1
    print("The release workflow is ready for trusted publishing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
