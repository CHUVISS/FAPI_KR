from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

VALID_USERNAME = "champion"
VALID_PASSWORD = "secret"

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> str:

    is_correct_username = credentials.username == VALID_USERNAME
    is_correct_password = credentials.password == VALID_PASSWORD

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": 'Basic realm = "Secure Area"'},
        )
    
    return credentials.username


@app.get("/login")
def login_endpoint(username: str = Depends(verify_credentials)):
    return "You got my secret, welcome"
