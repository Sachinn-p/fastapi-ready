# FastAPI Freelance Backend Template

This repository is a reusable FastAPI backend template for a freelancing platform. It includes:

- FastAPI with async endpoints
- PostgreSQL with SQLAlchemy 2.0 async sessions
- JWT authentication for users
- A `fastapi-ready` CLI to scaffold new projects from this template
- GitHub Actions workflows for CI and PyPI publishing with OIDC trusted publishing
- Python 3.8 support for local development, CI, and packaging

---

## For Users of This Template

If you've installed this package with `pip install fastapi-ready`, go to **"Create a New Project"** section below.

If you've cloned or downloaded this repository to develop or modify the template itself, see **"For Template Developers"** at the end.

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

## Helper Tools

### Verify Scaffold Cleanliness

Use `verify_scaffold.py` to ensure a generated project contains only expected files:

```bash
python verify_scaffold.py /path/to/generated/project
```

This checks for:
- Correct top-level files (`.env.example`, `main.py`, module directories)
- No forbidden patterns (`.venv`, `__pycache__`, `.egg-info`, etc.)
- File and directory counts

Example output:
```
✅ Scaffold verification passed!
📊 Statistics:
   Files: 12
   Directories: 7
```

## Generated Project Structure

When you run `fastapi-ready my-app`, the generated project includes:

```
my-app/
├── .env.example           # Template environment variables
├── main.py               # FastAPI application entry point
├── auth/                 # Authentication module
│   └── auth.py          # JWT & password utilities
├── config/              # Configuration module
│   ├── __init__.py
│   └── settings.py      # Environment-based settings
├── core/                # Core utilities
│   └── deps.py          # Dependency injection
├── db/                  # Database module
│   ├── __init__.py
│   └── database.py      # SQLAlchemy async setup
├── models/              # Database models
│   └── users.py        # User model
├── router/              # API routes
│   ├── __init__.py
│   └── auth.py         # Auth endpoints
└── schemas/             # Pydantic schemas
    └── users.py        # User request/response schemas
```

### First Steps After Generation

1. **Create environment file:**

   ```bash
   cp .env.example .env
   ```

   Update with your database URL, secret key, and other settings.

2. **Install dependencies:**

   ```bash
   uv sync
   ```

   This creates a `.venv/` folder locally (not copied from the template).

3. **Run the app:**

   ```bash
   uvicorn main:app --reload
   ```

   The dev server will start at `http://localhost:8000`

4. **Verify setup:**

   Visit `http://localhost:8000/docs` for interactive API documentation.

### Environment Variables

The generated project requires these environment variables (create a `.env` file):

```env
# Database (PostgreSQL + asyncpg)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/db_name

# Security
SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database logging
SQL_ECHO=false
```

All variables are **required**; the app will fail to start if any are missing or empty.

### Database Setup

The generated project uses SQLAlchemy 2.0 with async/await:

```bash
# Create PostgreSQL database
createdb fastapi_db

# Export connection string
export DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/fastapi_db

# Tables are created automatically on first app startup
```

### Authentication Flow

The generated project includes JWT-based authentication:

- **Register:** `POST /auth/register` - Create a new user (password hashed with bcrypt)
- **Login:** `POST /auth/login` - Get JWT token (valid for 60 min by default)
- **Protected endpoints:** Include `Authorization: Bearer <token>` header

Example:
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -d "username=user@example.com&password=secure123"
```

---

## For Template Developers

This section is for developers who want to modify, test, or publish this template package.

### Local Development

```bash
git clone <repo>
cd backend
uv sync
uvicorn main:app --reload
```

### Testing Template Generation

After making changes to the template:

```bash
# Reinstall the package in editable mode
uv pip install -e . --no-deps

# Generate a test scaffold
fastapi-ready /tmp/test-app

# Verify the scaffold
python verify_scaffold.py /tmp/test-app
```

### Publishing to PyPI

1. **Update version** in `pyproject.toml`
2. **Commit and tag:**
   ```bash
   git add .
   git commit -m "Release v0.2.0"
   git tag v0.2.0
   git push origin main --tags
   ```
3. **Trigger workflow:** Push to `main` with a new version tag
4. **Monitor:** Check GitHub Actions for build/publish status

The workflow automatically publishes to PyPI using OIDC trusted publishing (no API tokens needed).

### Project Structure

- `fastapi_ready.py` - Template generator CLI (entry point)
- `verify_scaffold.py` - Scaffold validation tool
- `main.py`, `auth/`, `config/`, etc. - Template scaffold files
- `.github/workflows/` - CI/CD pipelines

### Adding New Template Files

1. Create the file/directory in this repo
2. Add the path to `INCLUDED_PATHS` in `fastapi_ready.py`
3. Update `EXPECTED_SCAFFOLD_FILES` in `verify_scaffold.py`
4. Test with: `fastapi-ready test-proj && python verify_scaffold.py test-proj`