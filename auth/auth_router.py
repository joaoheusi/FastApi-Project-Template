from fastapi import APIRouter, status, Body
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from auth.auth_models import AuthToken, AuthForm
from auth.auth_services import authenticate_user_service
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer

auth_scheme = JWTBearer(tokenUrl="auth")

router = APIRouter(
    prefix= "/auth",
    tags=["auth"]
)

@router.post("/",response_description="Returns the authentication Bearer token", response_model=AuthToken)
async def authenticate_user(form_data: AuthForm = Body(...)):
    token = await authenticate_user_service(form_data)
    return JSONResponse(status_code=status.HTTP_200_OK,content= token)
    
@router.post("/verify",response_description="Verify if access token is valid",response_model=AuthToken)
async def verify_token(auth:Depends = Depends(auth_scheme)):
    return JSONResponse(status_code=status.HTTP_200_OK,content={
        "Success": "Token validated!"
    })