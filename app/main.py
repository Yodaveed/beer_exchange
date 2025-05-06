from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import drinks

app = FastAPI(title="The Beer Exchange")

app.include_router(drinks.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return {"message": "FastAPI is working!"}

@app.get("/dashboard")
def get_dashboard():
    return FileResponse("app/static/dashboard.html")
