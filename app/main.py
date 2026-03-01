# App entry point
from fastapi import FastAPI
from api.routes import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(title="TraceLedger")
    app.include_router(api_router)
    return app

app = create_app()