# FastAPI Freelance Backend Template

This repository is a reusable FastAPI backend template for a freelancing platform. It includes:

- FastAPI with async endpoints
- PostgreSQL with SQLAlchemy 2.0 async sessions
- JWT authentication for users
- A `fastapi-ready` CLI to scaffold new projects from this template
- GitHub Actions workflows for CI and PyPI publishing with OIDC trusted publishing
- Python 3.8 support for local development, CI, and packaging

## Quick Start

Install the template command with pip:

```bash
python -m pip install .
```

Install dependencies:

```bash
uv sync
```

Run the app:

```bash
uvicorn main:app --reload
```

## Create a New Project

After installing this package, generate a fresh clean project from the template:

```bash
fastapi-ready directory_name
cd directory_name
uv sync
uvicorn main:app --reload
```

The generated project includes only the app scaffold and template files. It does not copy virtualenvs, installed libraries, or build artifacts.
After you run `uv sync`, a local `.venv/` folder will appear in the new project. That is expected and comes from the environment install step, not from the template copy.

Usage pattern:

- `fastapi-ready my-new-app` creates a new folder in the current directory
- `fastapi-ready /absolute/path/to/my-new-app` creates the project at that path
- `fastapi-ready .` is not supported because the current directory already exists

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://postgres:root@localhost:5432/users
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
SQL_ECHO=False
JWT_ALGORITHM=HS256
```

## CI

The repository includes a GitHub Actions workflow that installs dependencies and runs checks on every push and pull request.

## CD to PyPI

Publishing uses GitHub Actions OpenID Connect trusted publishing through PyPI.

When configuring the PyPI trusted publisher, use these values:

- PyPI project name: `project name`
- Owner: `owner`
- Repository name: `repository`
- Workflow name: `workflow.yml`
- Environment name: `pypi`

The publishing workflow lives at `.github/workflows/workflow.yml`.

## Files

- `.github/workflows/ci.yml` - test workflow
- `.github/workflows/workflow.yml` - PyPI publish workflow

## Versioning

Release versions are published from `pyproject.toml`. Bump the version before each PyPI release to avoid file reuse errors.