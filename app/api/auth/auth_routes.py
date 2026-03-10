from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

import bcrypt

from app.api.auth.auth_models import LoginRequest, RegisterRequest, TokenResponse
from app.api.auth.auth_handler import create_access_token, create_refresh_token, verify_token
from app.api.dependencies import get_current_user, get_file_manager
from app.engines.file_content_manager import FileContentManager



router = APIRouter(prefix="/auth", tags=["Auth"])


# -----------------------------
# REGISTER
# -----------------------------
@router.post("/register")
def register(data: RegisterRequest, file_manager=Depends(get_file_manager)):

    conn = file_manager.get_connection()
    cursor = conn.cursor()

    # check if user exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (data.username,))
    existing = cursor.fetchone()

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

    cursor.execute(
        """
        INSERT INTO users (username, password_hash, created_at)
        VALUES (?, ?, ?)
        """,
        (data.username, hashed.decode(), datetime.now().isoformat())
    )

    conn.commit()

    return {"message": "User registered successfully"}


# -----------------------------
# LOGIN
# -----------------------------
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, file_manager=Depends(get_file_manager)):

    conn = file_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (data.username,)
    )

    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stored_hash = user["password_hash"]

    if not bcrypt.checkpw(data.password.encode(), stored_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token({"sub": data.username})
    refresh = create_refresh_token({"sub": data.username})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


# -----------------------------
# REFRESH TOKEN
# -----------------------------
@router.post("/refresh")
def refresh_token(refresh_token: str):

    payload = verify_token(refresh_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access = create_access_token({"sub": payload["sub"]})

    return {"access_token": access}

@router.post("/migrate")
def migrate_guest_data(
    anonymous_id: str,
    user=Depends(get_current_user),
    file_manager: FileContentManager = Depends(get_file_manager)
):

    conn = file_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE entries
        SET user_id = ?, anonymous_id = NULL
        WHERE anonymous_id = ?
        """,
        (user, anonymous_id)
    )

    conn.commit()

    return {"message": "Guest data migrated"}