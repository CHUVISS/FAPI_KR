from fastapi import FastAPI, HTTPException, Response, Header
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
import re

app = FastAPI(title="Headers Processing with Model - Task 5.5")

class CommonHeaders(BaseModel):
    user_agent: str = Header(..., alias="user-agent")
    accept_language: str = Header(..., alias="accept-language")
    
    @validator('accept_language')
    def validate_accept_language(cls, v):
        pattern = r'^([a-z]{2}(-[A-Z]{2})?(;q=[0-9]\.[0-9])?)(,\s*[a-z]{2}(-[A-Z]{2})?(;q=[0-9]\.[0-9])?)*$'
        if not re.match(pattern, v) and v != "":
            raise ValueError('Invalid Accept-Language format. Expected format: "en-US,en;q=0.9,es;q=0.8"')
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
    
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    response.headers["X-Server-Time"] = current_time
    
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 400 and "Accept-Language" in str(exc.detail):
        return Response(
            content='{"detail": "Invalid Accept-Language format. Expected format: \\"en-US,en;q=0.9,es;q=0.8\\""}',
            status_code=400,
            media_type="application/json"
        )
    return Response(
        content=f'{{"detail": "{exc.detail}"}}',
        status_code=exc.status_code,
        media_type="application/json"
    )

@app.get("/")
async def root():
    return {
        "message": "Headers Processing API with Model - Task 5.5",
        "endpoints": {
            "GET /headers": "Return User-Agent and Accept-Language headers",
            "GET /info": "Return headers with welcome message and X-Server-Time header"
        },
        "example_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
        }
    }