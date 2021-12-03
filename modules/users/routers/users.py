from fastapi import APIRouter, Body, status, Depends
from typing import List


from fastapi.responses import JSONResponse
from modules.users.models.user import UpdateUser, User, CreateUser
from modules.users.services.users import (
    authenticate_service,
    create_user_service,
    delete_user_service,
    find_all_service,
    find_one_service,
    update_user_service,
)
from auth.auth_bearer import JWTBearer
from fastapi.security import OAuth2PasswordRequestForm

oauth2_scheme = JWTBearer(tokenUrl="users/authenticate")

from uuid import uuid4


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_description="List all users", response_model=List[User])
async def get_users():
    users = await find_all_service()
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)


@router.get(
    "/{id}",
    response_description="Return specified user",
    response_model=User,
)
async def get_user(id: str):
    user = await find_one_service(id)
    if user:
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"Error": "User not found!"}
    )


@router.post("/", response_description="Create a new user", response_model=User)
async def create_user(requestBody: CreateUser = Body(...)):
    created_user = await create_user_service(requestBody)
    if created_user:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"Error": "User could not be created"},
    )


@router.patch("/{id}", response_description="Updates a user info", response_model=User)
async def update_user(id: str, requestBody: UpdateUser = Body(...)):
    updated_user = await update_user_service(id, requestBody)
    if updated_user:
        return JSONResponse(status_code=status.HTTP_200_OK, content=updated_user)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"Error": "User not found"}
    )


@router.delete("/{id}", response_description="Deletes specified user")
async def delete_user(id: str, acess_token : str = Depends(oauth2_scheme)):
    deleted = await delete_user_service(id)
    if deleted:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"Success": "User deleted!"}
        )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"Error": "User not found!"}
    )

@router.post("/authenticate")
async def authenticate(form_data: OAuth2PasswordRequestForm = Depends()):
    token = await authenticate_service(form_data)
    return JSONResponse(status_code=status.HTTP_200_OK, content=token)
