from fastapi import FastAPI
from app.routers import drinks

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI is alive"}

app.include_router(drinks.router)

