from fastapi import FastAPI
from modules.users.routers import users

app = FastAPI()

app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Root"}
