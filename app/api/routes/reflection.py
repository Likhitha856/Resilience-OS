from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.api.schemas import EntryCreate, EntryResponse
from app.engines.file_content_manager import FileContentManager
from app.api.dependencies import get_file_manager, get_state
from app.state.app_state import AppState
from fastapi import Body

router = APIRouter(prefix="/reflection", tags=["Reflection"])


@router.post("", response_model=EntryResponse)
def create_reflection(
    entry: EntryCreate,
    file_manager: FileContentManager = Depends(get_file_manager)
):
    new_id = file_manager.save_entry(
        content=entry.content,
        entry_type="reflection",
        is_locked=entry.is_locked
    )

    return EntryResponse(
        id=new_id,
        entry_type="reflection",
        content=entry.content,
        created_at=datetime.now().isoformat(),
        is_locked=entry.is_locked
    )


@router.get("", response_model=list[EntryResponse])
def list_reflections(
    file_manager: FileContentManager = Depends(get_file_manager)
):
    entries = file_manager.display_entries("reflection")

    return [
        EntryResponse(
            id=e["id"],
            entry_type="reflection",
            content="",
            created_at=e["created_at"],
            is_locked=bool(e["is_locked"])
        )
        for e in entries
    ]


@router.post("/{entry_id}/open", response_model=EntryResponse)
def open_reflection(
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
        raise HTTPException(status_code=404, detail="Reflection not found")

    return EntryResponse(
        id=entry["id"],
        entry_type=entry["entry_type"],
        content=entry["content"],
        created_at=entry["created_at"],
        is_locked=bool(entry["is_locked"])
    )

@router.delete("/{entry_id}")
def delete_reflection(
    entry_id: int,
    file_manager: FileContentManager = Depends(get_file_manager)
):
    file_manager.delete_entry(entry_id)
    return {"message": "Reflection deleted"}