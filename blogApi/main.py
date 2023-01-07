from fastapi import FastAPI
from core.database import engine
from routes import user, post

app = FastAPI()

@app.get("/")
async def root():
    return "Welcome to My Api"