from fastapi import APIRouter, Depends, HTTPException, Query
from .auth_dtos import LoginResponse, LoginRequest, SignupRequest, SignupResponse, UserResponse
from .user_service import UserService, get_user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=SignupResponse)
def signup(user_data: SignupRequest, service: UserService = Depends(get_user_service)):
    try:
        user = service.signup(user_data.username, user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return SignupResponse(id=str(user.id), username=user.username)


@router.post("/login", response_model=LoginResponse)
def login(user_data: LoginRequest, service: UserService = Depends(get_user_service)):
    try:
        user, token = service.login(user_data.username, user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return LoginResponse(id=str(user.id), username=user.username, token=token)

@router.get("/user/get/{username}", response_model=UserResponse)
def get_by_username(username: str, service: UserService = Depends(get_user_service)):
    user = service.search_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=str(user.id), username=user.username)

@router.get("/search", response_model=list[UserResponse])
def search_users(username: str = Query(...), service: UserService = Depends(get_user_service)):
    users = service.search_users(username)
    return [UserResponse(id=str(user.id), username=user.username) for user in users]