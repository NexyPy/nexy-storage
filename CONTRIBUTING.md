# Contributing to nexy-storage

Read AGENTS.md first. It is the contract for every change in this repository.

## Setup

```bash
uv sync --frozen --group dev
git config core.hooksPath .githooks
```

The hooks check the commit message, the identity and the staged files. Never use `--no-verify`.

## Work

1. Branch from `develop` with `feature/<issue>`, `fix/<issue>`, `docs/<issue>` or `perf/<issue>`.
   `main` is reserved for releases.
2. Read the issue and research the question with primary sources. Check versions and advisories
   with commands, not from memory.
3. Write a failing test. Write the least code that passes. Refactor.
4. Run `uv run python scripts/verify.py` from the root.
5. Open a pull request against `develop` with the gate output. One purpose, one unit, one file per
   commit.
6. Wait for the maintainer review. Do not approve or merge your own pull request. The maintainer
   validates the work and merges it.

## Language and characters

Code, comments, identifiers, docs, issues, pull requests and commit messages are in English.
Use only characters typed on an English or French keyboard. No emoji. The gate
`scripts/check_human_characters.py` refuses generated characters in files and commit messages.

## Attribution

No AI tool or agent is an author, a co-author or a generator. Do not add a `Co-authored-by`
trailer for Codex, Freebuff, Claude Code, OpenCode or any other tool. Do not add a
`Generated with` footer. GitHub counts a trailer as a contributor forever.

`scripts/check_attribution.py` runs in `.githooks/commit-msg` and in CI on every new commit. A
commit with AI attribution is rejected. Fix the commit instead of bypassing the hook.
