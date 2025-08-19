from fastapi import Depends
import requests 
from .user_repo import UserRepository, get_user_repository
from config.serttings import settings
from .jwt import create_jwt_token

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def google_auth(self, google_token: str):
        google_res = requests.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={google_token}"
        )

        if not google_res.ok:
            raise ValueError("Invalid Google token")
        
        res = google_res.json()

        if res.get("aud") != settings.GOOGLE_CLIENT_ID:
            raise ValueError("Invalid Google token")

        email = res.get("email")
        if email is None:
            raise ValueError("Invalid Google token")

        user = self.user_repo.get_by_email(email)
        if user is None:
            user = self.user_repo.create(email=email)

        token = create_jwt_token({"email": user.email})
        return user, token


def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)