from fastapi import FastAPI, HTTPException, Response, Cookie
from pydantic import BaseModel
from itsdangerous import URLSafeTimedSerializer
import uuid
import time
from typing import Optional
import os

app = FastAPI(title="Dynamic Session Lifetime - Task 5.3")

SECRET_KEY = "my-super-secret-key-12345"
serializer = URLSafeTimedSerializer(SECRET_KEY)

class LoginData(BaseModel):
    username: str
    password: str

VALID_USERS = {
    "user123": "password123",
    "admin": "admin123"
}

SESSION_DURATION = 300
RENEWAL_THRESHOLD = 180

def create_session_token(user_id: str) -> str:
    current_time = int(time.time())
    data = f"{user_id}.{current_time}"
    return serializer.dumps(data)

def verify_and_extract_session_token(token: str):
    try:
        data = serializer.loads(token, max_age=SESSION_DURATION)
        user_id, timestamp_str = data.rsplit('.', 1)
        timestamp = int(timestamp_str)
        
        return user_id, timestamp
    except:
        return None, None

@app.post("/login")
async def login(login_data: LoginData, response: Response):
    if login_data.username in VALID_USERS and VALID_USERS[login_data.username] == login_data.password:
        user_id = str(uuid.uuid4())
        
        session_token = create_session_token(user_id)
        
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=SESSION_DURATION,
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
async def get_profile(response: Response, session_token: Optional[str] = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=401, detail={"message": "Session expired"})
    
    user_id, last_activity = verify_and_extract_session_token(session_token)
    
    if not user_id or not last_activity:
        raise HTTPException(status_code=401, detail={"message": "Invalid session"})
    
    current_time = int(time.time())
    time_since_last_activity = current_time - last_activity
    
    if time_since_last_activity >= SESSION_DURATION:
        raise HTTPException(status_code=401, detail={"message": "Session expired"})
    
    if time_since_last_activity >= RENEWAL_THRESHOLD:
        new_session_token = create_session_token(user_id)
        
        remaining_time = SESSION_DURATION - time_since_last_activity
        max_age = remaining_time if remaining_time > 0 else SESSION_DURATION
        
        response.set_cookie(
            key="session_token",
            value=new_session_token,
            httponly=True,
            max_age=max_age,
            secure=False,
            samesite="lax"
        )
        
        return {
            "message": "Session renewed",
            "user_id": user_id,
            "username": "User from session",
            "time_since_activity": time_since_last_activity
        }
    
    return {
        "message": "Profile information",
        "user_id": user_id,
        "username": "User from session",
        "time_since_activity": time_since_last_activity
    }

@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}

@app.get("/")
async def root():
    return {
        "message": "Dynamic Session Lifetime - Task 5.3",
        "endpoints": {
            "POST /login": "Login with username/password",
            "GET /profile": "Get user profile with dynamic session renewal",
            "GET /logout": "Logout"
        },
        "session_settings": {
            "duration_seconds": SESSION_DURATION,
            "renewal_threshold_seconds": RENEWAL_THRESHOLD
        }
    }