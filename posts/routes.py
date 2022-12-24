from fastapi import FastAPI
from . import database

app = FastAPI()



@app.route('/posts')
def get_post():
    return "All posts"