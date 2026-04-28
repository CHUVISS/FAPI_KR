from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import CustomExceptionA, CustomExceptionB, ErrorResponse

app = FastAPI(title="Custom Error Handling Demo")

@app.exception_handler(CustomExceptionA)
async def handle_custom_a(request: Request, exc: CustomExceptionA):
    print(f"[LOG] CustomExceptionA: {exc.detail} | Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            message=exc.message,
            detail=exc.detail
        ).model_dump()
    )

@app.exception_handler(CustomExceptionB)
async def handle_custom_b(request: Request, exc: CustomExceptionB):
    print(f"[LOG] CustomExceptionB: {exc.detail} | Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            message=exc.message,
            detail=exc.detail
        ).model_dump()
    )

# Эндпоинты, вызывающие исключения
@app.get("/validate/{value}")
def validate_value(value: int):
    if value <= 0:
        raise CustomExceptionA()  # Вызывается при нарушении условия
    return {"status": "success", "data": f"Value {value} is valid"}

@app.get("/resource/{res_id}")
def get_resource(res_id: int):
    available_ids = [1, 42, 99]
    if res_id not in available_ids:
        raise CustomExceptionB()  # Вызывается, если ресурс не найден
    return {"status": "success", "data": {"id": res_id, "name": f"Resource #{res_id}"}}