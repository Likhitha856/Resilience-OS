from fastapi import FastAPI
from app.api.routes import state
from app.api.routes import lock
from app.api.auth.auth_routes import router as auth_router
from app.api.routes.entry_routes import create_entry_router

app = FastAPI(title="Resilience OS API")

app.include_router(state.router)
app.include_router(create_entry_router("vent"))
app.include_router(create_entry_router("reflection"))
app.include_router(lock.router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Resilience OS Backend Running"}