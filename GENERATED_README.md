# FastAPI Backend Project

A FastAPI backend generated from the `fastapi-ready` template.

## Quick Start

### 1. Install Dependencies

```bash
uv sync
```

This creates a local `.venv/` with all dependencies.

### 2. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/db_name
SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
SQL_ECHO=false
```

### 3. Set Up Database

Create a PostgreSQL database:

```bash
createdb your_database_name
```

Export the connection string (or add to `.env`):

```bash
export DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/your_database_name
```

### 4. Run the Application

```bash
uvicorn main:app --reload
```

The app will start at `http://localhost:8000`

Access the interactive API docs at `http://localhost:8000/docs`

## Project Structure

```
.
├── .env.example           # Environment variable template
├── main.py               # FastAPI application entry point
├── auth/                 # Authentication module
│   └── auth.py          # JWT & password utilities
├── config/              # Configuration
│   ├── __init__.py
│   └── settings.py      # Environment settings
├── core/                # Core utilities
│   └── deps.py          # Dependency injection
├── db/                  # Database
│   ├── __init__.py
│   └── database.py      # SQLAlchemy async setup
├── models/              # Database models
│   └── users.py        # User model
├── router/              # API routes
│   ├── __init__.py
│   └── auth.py         # /auth endpoints
└── schemas/             # Pydantic schemas
    └── users.py        # Request/response schemas
```

## API Endpoints

### Authentication

- `POST /auth/register` - Create a new user
  ```json
  {"email": "user@example.com", "password": "secure123"}
  ```

- `POST /auth/login` - Get JWT token
  ```json
  {"username": "user@example.com", "password": "secure123"}
  ```

### Protected Endpoints

Include the JWT token in the `Authorization` header:

```bash
Authorization: Bearer <your_jwt_token>
```

## Environment Variables

All variables are **required**:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL + asyncpg | `postgresql+asyncpg://user:pass@localhost/db` |
| `SECRET_KEY` | JWT signing key | `your-secret-key-change-in-production` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token TTL | `60` |
| `SQL_ECHO` | Log SQL queries | `false` |

## Development

### Run Tests

```bash
pytest
```

### Format Code

```bash
black .
```

### Lint

```bash
flake8 .
```

## Troubleshooting

### "Module not found" errors

Ensure dependencies are installed:
```bash
uv sync
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Database connection errors

- Verify PostgreSQL is running
- Check `DATABASE_URL` format in `.env`
- Ensure the database exists: `createdb your_database_name`

### 500 errors on startup

- Check that all environment variables are set and non-empty
- Review error logs in terminal output

## Next Steps

1. Define your own database models in `models/`
2. Create API routes in `router/`
3. Update `schemas/` for request/response validation
4. Add business logic modules as needed
5. Deploy to your hosting platform

## License

[Add your license here]
