from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.database import SessionLocal, engine
from db import models   
from setting.config import settings
from router import userRouter, product_router, category_router
from fastapi.middleware.cors import CORSMiddleware
from crud.userCRUD import create_default_admin

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    create_default_admin(db)
finally:
    db.close()

app = FastAPI(title=settings.APP_NAME, debug=settings.APP_DEBUG)

app.include_router(userRouter.router)

app.include_router(category_router.router)

app.include_router(product_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running!"}

