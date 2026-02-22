from fastapi import FastAPI
from models import Feedback

app = FastAPI()

feedback_storage = []

@app.post("/feedback")
def create_feedback(feedback: Feedback):
    feedback_storage.append(feedback.model_dump())

    return {
        "message": f"Feedback received. Thank you, {feedback.name}."
    }

@app.get("/feedback")
def dd():
    return feedback_storage