from src.auth.database import User
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead
from src.auth.auth import auth_backend
from src.operations.router import router as router_operation

from fastapi import Depends, FastAPI
import fastapi_users

from pydantic import BaseModel
from pydantic import Field

from enum import Enum
from typing import List, Optional
from datetime import datetime

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.requests import Request
from starlette.responses import Response

app=FastAPI(title='Some App')

fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"

@app.get("/unprotected-route")
def unprotected_route():
    return "Hello anonymus"

#redis
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")







"""fake_users=[
    {'id':1,'role':'admin','name':'Bob'},
    {'id':2,'role':'user','name':'Sam'},
    {'id':3,'role':'manager','name':'Jack'},
    {'id':4,'role':'user','name':'W', 'degree':[{'id':1,
                                                 "created_at":"2020-01-01T00:00:00",
                                                 'type_degree':'expert'}
    ]},
]

class DegreeType(Enum):
    newbie='newbie'
    expert='expert'

class Degree(BaseModel):
    id: int
    created_at:datetime
    type_degree:DegreeType


class User(BaseModel):
    id:int
    role:str
    name:str
    degree: Optional[List[Degree]] = []

@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id:int):
    return [user for user in fake_users if user.get('id')==user_id]

fake_trades=[
    {'id':1, 'user_id':1,'currency':'BTC','side':'buy','price':123,'amount':2.12},
    {'id':2, 'user_id':1,'currency':'BTC','side':'buy','price':12,'amount':2.12},
]

@app.get('/trades')
def get_trades(limit: int = 1, offset:int = 0):
    return fake_trades[offset:][:limit]

fake_users2=[
    {'id':1,'role':'admin','name':'Bob'},
    {'id':2,'role':'user','name':'Sam'},
    {'id':3,'role':'manager','name':'Jack'}
]

@app.post('/users/{user_id}')
def change_user_name(user_id:int, new_name:str):
    current_user=list(filter(lambda user:user.get('id') == user_id, fake_users2))[0]
    current_user['name']=new_name
    return{'status': 200, 'data': current_user}

class Trade(BaseModel):
    id: int
    user_id:int
    currency: str = Field(max_length=5)
    side:str
    price:float = Field(ge=0)
    amount:float

@app.post('/trades')
def add_trades(trades: list[Trade]):
    fake_trades.extend(trades)
    return {'status':200,'data':fake_trades}"""
