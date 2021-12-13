import os
from dotenv import load_dotenv
import motor.motor_asyncio
from passlib.context import CryptContext
from psycopg2 import connect

DEPLOYMENT = False

## MONGO DB CONNECTION CONFIGS
load_dotenv()
MONGODB_URL = os.getenv("MONGO_URL")
database_client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)["titania"]


# PASSWORD ENCRYPTION CONFIGS
encryption_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#JWT TOKENS CONFIGS
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

#FERNET CONFIGS
FERNET_SECRET_KEY = os.getenv("FERNET_SECRET_KEY")


