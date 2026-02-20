from fastapi import FastAPI, HTTPException, status, Depends, APIRouter

from Service.Register import router as auth_router
from Service.user_profile_routers import router as user_profile_router
from Database.sql import Base, engine
from Utils.auth_bearer import JWTBearer
from Models.register import User
from sqlalchemy.orm import Session
from Database.sql import get_db


app = FastAPI(title="Calorie Tracking API", description="API for user registration and authentication")

app.include_router(auth_router)
app.include_router(user_profile_router)
Base.metadata.create_all(bind=engine)

@app.get('/getusers')
def getusers( dependencies=Depends(JWTBearer()),session: Session = Depends(get_db)):
    user = session.query(User).all()
    return user

@app.get("/")
def read_root():
    return {"message": "Welcome to the Calorie Tracking API!"}