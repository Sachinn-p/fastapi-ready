from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


TEMPLATE_ROOT = Path(__file__).resolve().parent
INCLUDED_PATHS = [
    "main.py",
    "auth",
    "config",
    "core",
    "db",
    "models",
    "router",
    "schemas",
]


def create_env_example(target: Path) -> None:
    """Create a .env.example file with all required environment variables."""
    env_example_content = """# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/fastapi_db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
SQL_ECHO=false
"""
    env_example_path = target / ".env.example"
    with open(env_example_path, "w") as f:
        f.write(env_example_content)


def copy_readme(target: Path) -> None:
    """Copy the generated project README template."""
    source_readme = TEMPLATE_ROOT / "GENERATED_README.md"
    target_readme = target / "README.md"
    
    if source_readme.is_file():
        shutil.copy2(source_readme, target_readme)


def create_project(target: Path) -> None:
    if target.exists():
        raise FileExistsError(f"Target already exists: {target}")

    target.mkdir(parents=True, exist_ok=False)

    for relative_path in INCLUDED_PATHS:
        source_path = TEMPLATE_ROOT / relative_path
        destination_path = target / relative_path

        if source_path.is_dir():
            shutil.copytree(source_path, destination_path)
        elif source_path.is_file():
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)

    create_env_example(target)
    copy_readme(target)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="fastapi-ready", description="Create a new clean FastAPI backend scaffold from this template.")
    parser.add_argument("name", help="New directory name or absolute target path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.name == ".":
        print("Use a new directory name or an absolute path. '.' is the current directory and cannot be used.", file=sys.stderr)
        return 1

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
    print("  uv sync  # creates a local .venv; this is not copied from the template")
    print("  uvicorn main:app --reload")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())