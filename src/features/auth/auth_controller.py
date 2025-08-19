from fastapi import APIRouter, Depends, HTTPException
from .auth_dtos import LoginResponse, TokenData
from .user_service import UserService, get_user_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def google_login(token_data: TokenData, service: UserService = Depends(get_user_service)):
    try:
        user, token = service.google_auth(token_data.token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    return LoginResponse(email=user.email, token=token)