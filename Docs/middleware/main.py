import time
from fastapi import FastAPI, Request

app = FastAPI()

"""
    To use a middleware, you need to add @app.middleware() on top of the function
"""

@app.middleware("http")
async def add_process_time_loader(request:Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return