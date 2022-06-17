from datetime import timedelta
from fastapi import Depends, FastAPI, Request, Body, status,HTTPException
import uvicorn
from sqlalchemy.orm import Session
from database import DBContext, SessionLocal, engine
import crud, schemas, models
import password as pwd
import jwt
from fastapi_login import LoginManager
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv
load_dotenv()

def get_database():
	with DBContext() as db:
		yield db

SECRET_KEY = os.getenv('SECRET_KEY_64')
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*365

manager = LoginManager(SECRET_KEY, token_url="/login", use_cookie=True)
manager.cookie_name="auth"
app = FastAPI()

@manager.user_loader()
def get_user(username: str, db: Session = None):
    if db is None:
        with DBContext() as db:
            return crud.get_user_by_username(db=db,username=username)
    return crud.get_user_by_username(db=db,username=username)

def authenticate_user(username: str, password: str, db: Session = Depends(get_database)):
    user:schemas.User = crud.get_user_by_username(db=db,username=username)
    if not user:
        return None
    if not pwd.verify_password(plain_password=password,hashed_password=user.hashed_password):
        return None
    return user

class NotAuthenticatedException(Exception):
    pass

def not_authenticated_exception_handler(request, exception):
    return RedirectResponse("/login")

manager.not_authenticated_exception = NotAuthenticatedException
app.add_exception_handler(NotAuthenticatedException, not_authenticated_exception_handler)

@app.get("/")
async def root():
    return {"root":"tecacom"}

@app.get("/login", tags=["user"])
async def login():
    return {"login":"tecacom-admin"}

@app.post('/login', 
	tags = ['user'],
	response_class=RedirectResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
                    db: Session = Depends(get_database)):
    user:schemas.User = authenticate_user(
        username=form_data.username,
        password = form_data.password, db = db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = manager.create_access_token(
        data={"sub": user.username},
        expires=access_token_expires)
    
    resp = JSONResponse(access_token, status_code=status.HTTP_200_OK)
    manager.set_cookie(resp,access_token)
    return resp

@app.get("/home", response_model=schemas.UserPublic)
async def home(user: schemas.User = Depends(manager)):
	public_user = schemas.UserPublic(username=user.username)
	return public_user

@app.get('/logout', tags=["user"])
async def protected_route(user:schemas.User=Depends(manager)):
    resp = JSONResponse({"status": "logout","user":user.username}, status_code=status.HTTP_200_OK)
    # manager.delete_cookie(resp)
    resp.delete_cookie(key=manager.cookie_name)
    return resp

if __name__=="__main__":
	uvicorn.run(app)
    # hellosss
	