"""The version imported by users is the version the build publishes."""

import tomllib
from pathlib import Path

import nexy_storage

ROOT = Path(__file__).resolve().parents[2]


def test_version_matches_pyproject():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert nexy_storage.__version__ == data["project"]["version"]
