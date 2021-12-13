from modules.users.models.users import CreateUser, User, UpdateUser
from config import database_client, encryption_context
from fastapi.encoders import jsonable_encoder
from typing import List


users_repository = database_client.users


async def create_user_service(requestBody: CreateUser) -> User|None:
    new_user: User = User(
        username=requestBody.username,
        email=requestBody.email,
        password=encryption_context.hash(requestBody.password),
        fullName=requestBody.fullName,
        disabled=False,
    )
    new_user = await users_repository.insert_one(jsonable_encoder(new_user))
    new_user: User|None = await find_one_service(new_user.inserted_id)
    if new_user:
        return new_user
    return None 


async def find_all_service() -> List[User]| List:
    try:
        users = await users_repository.find().to_list(100)
        return users
    except:
        return False


async def find_one_service(user_id: str) -> User|None:
    try:
        user : User| None = await users_repository.find_one({"_id": user_id})
        user = User(**user)
        return user
    except:
        return None
    
async def find_one_by_name(username: str) -> User|None:
    try:
        user = await users_repository.find_one({"username": username})
        user : User= User(**user)
        return user
    except:
        return None

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

