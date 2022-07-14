from typing import Optional
from pydantic import BaseModel


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