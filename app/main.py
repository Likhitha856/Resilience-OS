from state.app_state import AppState
from flow.main_flow import MainFlow

state=AppState()
flow=MainFlow(state=state)
flow.start_app()