from fastapi import FastAPI
from app.api import users
from app.api import auth

app = FastAPI(
    title="Mini ERP - Backend",
    version="0.1.0"
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Mini ERP API is running 🚀"}
