# Hellbox

A modular, editor-agnostic build system for font development. Tasks are composed
of "chutes" — single-operation modules chained together with `>>`.

## Setup

```sh
make init  # runs uv sync + lefthook install
```

## Common commands

```sh
uv run pytest tests        # run tests
uv run ruff check .        # lint Python
uv run ruff format .       # format Python
uv run mdformat .          # format Markdown
shfmt -w <file>            # format a shell file
uv run lefthook install    # (re)install git hooks
```

## Python environment

Do not call `python` or `python3` directly — asdf manages Python here and
requires a `.tool-versions` entry that isn't set for this project. Always
prefix with `uv run`.

## Pre-commit hooks (lefthook)

Hooks are defined in `lefthook.yml` and installed as a Python package via uv
(not the system binary). On commit, lefthook automatically formats staged
`.py`, `.md`, and `.sh` files and re-stages the results.

If the hooks aren't firing, run `uv run lefthook install`.

## CI

Two jobs in `.github/workflows/test.yml`:

- **lint** — runs once; checks Python formatting + linting (ruff), Markdown
  (mdformat), and shell (shfmt). Markdown and shell checks use
  `git ls-files | xargs` to avoid descending into `.venv`.
- **test** — runs against Python 3.11, 3.12, and 3.13.

## Architecture

- `Hellbox` — class-level task registry; used as a context manager to define tasks
- `Task` — holds a chain of chutes and optional requirements (other task names)
- `Chute` — base class for pipeline steps; `>>` wires chutes together
- `ReadFiles` / `WriteFiles` — built-in chutes for I/O; exposed as `task.read()` / `task.write()`
- `Autoimporter` — discovers installed packages via `importlib.metadata` and
  imports them into the caller's namespace; called via `Hellbox.autoimport()`

## Package

No runtime dependencies. Version is defined in `hellbox/__version__.py` and
read dynamically by the build system via `[tool.setuptools.dynamic]`.
