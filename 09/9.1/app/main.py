from fastapi import FastAPI
from app.database import engine
from app.models import Base

app = FastAPI(title="Alembic Demo App")

# Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "FastAPI + Alembic ready"}