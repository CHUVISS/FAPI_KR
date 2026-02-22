from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r", encoding="utf-8") as file:
        content = file.read()
    return content


# Другая версия

# from fastapi import FastAPI
# from fastapi.responses import FileResponse

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return FileResponse("index.html")