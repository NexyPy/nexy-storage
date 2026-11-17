## What changed

One sentence. Name the behaviour, not the files.

## Why

Link the issue. Say what problem this solves for a person using Nexy.

## Verification

Paste the output of this command:

```text
uv run python scripts/verify.py
```

If a gate was skipped, say which one and why. A skipped gate is not a pass.

## Checklist

- [ ] The test was written before the code.
- [ ] Every added line of `src/server/nexy_storage/` runs in a test and every branch is taken.
- [ ] Hostile inputs have their own security tests.
- [ ] No character a person does not type appears in code, docs or this description.
- [ ] No AI tool or agent is named as an author, a co-author or a generator.
- [ ] Every identifier, comment and sentence is in English.
- [ ] The commit is one unit and its message says why.
- [ ] The maintainer, not the author, will review and merge this pull request.
- [ ] This pull request targets `develop`, or `main` for a release.
