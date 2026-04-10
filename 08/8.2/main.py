from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection

app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

@app.post("/todos", status_code=201, response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO todos (title, description, completed) VALUES (?, ?, 0)",
        (todo.title, todo.description)
    )
    conn.commit()
    conn.close()
    return {"id": cursor.lastrowid, "title": todo.title, "description": todo.description, "completed": False}

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"id": row["id"], "title": row["title"], "description": row["description"], "completed": bool(row["completed"])}

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    title = todo.title if todo.title is not None else row["title"]
    description = todo.description if todo.description is not None else row["description"]
    completed = int(todo.completed) if todo.completed is not None else row["completed"]

    conn.execute(
        "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
        (title, description, completed, todo_id)
    )
    conn.commit()
    conn.close()
    return {"id": todo_id, "title": title, "description": description, "completed": bool(completed)}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}