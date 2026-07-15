# Release process

This project publishes to PyPI via [trusted publishing](https://docs.pypi.org/trusted-publishers/):
[`.github/workflows/publish.yaml`](.github/workflows/publish.yaml) runs whenever a GitHub Release
is published and uploads the built distributions using OIDC, so no PyPI API token needs to be
stored as a secret. This is the same approach used by
[PyMUSAS](https://github.com/UCREL/pymusas/blob/main/RELEASE_PROCESS.md).

Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html), with tags of the
form `vX.Y.Z`.

## Steps

1. Set the tag as an environment variable, e.g.:

   ```bash
   export TAG=v0.2.0
   ```

2. Update the version in `pyproject.toml` (and `src/usas_validator/__init__.py`'s
   `__version__`) to match:

   ```bash
   uv version "${TAG#v}"
   ```

3. In [`CHANGELOG.md`](CHANGELOG.md), move everything under `## Unreleased` into a new
   `## [$TAG]` section, leaving `## Unreleased` empty above it.

4. Commit the version and changelog updates:

   ```bash
   git add pyproject.toml uv.lock src/usas_validator/__init__.py CHANGELOG.md
   git commit -m "Prepare for release $TAG"
   ```

5. Create and push a signed tag:

   ```bash
   git tag -s "$TAG" -m "$TAG"
   git push origin main --tags
   ```

6. Generate the release notes:

   ```bash
   make release-notes
   ```

7. On GitHub, open the pushed tag, create a release titled `$TAG`, paste in the generated
   notes, and publish it. Publishing the release triggers the `publish.yaml` workflow, which
   builds the package and uploads it to PyPI.

## If the workflow fails

Delete the tag and the GitHub release, fix the issue locally, and repeat from step 4.

After you've pushed a fix, delete the tag from your local clone with:

``` bash
git tag -l | xargs git tag -d && git fetch -t
```

## One-time setup

Before the first release, register this repository as a
[trusted publisher](https://pypi.org/manage/account/publishing/) on the `usas-validator` PyPI
project, pointing at the `UCREL/USAS-Validator` repo, the `publish.yaml` workflow, and (if used)
the deployment environment name.
