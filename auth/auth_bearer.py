from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Request, HTTPException
from typing import Optional
from auth.auth_handler import decodeJWT
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED

class JWTBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl:str, auto_error:bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error,tokenUrl=tokenUrl)
    
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
            if scheme.lower() != "bearer":
                if self.auto_error:
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Not authenticated",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            return param
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self,jwtoken:str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid