from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="RAG Platform")
app.include_router(router)