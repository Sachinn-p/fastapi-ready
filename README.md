# FastAPI Freelance Backend Template

This repository is a reusable FastAPI backend template for a freelancing platform. It includes:

- FastAPI with async endpoints
- PostgreSQL with SQLAlchemy 2.0 async sessions
- JWT authentication for users
- A `fastapi-ready` CLI to scaffold new projects from this template
- GitHub Actions workflows for CI and PyPI publishing with OIDC trusted publishing

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

After installing this package, generate a fresh project from the template:

```bash
fastapi-ready my-new-app
cd my-new-app
uv sync
uvicorn main:app --reload
```

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