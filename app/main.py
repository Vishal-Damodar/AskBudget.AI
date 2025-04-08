from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Budget Buddy")

app.include_router(router)