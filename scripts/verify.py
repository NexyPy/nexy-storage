"""Run every local quality gate in order, stopping at the first failure.

Usage: python scripts/verify.py
The network audit stays in CI; every other gate runs here with the exact CI commands.
"""

import argparse
import subprocess
import sys

GATES: list[tuple[str, list[str]]] = [
    ("lint", ["-m", "ruff", "check", "src/", "tests/", "scripts/"]),
    ("format", ["-m", "ruff", "format", "src/", "tests/", "scripts/", "--check"]),
    ("typecheck", ["-m", "mypy", "src/server/nexy_storage", "--strict"]),
    ("structure", ["scripts/audit_structure.py", "--check"]),
    ("characters", ["scripts/check_human_characters.py"]),
    (
        "release",
        [
            "scripts/check_release_setup.py",
            "--publish-command",
            "uv publish --trusted-publishing always",
        ],
    ),
    (
        "test",
        [
            "-m",
            "pytest",
            "tests/",
            "-q",
            "--cov=nexy_storage",
            "--cov-report=json:.coverage.json",
        ],
    ),
    ("diff-coverage", ["scripts/check_diff_coverage.py", "--report", ".coverage.json"]),
    ("security", ["-m", "bandit", "-r", "src/server/nexy_storage/", "-c", ".bandit", "-q"]),
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default="origin/develop")
    options = parser.parse_args(argv)
    gates = [
        (name, [*args, "--base", options.base] if name == "diff-coverage" else args)
        for name, args in GATES
    ]
    for name, args in gates:
        print(f"[verify] {name}: python {' '.join(args)}")
        result = subprocess.run([sys.executable, *args], check=False)
        if result.returncode != 0:
            print(f"[verify] FAILED at {name}")
            return result.returncode
        print(f"[verify] {name}: ok")
    print("[verify] all gates passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
