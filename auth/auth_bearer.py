from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Request, HTTPException
from typing import Optional
from auth.auth_handler import decodeJWT
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from modules.users.services.users import find_one_service
from modules.users.models.users import User

class JWTBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl:str, moduleName:Optional[str]= None, auto_error:bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error,tokenUrl=tokenUrl)
        self.moduleName = moduleName
    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if authorization:
            if not self.verify_jwt(param):
                raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Invalid token or expired token",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            if self.moduleName:
                if not await self.verify_module_token(param):
                    raise HTTPException(
                            status_code=HTTP_401_UNAUTHORIZED,
                            detail="This user does not have authorization to request this module",
                            headers={"WWW-Authenticate": "Bearer"},
                        )
            if scheme.lower() != "bearer":
                if self.auto_error:
                    raise HTTPException(
                        status_code=HTTP_403_FORBIDDEN,
                        detail="Invalid authentication method.",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            return param
        else:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN,
             detail="Invalid authorization code.",
             headers={"WWW-Authenticate": "Bearer"})

    def verify_jwt(self,jwtoken:str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid

    async def verify_module_token(self, jwtoken:str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decodeJWT(jwtoken)
            user_id: str = payload['_id']
            user : User = await find_one_service(user_id)
            user_disabled = user.disabled
            user_modules = user.allowedModules
        except:
            payload = None
            user_modules = []
            user_disabled = True
        if self.moduleName in user_modules and not user_disabled:
            is_token_valid = True
        return is_token_valid
