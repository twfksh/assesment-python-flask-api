from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    """
    User model for the Auth API database.
    """

    __tablename__ = "users"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    username: str = Field(index=True, unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<User {self.username}>"


class TokenBlocklist(SQLModel, table=True):
    """
    Token blocklist model for the Auth API database.
    """

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    jti: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
