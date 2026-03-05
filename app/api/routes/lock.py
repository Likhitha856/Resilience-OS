from fastapi import APIRouter, Depends, HTTPException
import bcrypt

from app.api.schemas import LockCreate, LockVerify, LockStatus
from app.api.dependencies import get_state
from app.state.app_state import AppState

router = APIRouter(prefix="/lock", tags=["Feature Lock"])


# -------------------------
# GET LOCK STATUS
# -------------------------
@router.get("", response_model=LockStatus)
def lock_status(state: AppState = Depends(get_state)):
    return LockStatus(enabled=state.feature_lock.lock_enabled)


# -------------------------
# SET LOCK
# -------------------------
@router.post("/set")
def set_lock(data: LockCreate, state: AppState = Depends(get_state)):

    if state.feature_lock.lock_enabled:
        raise HTTPException(status_code=400, detail="Lock already enabled")

    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

    state.feature_lock._hashed_pin = hashed
    state.feature_lock.lock_enabled = True

    state.save()

    return {"message": "Lock enabled"}


# -------------------------
# VERIFY LOCK
# -------------------------
@router.post("/verify")
def verify_lock(data: LockVerify, state: AppState = Depends(get_state)):

    if not state.feature_lock.lock_enabled:
        return {"verified": True}

    if bcrypt.checkpw(data.password.encode(), state.feature_lock._hashed_pin):
        return {"verified": True}

    raise HTTPException(status_code=401, detail="Invalid password")


# -------------------------
# DELETE LOCK
# -------------------------
@router.delete("")
def delete_lock(data: LockVerify, state: AppState = Depends(get_state)):

    if not state.feature_lock.lock_enabled:
        return {"message": "No lock set"}

    if not bcrypt.checkpw(data.password.encode(), state.feature_lock._hashed_pin):
        raise HTTPException(status_code=401, detail="Invalid password")

    state.feature_lock._hashed_pin = None
    state.feature_lock.lock_enabled = False

    state.save()

    return {"message": "Lock removed"}