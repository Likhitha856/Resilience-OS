from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas import EntryCreate, EntryResponse
from app.engines.file_content_manager import FileContentManager
from app.api.dependencies import get_file_manager, get_state
from app.state.app_state import AppState
from fastapi import Body

router = APIRouter(prefix="/vent", tags=["Vent"])


# ----------------------------
# CREATE VENT
# ----------------------------
@router.post("", response_model=EntryResponse)
def create_vent(
    entry: EntryCreate,
    file_manager: FileContentManager = Depends(get_file_manager)
):
    file_manager.save_entry(
        content=entry.content,
        entry_type="vent",
        is_locked=entry.is_locked
    )

    # fetch latest entry
    entries = file_manager.display_entries("vent")
    latest = entries[0]

    return EntryResponse(
        id=latest["id"],
        entry_type="vent",
        content=entry.content,
        created_at=latest["created_at"],
        is_locked=entry.is_locked
    )


# ----------------------------
# LIST VENTS
# ----------------------------
@router.get("", response_model=list[EntryResponse])
def list_vents(
    file_manager: FileContentManager = Depends(get_file_manager)
):
    entries = file_manager.display_entries("vent")

    return [
        EntryResponse(
            id=e["id"],
            entry_type="vent",
            content="",
            created_at=e["created_at"],
            is_locked=bool(e["is_locked"])
        )
        for e in entries
    ]


# ----------------------------
# GET SINGLE VENT
# ----------------------------
@router.post("/{entry_id}/open", response_model=EntryResponse)
def open_vent(
    entry_id: int,
    password: str | None = Body(default=None),
    state: AppState = Depends(get_state),
    file_manager: FileContentManager = Depends(get_file_manager)
):

    entry = file_manager.open_entry(entry_id, state, password)

    if entry == "PASSWORD_REQUIRED":
        raise HTTPException(status_code=401, detail="Password required")

    if entry == "INVALID_PASSWORD":
        raise HTTPException(status_code=401, detail="Invalid password")

    if not entry:
        raise HTTPException(status_code=404, detail="Vent not found")

    return EntryResponse(
        id=entry["id"],
        entry_type=entry["entry_type"],
        content=entry["content"],
        created_at=entry["created_at"],
        is_locked=bool(entry["is_locked"])
    )


# ----------------------------
# DELETE VENT (SOFT)
# ----------------------------
@router.delete("/{entry_id}")
def delete_vent(
    entry_id: int,
    file_manager: FileContentManager = Depends(get_file_manager)
):
    file_manager.delete_entry(entry_id)
    return {"message": "Vent deleted"}