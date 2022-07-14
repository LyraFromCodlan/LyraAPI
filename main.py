import jwt

from fastapi import FastAPI, Path, Query, Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from models_file import*
from typing import List

from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator





testApp = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='acc_token')

User_Pydantic = pydantic_model_creator(UserModel, name="Lyra")
User_InPydantic = pydantic_model_creator(UserModel, name="InLyra", exclude_readonly=True)

JWT_SECRET="LyraAPI"

async def authenticate_user(username:str, password:str):
    user = await UserModel.get(username=username)
    if not (user and user.verify_password(password)):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await UserModel.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    return await User_Pydantic.from_tortoise_orm(user)


@testApp.post("/user_post", response_model=User_Pydantic)
async def create_user(user: User_InPydantic):
    user_obj=UserModel(username=user.username, hash_password=bcrypt.hash(user.hash_password))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@testApp.post("/acc_token")
async def gen_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username,form_data.password)
    if not user:
        return {"Error":"Incorrect username or password"}
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {"access_token": token, "token_type":"Bearer"}





@testApp.get('/see_token')
async def index(token: str = Depends(oauth2_scheme)):
    return {'the_token' : token}

@testApp.get("/home")
async def home(token: str = Depends(oauth2_scheme)):
    print(token)
    return {"Homepage":"here", "Token_data":token}
    


@testApp.get("/users", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(UserModel.all())


@testApp.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user  






@testApp.get("/user_path_by_id/{uniqueId}")
async def user_path_id(uniqueId:int = Path(None, description="Enter Valid Id")):
    for key_id in listUser.keys():
        if uniqueId==key_id:
            return {"User":listUser[key_id]}
    return {"User":"not found"}


@testApp.get("/user_query_by_id")
async def user_query_id(uniqueId:int = Query(None, description="Enter Valid Id")):
    for key_id in listUser.keys():
        if uniqueId==key_id:
            return {"User":listUser[key_id]}
    return {"User":"not found"}

@testApp.post("/user_show_post",response_model=User)
async def base(user:User):
    user1=user
    return user1

@testApp.post("/user_reg", response_model=User)
async def base(user:User):
    listUser[len(listUser)+1]=user
    return user

@testApp.get("/user_all")
async def base():
    return listUser


@testApp.put("/update_info")
async def update_item(user : UserInput, user_id:int = Query(... ,describe="ID is iteger number starting from 1")):
    if user_id in listUser:
        listUser[user_id]["username"]= user.username if user.username!=None else listUser[user_id]["username"]
        listUser[user_id]["password"]= user.password if user.password!=None else listUser[user_id]["password"]
        listUser[user_id]["uniqueId"]= user.uniqueId if user.uniqueId!=None else listUser[user_id]["uniqueId"]
        return {"Success": "Entity updated", 
                "User":user}
    return "Item doesn't exist"

@testApp.delete("/delete_user")
async def delete_user(user_id: int = Query(..., describe="Enter user ID")):
    if user_id in listUser:
        del listUser[user_id]
        return {"Success":"USer deleted"}
    return {"Fail":"User doesn't exist"}




register_tortoise(
    testApp, 
    db_url="sqlite://db.users",
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)