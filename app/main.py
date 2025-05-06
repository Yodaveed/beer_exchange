from fastapi import FastAPI
from app.routers import drinks

app = FastAPI()
app.include_router(drinks.router)
