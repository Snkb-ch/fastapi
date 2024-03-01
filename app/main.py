from fastapi import FastAPI
import  models
from database import engine
from  routers import book, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(book.router)
app.include_router(user.router)