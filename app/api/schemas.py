from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel



# -------------------------
# STATE
# -------------------------

class StateResponse(BaseModel):
    preferred_tone: str
    preferred_grounding: List[str]
    support_preference: str
    default_use_count: int
    prompt_shown: bool
    lock_enabled: bool


class StateUpdate(BaseModel):
    preferred_tone: Optional[str] = None
    preferred_grounding: Optional[List[str]] = None
    support_preference: Optional[str] = None


# -------------------------
# ENTRY
# -------------------------

class EntryCreate(BaseModel):
    content: str
    is_locked: bool = False


class EntryResponse(BaseModel):
    id: int
    entry_type: str
    content: str
    created_at: str
    is_locked: bool


# -------------------------
# LOCK
# -------------------------

class LockSet(BaseModel):
    password: str


class LockVerify(BaseModel):
    password: str


class LockCreate(BaseModel):
    password: str


class LockStatus(BaseModel):
    enabled: bool