from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

app = FastAPI()


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Имя пользователя")
    email: str = Field(..., description="Email")
    age: Optional[int] = Field(None, description="Возраст")
    is_subscribed: bool = Field(False, description="Подписка на рассылку")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise ValueError("Некорректный формат email")
        return v

    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        if v is not None and v < 0:
            raise ValueError("Возраст не может быть отрицательным")
        return v


@app.post("/create_user")
async def create_user(user: UserCreate):
    return {
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "is_subscribed": user.is_subscribed
    }