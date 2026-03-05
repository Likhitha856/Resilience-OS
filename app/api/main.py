from fastapi import FastAPI
from app.api.routes import state
from app.api.routes import vent
from app.api.routes import reflection
from app.api.routes import lock

app = FastAPI(title="Resilience OS API")

app.include_router(state.router)
app.include_router(vent.router)
app.include_router(reflection.router)
app.include_router(lock.router)

@app.get("/")
def root():
    return {"message": "Resilience OS Backend Running"}