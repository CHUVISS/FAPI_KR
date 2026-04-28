from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.models import User
from app.exceptions import ValidationErrorResponse

app = FastAPI(title="Validation & Custom Error Handling")

# Кастомный обработчик ошибок валидации
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for err in exc.errors():
        formatted_errors.append({
            "field": ".".join(str(loc) for loc in err["loc"]),
            "message": err["msg"]
        })
    
    response_data = ValidationErrorResponse(details=formatted_errors)
    print(f"[LOG] ⚠️ Validation error on {request.url.path}: {formatted_errors}")
    
    return JSONResponse(
        status_code=422,
        content=response_data.model_dump()
    )

# Эндпоинт регистрации пользователя
@app.post("/register", status_code=201)
async def register_user(user: User):
    return {
        "status": "success",
        "data": user.model_dump(),
        "message": "User registered successfully"
    }