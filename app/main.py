
from fastapi import FastAPI
from app.routers import drinks

app = FastAPI(title="The Beer Exchange")

app.include_router(drinks.router)

@app.get("/")
def root():
    return {"message": "FastAPI is working!"}
