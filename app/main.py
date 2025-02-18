# app/main.py
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.auth import router as auth_router
from app.compress import encrpyt_router
import os
import shutil



app = FastAPI()

@app.on_event("startup")
def on_startup():
    
    if not os.path.exists("userspace"):
        os.mkdir("userspace")
    else:
        shutil.rmtree("userspace")
        os.mkdir("userspace")

        
       
    SQLModel.metadata.create_all(engine)

app.include_router(auth_router)
app.include_router(encrpyt_router)

