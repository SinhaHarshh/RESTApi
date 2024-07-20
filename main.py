import json
import os
from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

# Secret key to encode the JWT tokens
SECRET_KEY = "snfdsfndushfasndksaefj"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Book(BaseModel):                                  #BOOK DATA STRUCTURE.......
    id: Optional[str] = uuid4().hex
    title: str
    author: str
    published_date: str
    isbn: str

class User(BaseModel):                                  #USER DATA STRUCTURE ....
    username: str
    email: EmailStr
    password: str

class UserInDB(User):
    id: str
    hashed_password: str

BOOKS_FILE = "books.json"                               #STORING DATA IN A FILE BOOKS.JSON
BOOKS = []
USERS_FILE = "users.json"                               #STORING DATA IN A FILE USERS.JSON
USERS = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOKS = json.load(f)

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        USERS = json.load(f)
        

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my bookstore app Using Restapi! "}          #API ENDPOINTS

@app.get("/books")                                                 #ALL BOOKS
async def list_books():
    return {"books": BOOKS}

@app.get("/books/{id}")                                             #BOOKS BY INDEX
async def book_by_index(id: int):
    if id < len(BOOKS):
        return BOOKS[id]
    else:
        raise HTTPException(404, f"Book index {id} out of range ({len(BOOKS)}).")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = None
    for u in USERS:
        if u["username"] == username:
            user = u
            break
    if user is None:
        raise credentials_exception
    return user

@app.post("/books", dependencies=[Depends(get_current_user)])
async def add_book(book: Book):
    book.id = uuid4().hex
    json_book = jsonable_encoder(book)                                          #ADD BOOKS
    BOOKS.append(json_book)
    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOKS, f)
    return {"book_id": book.id}

@app.put("/books/{id}", dependencies=[Depends(get_current_user)])
async def update_book(id: int, updated_book: Book):
    if id < len(BOOKS):                                                         #UPDATE BOOK
        BOOKS[id] = jsonable_encoder(updated_book)
        with open(BOOKS_FILE, "w") as f:
            json.dump(BOOKS, f)
        return BOOKS[id]
    else:
        raise HTTPException(404, f"Book index {id} out of range ({len(BOOKS)}).")

@app.delete("/books/{id}", dependencies=[Depends(get_current_user)])
async def delete_book(id: int):                                                             #DELETE BOOOKS
    if id < len(BOOKS):
        removed_book = BOOKS.pop(id)
        with open(BOOKS_FILE, "w") as f:
            json.dump(BOOKS, f)
        return removed_book
    else:
        raise HTTPException(404, f"Book index {id} out of range ({len(BOOKS)}).")

@app.post("/register")
async def register_user(user: User):
    if any(u["username"] == user.username for u in USERS):                                          #USER REGISTERATION
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(
        id=str(ObjectId()), 
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    USERS.append(user_in_db.dict())
    with open(USERS_FILE, "w") as f:
        json.dump(USERS, f)
    return {"message": "User registered successfully"}

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    for user in USERS:
        if user["username"] == username and verify_password(password, user["hashed_password"]):
            return user
    return None

