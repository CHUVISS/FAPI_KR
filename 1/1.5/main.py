from fastapi import FastAPI
from models import User

app = FastAPI()

@app.post("/user")
def create_user(user: User):
    
    is_adult = user.age >= 18

    response = user.model_dump()
    response["is_adult"] = is_adult

    return response