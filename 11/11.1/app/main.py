from fastapi import FastAPI, HTTPException
from threading import Lock
from app.models import UserCreate, UserResponse

app = FastAPI(title="User Management API")

db: dict[int, dict] = {}
next_id = 1
_id_lock = Lock()

def get_next_id() -> int:
    global next_id
    with _id_lock:
        current = next_id
        next_id += 1
        return current

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    user_id = get_next_id()
    db[user_id] = user.model_dump()
    return {"id": user_id, **db[user_id]}

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db[user_id]}

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if db.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return None