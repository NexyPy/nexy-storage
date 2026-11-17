"""Fail when a function or a class grows past the Nexy limits.

The limits are in AGENTS.md: a function aims for fewer than 20 lines and a class for fewer than
10 methods. A folder that mixes intentions is named utils, misc or common, which is refused here.
"""

from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "src/server/nexy_storage"
MAX_FUNCTION_LINES = 20
MAX_METHODS = 10
FORBIDDEN_FOLDERS = frozenset({"utils", "misc", "common"})


def package_files() -> list[Path]:
    """The Python files of the package that git tracks."""
    result = subprocess.run(
        ["git", "ls-files", PACKAGE], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return [ROOT / line for line in result.stdout.splitlines() if line.endswith(".py")]


def issues(path: Path) -> list[str]:
    """One sentence per structure limit this file breaks."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            length = node.end_lineno - node.lineno + 1
            if length > MAX_FUNCTION_LINES:
                found.append(f"{path.name}:{node.lineno} {node.name} has {length} lines")
        if isinstance(node, ast.ClassDef):
            methods = sum(
                isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) for child in node.body
            )
            if methods > MAX_METHODS:
                found.append(f"{path.name}:{node.lineno} {node.name} has {methods} methods")
    for folder in FORBIDDEN_FOLDERS:
        if folder in path.parts:
            found.append(f"{path.relative_to(ROOT)} sits in a {folder} folder")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if not args.check:
        print("Use --check to run the gate")
        return 2
    found = [issue for path in package_files() for issue in issues(path)]
    for issue in found:
        print(f"error: {issue}")
    if found:
        return 1
    print("Structure limits respected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
