from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
Oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')

@app.get('/items')
async def read_items(token : str = Depends(Oauth2_scheme)):
    return {'token': token}