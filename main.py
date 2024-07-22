from fastapi import FastAPI
from routers import books, users
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(books.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to BookStore Using RestApi Updated"}
