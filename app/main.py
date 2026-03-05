from database.db import Database
from state.app_state import AppState
from flow.main_flow import MainFlow

db = Database()
state = AppState(db)

flow = MainFlow(state)
flow.start_app()