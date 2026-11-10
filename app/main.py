
from fastapi import FastAPI

app = FastAPI(title="My Docker API")

@app.get("/")
def home():
    return {
        "message": "FastAPI works in Docker!"
    }

@app.get("/users")
def users():
    return [
        {"id": 1, "name": "Ivan"},
        {"id": 2, "name": "Petro"}
    ]
