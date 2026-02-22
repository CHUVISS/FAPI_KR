from pydantic import BaseModel, Field, field_validator
import re

class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str):

        forbidden_words = ["кринж", "рофл", "вайб"]

        for word in forbidden_words:
            if re.search(rf"\b{word}\w*\b", value, re.IGNORECASE):
                raise ValueError("Использование недопустимых слов")

        return value