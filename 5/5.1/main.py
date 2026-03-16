from fastapi import FastAPI, HTTPException, Response, Cookie
from pydantic import BaseModel
import uuid
from typing import Optional

app = FastAPI(title="Cookie Authentication - Task 5.1")

class LoginData(BaseModel):
    username: str
    password: str

VALID_USERS = {
    "user123": "password123",
    "admin": "admin123"
}

sessions = {}

@app.post("/login")
async def login(login_data: LoginData, response: Response):
    if login_data.username in VALID_USERS and VALID_USERS[login_data.username] == login_data.password:
        session_token = str(uuid.uuid4())
        
        sessions[session_token] = login_data.username
        
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=3600,
            secure=False,
            samesite="lax"
        )
        
        return {"message": "Login successful", "username": login_data.username}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/user")
async def get_user(session_token: Optional[str] = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})
    
    if session_token in sessions:
        username = sessions[session_token]
        return {
            "message": "User profile",
            "username": username,
            "user_id": session_token
        }
    else:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})

@app.get("/logout")
async def logout(response: Response, session_token: Optional[str] = Cookie(None)):
    if session_token and session_token in sessions:
        del sessions[session_token]
    
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}

@app.get("/")
async def root():
    return {
        "message": "Cookie Authentication API - Task 5.1",
        "endpoints": {
            "POST /login": "Login with username/password",
            "GET /user": "Get user profile (protected)",
            "GET /logout": "Logout"
        }
    }