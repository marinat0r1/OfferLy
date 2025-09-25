from fastapi import FastAPI
from .api import router

app = FastAPI(title="Contractor GPT API")
app.include_router(router)
