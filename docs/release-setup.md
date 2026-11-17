# Release setup for nexy-storage

This repository is in design phase. The release workflow is prepared but no release is published
yet. This page records the external setup needed for the first release to PyPI.

## What is in the repository

- `.github/workflows/release.yml` builds the distributions and publishes them when a version tag
  is pushed to `main`.
- The build and publish jobs are separate. The publish job has only `id-token: write` and uses the
  `pypi` GitHub environment.
- No API token is stored in the repository.

## Setup on PyPI

1. Sign in to PyPI with an account that can manage the `nexy-storage` project.
2. Open the account Publishing page and add a pending publisher for a project that does not exist
   yet, or the Publishing page of the project if it exists.
3. Use these values:
   - PyPI project name: `nexy-storage`
   - Owner: `NexyPy`
   - Repository name: `nexy-storage`
   - Workflow filename: `release.yml`
   - Environment: `pypi`
4. A pending publisher does not reserve the name until the first upload. Create it close to the
   first release, not months in advance.

## Setup on GitHub

1. Create an environment named `pypi` in the repository settings. Add required reviewers if the
   maintainer wants a manual gate before publishing.
2. Tag a commit already on `main` with `v<major>.<minor>.<patch>` and push the tag.

## What happens on a tag

1. The build job checks that the commit is on `main`, that the tag matches the package version,
   builds the sdist and wheel, and smoke tests both by importing `nexy_storage`.
2. The publish job exchanges the GitHub OIDC token for a short-lived PyPI token and uploads the
   distributions with `uv publish --trusted-publishing always`.
3. The release job creates the GitHub release from the tag.

## Sources

- https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/
- https://docs.pypi.org/trusted-publishers/adding-a-publisher/
