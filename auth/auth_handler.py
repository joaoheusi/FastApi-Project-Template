from datetime import datetime, timedelta
from bson import json_util
from cryptography.fernet import Fernet
from typing import Dict
from config import ACCESS_TOKEN_EXPIRE_MINUTES,JWT_SECRET_KEY,ALGORITHM, FERNET_SECRET_KEY
from jose import jwt
import json

fernet = Fernet(FERNET_SECRET_KEY)

def fernet_encrypt(data:dict) -> Dict[str,str]:
    string_data = json.dumps(data)
    encrypted_data = fernet.encrypt(string_data.encode())
    encrypted_dict = {"data": encrypted_data.decode('utf-8')}
    return encrypted_dict

def fernet_decrypt(encrypted_dict:dict) -> Dict:
    encrypted_data = encrypted_dict["data"]
    string_data = fernet.decrypt(encrypted_data.encode()).decode('utf-8')
    data = json.loads(string_data)
    return data

def decodeJWT(token: str) -> dict:
    try:
        decode = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        data = fernet_decrypt(decode)
        return data
    except jwt.ExpiredSignatureError:
        return {}


async def create_access_token(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    expire = int(expire.timestamp())
    user_data = fernet_encrypt(data)
    to_encode = {**user_data,"exp":expire}
    encoded_jwt = jwt.encode(to_encode,JWT_SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt