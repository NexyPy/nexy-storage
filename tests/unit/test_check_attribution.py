"""The attribution gate keeps AI tools out of the contributor graph."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_attribution.py"


def _run(message: str, path: Path) -> subprocess.CompletedProcess[str]:
    path.write_text(message, encoding="utf-8")
    command = [sys.executable, str(SCRIPT), "--message-file", str(path)]
    return subprocess.run(command, capture_output=True, text=True, check=False)


def test_message_with_ai_co_author_is_rejected(tmp_path: Path):
    message = "feat: add port\n\nCo-authored-by: Claude <claude@anthropic.com>\n"
    result = _run(message, tmp_path / "message")
    assert result.returncode == 1


def test_message_with_human_trailer_is_accepted(tmp_path: Path):
    message = "feat: add port\n\nSigned-off-by: Espoir <espoir@example.com>\n"
    result = _run(message, tmp_path / "message")
    assert result.returncode == 0


def test_message_with_dependabot_co_author_is_accepted(tmp_path: Path):
    message = (
        "chore(deps): bump pnpm/action-setup\n\n"
        "Co-authored-by: dependabot[bot] "
        "<49699333+dependabot[bot]@users.noreply.github.com>\n"
    )
    result = _run(message, tmp_path / "message")
    assert result.returncode == 0


def test_message_with_spoofed_dependabot_domain_is_rejected(tmp_path: Path):
    message = (
        "chore(deps): bump pnpm/action-setup\n\n"
        "Co-authored-by: dependabot[bot] "
        "<1+dependabot[bot]@evilusers.noreply.github.com>\n"
    )
    result = _run(message, tmp_path / "message")
    assert result.returncode == 1
