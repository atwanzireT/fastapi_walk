# fastapi_walk

### Hello World
 
#### This is a simple example of a FastAPI application that returns a "Hello, World!" message when you make a GET request to the / endpoint:

- from fastapi import FastAPI
- app = FastAPI()
- @app.get("/")
- def read_root():
-    return {"Hello": "World"}

#### To run the application, you can use the uvicorn ASGI server:
- uvicorn main:app --reload

### Query Parameters
#### This example shows how to use query parameters in a FastAPI endpoint to filter a list of items:

- from fastapi import FastAPI
- from pydantic import BaseModel

- app = FastAPI()

- class Item(BaseModel):
-    name: str
-    price: float

- @app.get("/items/")
- def read_items(skip: int = 0, limit: int = 10):
-   return {"skip": skip, "limit": limit}

#### In this example, the read_items endpoint accepts two query parameters, skip and limit, which are used to paginate the list of items. The default values for skip and limit are 0 and 10,
