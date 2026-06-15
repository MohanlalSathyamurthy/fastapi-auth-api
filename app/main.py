from fastapi import FastAPI, Depends

from app.database.db import engine, get_db
from app.database.base import Base
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.routers.auth import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)

@app.get("/")
def health_check():
    return {"message": "API is healthy!"}