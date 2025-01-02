from pydantic import BaseModel, validator
import re


class User(BaseModel):
    username: str
    password: str
    permissions: str

    @validator("username")
    def validate_username(cls, value):
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not bool(re.match(padrao, value)):
            raise ValueError("Invalid user email")
        
        return value
