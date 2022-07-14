from typing import Optional
from pydantic import BaseModel

from passlib.hash import bcrypt
from tortoise.models import Model
from tortoise import fields

listUser = {
    1:{
        "username":"Lyra",
        "password":"Best",
        "uniqueId":1
    },
    2:{
        "username":"BonBon",
        "password":"Bon",
        "uniqueId":2
    }
}


class User(BaseModel):
    username: str = "Lyra"
    password: str = "Hearthstrings121"
    uniqueId: int = 5

    # def __init__(self,username, password, uniqueId):
    #     this.username = username
    #     this.password = password
    #     this.uniqueId = uniqueId

class UserInput(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    uniqueId: Optional[int] = None


class UserModel(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    hash_password = fields.CharField(128)

    # @classmethod
    # async def  get_username(cls, username):
    #     return cls.get_username(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.hash_password)

class Token(BaseModel):
    token: str
    token_type: str