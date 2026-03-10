from app.database.db import Database
from app.state.app_state import AppState
from app.engines.file_content_manager import FileContentManager
from fastapi import Header,HTTPException,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from app.api.auth.auth_handler import verify_token
import uuid

# Initialize once
db = Database()
state_instance = AppState(db)
file_manager_instance = FileContentManager(db)
security=HTTPBearer()

def get_state():
    return state_instance


def get_file_manager():
    return file_manager_instance


def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)):

    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload["sub"]

    
def get_optional_user(authorization: str = Header(None)):

    if not authorization:
        return None

    try:

        token = authorization.split(" ")[1]

        payload = verify_token(token)

        if payload:
            return payload["sub"]

    except:
        pass

    return None

def get_anonymous_id(x_anonymous_id: str = Header(None)):

    if x_anonymous_id:
        return x_anonymous_id

    return str(uuid.uuid4())

