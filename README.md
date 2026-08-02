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

### Commits and releases (commitizen)

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) and are
enforced by the `commit-msg` hook. Use the prompt if you like:

```bash
uv run cz commit            # interactive, guided commit message
uv run cz bump              # bump version, update CHANGELOG.md, create the v* tag
git push --follow-tags
```

`cz bump` derives the new version from the commits since the last tag, writes it to
`[project] version` in `pyproject.toml` and to `uv.lock` (`version_provider = "uv"`), and
updates `CHANGELOG.md`. The package exposes that same version at runtime via
`importlib.metadata`, so there is a single source of truth — **do not** switch back to a
dynamic/hatch version, it would break `cz bump`.

Pushing the tag triggers [.github/workflows/release.yml](.github/workflows/release.yml),
which builds, publishes to PyPI via Trusted Publishing (OIDC — no API token is stored), and
creates the GitHub release.

### Publishing setup (one-time)

Both registries use Trusted Publishing, so no API token is ever stored. PyPI supports
*pending* publishers, meaning the project does not have to exist yet.

On [pypi.org](https://pypi.org) and [test.pypi.org](https://test.pypi.org) — separate sites
needing separate accounts, both with 2FA — go to *Publishing* → *Add a pending publisher*:

| Field | PyPI | TestPyPI |
| --- | --- | --- |
| PyPI project name | `tcn-ae` | `tcn-ae` |
| Owner | `MarkusThill` | `MarkusThill` |
| Repository | `tcn-ae` | `tcn-ae` |
| Workflow | `release.yml` | `release-testpypi.yml` |
| Environment | `pypi` | `testpypi` |

Then create matching GitHub environments under *Settings* → *Environments*, and enable Pages
with "GitHub Actions" as the source.

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
