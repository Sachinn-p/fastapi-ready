from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from db.database import init_db
from router.auth import router as auth_router

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("backend.main:logs")


@asynccontextmanager
async def lifespan(app: FastAPI):
	logger.info("Initializing database schema")
	await init_db()
	yield


app = FastAPI(title="FastAPI ", version="1.0.0", lifespan=lifespan)

app.include_router(auth_router)


@app.get("/")
async def root() -> dict[str, str]:
	return {"FASTAPI-BACKEND + PGSQL + SQLALCHEMY ": "ok"}


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(_request: Request, exc: SQLAlchemyError) -> JSONResponse:
	logger.exception("Database error", exc_info=exc)
	return JSONResponse(status_code=500, content={"detail": "Database error"})


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
	logger.exception("Unhandled error", exc_info=exc)
	return JSONResponse(status_code=500, content={"detail": "Internal server error"})
