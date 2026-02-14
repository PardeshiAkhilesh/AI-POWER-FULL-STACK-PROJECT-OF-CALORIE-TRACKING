from fastapi import FastAPI, HTTPException, status, Depends, APIRouter

from Service.Register import router as auth_router
from Database.sql import Base, engine

app = FastAPI(title="Calorie Tracking API", description="API for user registration and authentication")

app.include_router(auth_router)
Base.metadata.create_all(bind=engine)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Calorie Tracking API!"}