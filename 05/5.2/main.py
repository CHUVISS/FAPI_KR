from fastapi import FastAPI, HTTPException, Response, Cookie
from pydantic import BaseModel
from itsdangerous import URLSafeTimedSerializer
import uuid
from typing import Optional
import os

app = FastAPI(title="Cookie Authentication with Signature - Task 5.2")

SECRET_KEY = "my-super-secret-key-12345"
serializer = URLSafeTimedSerializer(SECRET_KEY)

class LoginData(BaseModel):
    username: str
    password: str

VALID_USERS = {
    "user123": "password123",
    "admin": "admin123"
}

@app.post("/login")
async def login(login_data: LoginData, response: Response):
    if login_data.username in VALID_USERS and VALID_USERS[login_data.username] == login_data.password:
        user_id = str(uuid.uuid4())
        
        session_token = serializer.dumps(user_id)
        
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=3600,
            secure=False,
            samesite="lax"
        )
        
        return {
            "message": "Login successful",
            "username": login_data.username,
            "user_id": user_id
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/profile")
async def get_profile(session_token: Optional[str] = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})
    
    try:
        user_id = serializer.loads(session_token, max_age=3600)
        
        return {
            "message": "Profile information",
            "user_id": user_id,
            "username": "User from session",
            "email": "user@example.com"
        }
    except:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})

@app.get("/logout")
async def logout(response: Response, session_token: Optional[str] = Cookie(None)):
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}

@app.get("/")
async def root():
    return {
        "message": "Cookie Authentication with Signature - Task 5.2",
        "endpoints": {
            "POST /login": "Login with username/password",
            "GET /profile": "Get user profile (protected with signed cookie)",
            "GET /logout": "Logout"
        }
    }