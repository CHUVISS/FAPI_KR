from fastapi import FastAPI, HTTPException, Header, Response
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
import re

app = FastAPI(title="Headers Processing - Task 5.4")

class CommonHeaders(BaseModel):
    user_agent: str = Header(..., alias="User-Agent")
    accept_language: str = Header(..., alias="Accept-Language")
    
    @validator('accept_language')
    def validate_accept_language(cls, v):
        pattern = r'^([a-z]{2}(-[A-Z]{2})?(;q=[0-9]\.[0-9])?)(,\s*[a-z]{2}(-[A-Z]{2})?(;q=[0-9]\.[0-9])?)*$'
        if not re.match(pattern, v) and v != "":
            raise ValueError('Invalid Accept-Language format')
        return v

@app.get("/headers")
async def get_headers(headers: CommonHeaders = None):
    if not headers:
        raise HTTPException(status_code=400, detail="Headers are required")
    
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }

@app.get("/info")
async def get_info(response: Response, headers: CommonHeaders = None):
    if not headers:
        raise HTTPException(status_code=400, detail="Headers are required")
    
    current_time = datetime.now().isoformat()
    
    response.headers["X-Server-Time"] = current_time
    
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }

@app.get("/")
async def root():
    return {
        "message": "Headers Processing API - Task 5.4",
        "endpoints": {
            "GET /headers": "Return User-Agent and Accept-Language headers",
            "GET /info": "Return headers with welcome message and X-Server-Time header"
        }
    }