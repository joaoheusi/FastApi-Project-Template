from typing import Optional
from fastapi.exceptions import HTTPException
from auth.auth_handler import create_access_token
from datetime import datetime,timedelta
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordRequestForm
from modules.users.models.user import CreateUser, User, UpdateUser
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, database_client, encryption_context
from fastapi.encoders import jsonable_encoder


from test import update_student

users_repository = database_client.users


async def create_user_service(requestBody: CreateUser):
    try:
        new_user: User = User(
            username=requestBody.username,
            email=requestBody.email,
            password=encryption_context.hash(requestBody.password),
            fullName=requestBody.fullName,
            disabled=False,
        )
        # print(new_user)
        new_user = await users_repository.insert_one(jsonable_encoder(new_user))
        response = await users_repository.find_one({"_id": new_user.inserted_id})

        return response
    except:
        return False


async def find_all_service():
    try:
        users = await users_repository.find().to_list(100)
        return users
    except:
        return False


async def find_one_service(user_id: str):
    try:
        user = await users_repository.find_one({"_id": user_id})
        return user
    except:
        return False



async def update_user_service(user_id: str, new_user_info: UpdateUser):
    try:
        new_user_info = {k: v for k, v in new_user_info.dict().items() if v is not None}
        if len(new_user_info) >= 1:
            update_result = await users_repository.update_one(
                {"_id": user_id}, {"$set": new_user_info}
            )

            if update_result.modified_count == 1:
                if (
                    updated_user := await users_repository.find_one({"_id": user_id})
                ) is not None:
                    return updated_user
        if (
            existing_user := await users_repository.find_one({"_id": user_id})
        ) is not None:
            return existing_user
    except:
        return False


async def delete_user_service(user_id: str):
    delete_result = await users_repository.delete_one({"_id": user_id})
    if delete_result.deleted_count == 1:
        return True
    return False



#TODO ADD TOKEN VALIDATION FUNCTION
#EXPIRATION TIME SHOULD BE VALIDATED
#ANOTHER STUFF SHOULD BE VALIDATED

async def validate_token():
    pass

async def authenticate_service(form_data: OAuth2PasswordRequestForm):
    user = await users_repository.find_one({"username":form_data.username})
    user = User(**user)
    if not user:
        return False
    if not encryption_context.verify(form_data.password, user.password):
        return False
    access_token = create_access_token(
        data={"sub": user.username}
        )
    return {"acessToken": access_token, "tokenType": "Bearer"}