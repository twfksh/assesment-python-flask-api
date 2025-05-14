from datetime import timedelta
from sqlmodel import Session, select
import bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
)

from models import TokenBlocklist, User
from schemas import UserSchema


class AuthService:
    """
    Service class for authentication-related operations.
    """

    def __init__(self, engine):
        self.engine = engine

    def authenticate_user(self, username: str, password: str) -> User:
        """
        Authenticate a user by username and password.
        """
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).first()
            if not user:
                raise ValueError("[AuthError] - Username or password is incorrect")
            if not bcrypt.checkpw(
                password.encode("utf-8"), user.password.encode("utf-8")
            ):
                raise ValueError("[AuthError] - Username or password is incorrect")

            return user

    def login(self, username: str, password: str) -> dict:
        """
        Login a user by username and password.
        """
        user = self.authenticate_user(username, password)

        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "username": user.username,
                "created_at": user.created_at,
            },
        }

    def logout(self, jti: str) -> None:
        """
        Logout a user by invalidating their session.
        """
        with Session(self.engine) as session:
            blocked_toen = TokenBlocklist(jti=jti)
            session.add(blocked_toen)
            session.commit()

    def is_token_revoked(self, jti: str) -> bool:
        """
        Check if a token is revoked.
        """
        with Session(self.engine) as session:
            statement = select(TokenBlocklist).where(TokenBlocklist.jti == jti)
            token = session.exec(statement).first()
            return token is not None

    def refresh(self, jti: str) -> dict:
        """
        Refresh a user's access token.
        """
        with Session(self.engine) as session:
            token = decode_token(jti)
            user_id = token["sub"]
            statement = select(User).where(User.id == user_id)
            user = session.exec(statement).first()
            if not user:
                raise ValueError("[RefreshError] - User not found")

            access_token = create_access_token(
                identity=user.username,
                expires_delta=timedelta(minutes=15),
            )

            return {
                "access_token": access_token,
                "user": {
                    "username": user.username,
                    "created_at": user.created_at,
                },
            }


class UserService:
    """
    Service class for user-related operations.
    """

    def __init__(self, engine):
        self.engine = engine

    def create_user(self, username: str, password: str) -> User:
        """
        Create a new user in the database.
        """
        with Session(self.engine) as session:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            db_user = User(username=username, password=hashed_password.decode("utf-8"))
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    def get_user(self, username: str) -> User:
        """
        Retrieve a user by username from the database.
        """
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).first()
            if user:
                return user
            else:
                raise ValueError("[GetUserError] - User not found")

    def get_users(self) -> list[User]:
        """
        Retrieve all users from the database.
        """
        with Session(self.engine) as session:
            statement = select(User)
            users = session.exec(statement).all()
            return users

    def update_user(self, username: str, user: UserSchema) -> User:
        """
        Update an existing user in the database.
        """
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            db_user = session.exec(statement).first()
            if db_user:
                db_user.username = user.username
                db_user.password = bcrypt.hashpw(
                    user.password.encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")
                session.commit()
                session.refresh(db_user)
                return db_user
            else:
                raise ValueError("[UpdateError] - User not found")

    def delete_user(self, username: str) -> None:
        """
        Delete a user from the database.
        """
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).first()
            if user:
                session.delete(user)
                session.commit()
            else:
                raise ValueError("[DeleteError] - User not found")
