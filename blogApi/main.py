from fastapi import FastAPI
from database import engine
import post
import user

app = FastAPI()

@app.get("/")
async def root():
    return "Welcome to My Api"