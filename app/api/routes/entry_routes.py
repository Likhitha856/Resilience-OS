from fastapi import APIRouter, Depends, HTTPException, Body
from datetime import datetime

from app.api.schemas import EntryCreate, EntryResponse
from app.engines.file_content_manager import FileContentManager
from app.api.dependencies import get_file_manager, get_state, get_optional_user, get_anonymous_id
from app.state.app_state import AppState


def create_entry_router(entry_type: str):

    router = APIRouter(prefix=f"/{entry_type}", tags=[entry_type.capitalize()])

    # CREATE
    @router.post("", response_model=EntryResponse)
    def create_entry(
        entry: EntryCreate,
        user=Depends(get_optional_user),
        anon_id=Depends(get_anonymous_id),
        file_manager: FileContentManager = Depends(get_file_manager)
    ):

        new_id = file_manager.save_entry(
            content=entry.content,
            entry_type=entry_type,
            is_locked=entry.is_locked,
            user_id=user,
            anonymous_id=None if user else anon_id
        )

        return EntryResponse(
            id=new_id,
            entry_type=entry_type,
            content=entry.content,
            created_at=datetime.now().isoformat(),
            is_locked=entry.is_locked
        )

    # LIST
    @router.get("", response_model=list[EntryResponse])
    def list_entries(
        user=Depends(get_optional_user),
        anon_id=Depends(get_anonymous_id),
        file_manager: FileContentManager = Depends(get_file_manager)
    ):

        if user:
            entries = file_manager.display_entries(entry_type, user_id=user)
        else:
            entries = file_manager.display_entries(entry_type, anonymous_id=anon_id)

        return [
            EntryResponse(
                id=e["id"],
                entry_type=entry_type,
                content="",
                created_at=e["created_at"],
                is_locked=bool(e["is_locked"])
            )
            for e in entries
        ]

    # OPEN
    @router.post("/{entry_id}/open", response_model=EntryResponse)
    def open_entry(
        entry_id: int,
        password: str | None = Body(default=None),
        state: AppState = Depends(get_state),
        user=Depends(get_optional_user),
        anon_id=Depends(get_anonymous_id),
        file_manager: FileContentManager = Depends(get_file_manager)
    ):

        owner = user if user else anon_id

        entry = file_manager.open_entry(entry_id, state, password, owner)

        if entry == "PASSWORD_REQUIRED":
            raise HTTPException(status_code=401, detail="Password required")

        if entry == "INVALID_PASSWORD":
            raise HTTPException(status_code=401, detail="Invalid password")

        if not entry:
            raise HTTPException(status_code=404, detail=f"{entry_type} not found")

        return EntryResponse(
            id=entry["id"],
            entry_type=entry["entry_type"],
            content=entry["content"],
            created_at=entry["created_at"],
            is_locked=bool(entry["is_locked"])
        )

    # DELETE
    @router.delete("/{entry_id}")
    def delete_entry(
        entry_id: int,
        user=Depends(get_optional_user),
        anon_id=Depends(get_anonymous_id),
        file_manager: FileContentManager = Depends(get_file_manager)
    ):

        owner = user if user else anon_id

        file_manager.delete_entry(entry_id, owner)

        return {"message": f"{entry_type} deleted"}

    return router