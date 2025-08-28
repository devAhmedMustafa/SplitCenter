from fastapi import Depends
from firebase_admin import auth as firebase_auth
from .user_repo import UserRepository, get_user_repository
from .jwt import create_jwt_token
from src.utils.hash import hash_password, verify_password
from .user import User

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def firebase_auth(self, firebase_token: str):
        try:
            # Verify the Firebase ID token
            decoded_token = firebase_auth.verify_id_token(firebase_token)
        except Exception:
            raise ValueError("Invalid Firebase token")

        email = decoded_token.get("email")
        if not email:
            raise ValueError("Email not found in Firebase token")

        # Ensure email is verified
        if not decoded_token.get("email_verified", False):
            raise ValueError("Email is not verified")

        # Get or create user in your database
        user = self.user_repo.get_by_username(email)
        if user is None:
            user = User(username=email)
            user = self.user_repo.create(user)

        # Generate your own JWT for your backend
        token = create_jwt_token({"email": user.username})
        return user, token

    def signup(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)
        if user:
            raise ValueError("User already exists")
        
        # Encrypt password
        hashed_password = hash_password(password)

        # Create new user
        user = User(username=username, password=hashed_password)

        user = self.user_repo.create(user)
        return user

    def login(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)
        if not user:
            raise ValueError("User not found")

        if not verify_password(password, user.password):
            raise ValueError("Invalid password")

        token = create_jwt_token({"email": user.username, "id": str(user.id)})
        return user, token

def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)
