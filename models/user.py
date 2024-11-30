from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(..., unique=True)
    email: EmailStr = Field(..., unique=True)
    create_at: Optional[datetime] = Field(default_factory=datetime.now)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "Ivan",
                "email": "ivan2012@mail.ru",
            }
        }
    }


class UserEmailUpdate(SQLModel):
    email: EmailStr = Field(..., unique=True)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "ivan2012@mail.ru",
            }
        }
    }
