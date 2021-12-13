from fastapi.security import OAuth2PasswordRequestForm
from auth.auth_handler import create_access_token
from modules.users.models.users import User
from modules.users.services.users import find_one_by_name
from config import encryption_context
from typing import Dict
from fastapi import HTTPException, status

async def authenticate_user_service(form_data: OAuth2PasswordRequestForm) -> Dict[str,str]:
    user: User = await find_one_by_name(form_data.username)
    if not user:
        raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Username/Password combination invalid.",
                        headers={"WWW-Authenticate": "Bearer"}, 
                    )
    if not encryption_context.verify(form_data.password, user.password):
        raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Username/Password combination invalid.",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
    if user.disabled:
        raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User is disabled.",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
    access_token = await create_access_token(
        data={"_id":user.id,
        "allowedModules": user.allowedModules}
    )
    return {"accessToken": access_token, "tokenType": "bearer"}