from fastapi import APIRouter, Depends
from app.api.schemas import StateResponse, StateUpdate
from app.state.app_state import AppState
from app.api.dependencies import get_state

router = APIRouter()


@router.get("/state", response_model=StateResponse)
def get_state_route(state: AppState = Depends(get_state)):
    return StateResponse(
        preferred_tone=state.preferred_tone,
        preferred_grounding=state.preferred_grounding,
        support_preference=state.support_preference,
        default_use_count=state.default_use_count,
        prompt_shown=state.prompt_shown,
        lock_enabled=state.feature_lock.lock_enabled
    )


@router.patch("/state", response_model=StateResponse)
def update_state(
    update: StateUpdate,
    state: AppState = Depends(get_state)
):
    if update.preferred_tone is not None:
        state.preferred_tone = update.preferred_tone

    if update.preferred_grounding is not None:
        state.preferred_grounding = update.preferred_grounding

    if update.support_preference is not None:
        state.support_preference = update.support_preference

    state.save()

    return get_state_route(state)