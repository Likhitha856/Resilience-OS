from app.database.db import Database
from app.state.app_state import AppState
from app.engines.file_content_manager import FileContentManager

# Initialize once
db = Database()
state_instance = AppState(db)
file_manager_instance = FileContentManager(db)


def get_state():
    return state_instance


def get_file_manager():
    return file_manager_instance