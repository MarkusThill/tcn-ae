# tcn-ae

A temporal convolutional autoencoder for anomaly detection in multivariate time series.

This is a reference implementation of:

> Markus Thill, Wolfgang Konen, Hao Wang, Thomas Bäck.
> [*Temporal convolutional autoencoder for unsupervised anomaly detection in time series.*](https://doi.org/10.1016/j.asoc.2021.107751)
> Applied Soft Computing 112 (2021), 107751.

> [!NOTE]
> Early development — the package is being built up step by step and the public API is not
> stable yet.

## Installation

```bash
pip install tcn-ae
```

This installs Keras with the **TensorFlow backend**, matching the paper's original
implementation.

Keras 3 is multi-backend, so PyTorch can be used instead:

```bash
pip install "tcn-ae[torch]"
KERAS_BACKEND=torch python your_script.py
```

TensorFlow is a required dependency rather than an extra, so `tcn-ae[torch]` installs both.
To make the backend choice permanent, set `"backend": "torch"` in `~/.keras/keras.json`.

There is one implementation, written against the Keras 3 API — the backend is chosen at
install and run time, not by a separate code path.

## Documentation

<https://markusthill.github.io/tcn-ae/>

## Citing

If you use this software, please cite the paper above. GitHub reads
[CITATION.cff](CITATION.cff), so the "Cite this repository" button produces BibTeX for both
the software and the paper.

## Development

The project uses [uv](https://docs.astral.sh/uv/) for environments and packaging. In a
Codespace or devcontainer everything below is already provisioned by
[.devcontainer/post-create.sh](.devcontainer/post-create.sh).

```bash
uv sync                     # create .venv from uv.lock, incl. the dev group
uv run prek install --hook-type pre-commit --hook-type commit-msg
```

The dev interpreter is pinned to Python 3.13 (`.python-version`). The *package* supports
Python 3.11+, which is what CI's matrix exercises — keep those two numbers distinct.

### Everyday commands

| Task | Command |
| --- | --- |
| Run tests | `uv run pytest` |
| Tests with coverage gate | `uv run pytest --cov` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run pyrefly check` |
| Workflow security lint | `uv run zizmor .github/workflows` |
| Docs preview | `uv run --group docs zensical serve` |
| Docs build | `uv run --group docs zensical build` |

### Type checking

[pyrefly](https://pyrefly.org/) is the authority and gates CI and commits.
[ty](https://github.com/astral-sh/ty) is also installed and can be run with
`uv run ty check`, but it is **experimental and advisory only** — it never blocks a commit or
a build, and where the two disagree, pyrefly wins.

### Git hooks (prek)

Hooks are managed by [prek](https://github.com/j178/prek), a drop-in replacement for
`pre-commit` that reads the same [.pre-commit-config.yaml](.pre-commit-config.yaml).

```bash
uv run prek run --all-files   # run every hook against the whole repo
uv run prek auto-update       # bump pinned hook revisions
```

On commit this runs file hygiene checks, `ruff check --fix`, `ruff format`, `pyrefly`,
`nbstripout` (strips notebook outputs), and `zizmor`. On `commit-msg` it validates the
message with commitizen.

### Commit messages (commitizen)

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) and are
enforced by the `commit-msg` hook.

```bash
uv run cz commit            # interactive, guided commit message
```

The commit type determines the next version: `fix:` → patch, `feat:` → minor. With
`major_version_zero = true` the project stays on `0.x` until you deliberately go to 1.0.

`cz bump` writes the version to `[project] version` in `pyproject.toml` and to `uv.lock`
(`version_provider = "uv"`); the package reads it back at runtime via `importlib.metadata`.
**Do not** switch to a dynamic/hatch version, it would break `cz bump`.

### Trusted Publishing configuration

Already configured on both registries — nothing to do for a normal release. This is the
trust relationship that lets the workflows publish without any API token stored in the repo.

| Field | PyPI | TestPyPI |
| --- | --- | --- |
| PyPI project name | `tcn-ae` | `tcn-ae` |
| Owner | `MarkusThill` | `MarkusThill` |
| Repository | `tcn-ae` | `tcn-ae` |
| Workflow | `release.yml` | `release-testpypi.yml` |
| Environment | `pypi` | `testpypi` |

Renaming the repository, the workflow file, or the GitHub environment breaks the match and
publishing fails with an OIDC error — update the publisher on the registry to match. The
same table applies when setting up a fork: before a project exists, it is added under
*Publishing* → *Add a pending publisher*; afterwards it lives in the project's own
*Publishing* settings.

### Cutting a release to PyPI

From a clean `main` that is up to date with `origin`:

```bash
# 1. Preview the version derived from the commits since the last tag
uv run cz bump --dry-run

# 2. Bump: updates pyproject.toml, uv.lock and CHANGELOG.md, commits, creates the v* tag
uv run cz bump

# 3. Push the commit *and* the tag
git push --follow-tags

# 4. Confirm the tag actually arrived — this is where releases usually fail silently
git ls-remote --tags origin

# 5. Watch the release run
gh run watch
```

Step 3 is the one that catches people: a plain `git push` does **not** push tags. The bump
commit lands, `main` looks correct, and nothing is ever released. If step 4 prints no tag,
push it explicitly:

```bash
git push origin "v$(uv run cz version --project)"
```

The tag push triggers [release.yml](.github/workflows/release.yml): build → `twine check` →
publish to PyPI via Trusted Publishing (OIDC, no API token stored) → GitHub release with the
artifacts attached.

> [!WARNING]
> `annotated_tag = true` in `[tool.commitizen]` is load-bearing. `git push --follow-tags`
> pushes *annotated* tags only, and commitizen creates lightweight ones by default.

#### If a release fails

A version number is consumed permanently on PyPI — a deleted release cannot be re-uploaded
under the same version. If the run failed **before** anything was uploaded (a bad publisher
config, a failing build), drop the tag, fix, and retag:

```bash
git push --delete origin v0.1.0
git tag -d v0.1.0
```

If the upload already succeeded, do not try to reuse the version — bump to a new one.

### Rehearsing a release on TestPyPI

TestPyPI exists purely to prove the procedure works before it matters. Run
[release-testpypi.yml](.github/workflows/release-testpypi.yml) manually from the Actions tab;
it exercises the same build → `twine check` → OIDC publish path as a real release.

It does **not** cover the tag trigger, `cz bump`, or GitHub release creation — those only run
in [release.yml](.github/workflows/release.yml).

Optional, if verifying the upload is installable: an extra index is required, because
TestPyPI's own `tensorflow` stops at 1.0.0 and `keras` at 2.0.0.

```bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ tcn-ae
```

### Notebooks

Notebooks in `notebooks/` are executed in CI with
[nbmake](https://github.com/treebeardtech/nbmake) so the examples cannot silently rot:

```bash
uv run pytest --nbmake notebooks/
```

Outputs are stripped on commit by `nbstripout`, so keep notebooks free of large embedded
results in git.
