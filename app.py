from fastapi import FastAPI
from modules.users.routers import users
from auth import auth_router
import logging

log = logging.getLogger('__name__')

app = FastAPI()

app.include_router(users.router)
app.include_router(auth_router.router)

@app.get("/")
async def root():
    return {"message": "Root"}
