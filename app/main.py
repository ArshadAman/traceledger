# App entry point
from fastapi import FastAPI
from app.api.routes import router as api_router
from prometheus_fastapi_instrumentator import Instrumentator

def create_app() -> FastAPI:
    app = FastAPI(title="TraceLedger")
    Instrumentator().instrument(app).expose(app)
    app.include_router(api_router)
    return app

app = create_app()