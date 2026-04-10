# main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
import secrets
from pydantic import BaseModel
from typing import Optional

MODE = os.getenv("MODE", "DEV")
DOCS_USER = os.getenv("DOCS_USER")
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD")

if MODE not in ("DEV", "PROD"):
    raise ValueError(f"Invalid MODE value: {MODE}. Expected DEV or PROD")

if MODE == "PROD":
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI(docs_url="/docs", redoc_url=None, openapi_url="/openapi.json")

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

fake_users_db = {}

class UserBase(BaseModel):
    username: str

class User(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password[:72])

def check_docs_auth(credentials: HTTPBasicCredentials = Depends(security)) -> bool:
    if DOCS_USER is None or DOCS_PASSWORD is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Documentation credentials not configured"
        )
    username_correct = secrets.compare_digest(credentials.username, DOCS_USER)
    password_correct = secrets.compare_digest(credentials.password, DOCS_PASSWORD)
    if not (username_correct and password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials for documentation",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

def auth_user(credentials: HTTPBasicCredentials = Depends(security)) -> UserInDB:
    for db_username, user_in_db in fake_users_db.items():
        if secrets.compare_digest(credentials.username, db_username):
            if verify_password(credentials.password, user_in_db.hashed_password):
                return user_in_db
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


if MODE == "DEV":
    @app.get("/docs", include_in_schema=False)
    async def protected_docs(auth: bool = Depends(check_docs_auth)):
        from fastapi.openapi.docs import get_swagger_ui_html
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        )

    @app.get("/openapi.json", include_in_schema=False)
    async def protected_openapi(auth: bool = Depends(check_docs_auth)):
        return app.openapi()


if MODE == "PROD":
    @app.get("/docs", include_in_schema=False)
    @app.get("/openapi.json", include_in_schema=False)
    @app.get("/redoc", include_in_schema=False)
    async def docs_not_found():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


@app.post("/register", include_in_schema=MODE == "DEV")
def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(username=user.username, hashed_password=hashed_password)
    fake_users_db[user.username] = user_in_db
    return {"message": "User added successfully"}

@app.get("/login", include_in_schema=MODE == "DEV")
def login(user: UserInDB = Depends(auth_user)):
    return {"message": f"Welcome, {user.username}!"}