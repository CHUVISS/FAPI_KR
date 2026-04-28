from pydantic import BaseModel

class ErrorResponse(BaseModel):
    status_code: int
    message: str
    detail: str

class CustomExceptionA(Exception):
    status_code = 400
    message = "Ошибка проверки условия"
    detail = "Переданное значение не удовлетворяет бизнес-правилу A"

class CustomExceptionB(Exception):
    status_code = 404
    message = "Ресурс не найден"
    detail = "Запрошенный идентификатор отсутствует в системе"