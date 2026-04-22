from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import create_access_token, hash_password, verify_password
from db.database import get_db
from models.users import User
from schemas.users import LoginRequest, Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["AUTHENTICATION"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> User:
    result = await db.execute(select(User).where(User.email == payload.email))
    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(email=payload.email, password=hash_password(payload.password.get_secret_value()))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=Token)
async def login_user(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> Token:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(payload.password.get_secret_value(), user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.id)
    return Token(access_token=token)
