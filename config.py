import os
from dotenv import load_dotenv
import motor.motor_asyncio
from passlib.context import CryptContext

## MONGO DB CONNECTION CONFIGS
load_dotenv()
MONGODB_URL = os.getenv("MONGO_URL")
database_client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)["titania"]

# PASSWORD ENCRYPTION CONFIGS
encryption_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#JWT TOKENS CONFIGS
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2