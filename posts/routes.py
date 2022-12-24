from fastapi import FastAPI

app = FastAPI()



@app.route('/posts')
def get_post():
    return "All posts"