from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


TEMPLATE_ROOT = Path(__file__).resolve().parent
IGNORED_DIRS = {".git", ".venv", "__pycache__", "backend.egg-info"}
IGNORED_FILES = {"uv.lock"}


def _ignore_patterns(_: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in IGNORED_DIRS or name in IGNORED_FILES or name.endswith(".pyc"):
            ignored.add(name)
    return ignored


def create_project(target: Path) -> None:
    if target.exists():
        raise FileExistsError(f"Target already exists: {target}")

    target.mkdir(parents=True, exist_ok=False)
    shutil.copytree(
        TEMPLATE_ROOT,
        target,
        dirs_exist_ok=True,
        ignore=_ignore_patterns,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="fastapi-ready", description="Create a new FastAPI backend from this template.")
    parser.add_argument("name", help="Project name or target path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    raw_target = Path(args.name).expanduser()
    target = raw_target if raw_target.is_absolute() else Path.cwd() / raw_target

    try:
        create_project(target)
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Created project at: {target}")
    print("Next:")
    print(f"  cd {target}")
    print("  uv sync")
    print("  uvicorn main:app --reload")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())