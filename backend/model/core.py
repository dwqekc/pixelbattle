from pydantic import EmailStr
from fastapi import WebSocket
import os
import redis
from typing import Optional
from redis_om import JsonModel,Field,Migrator,NotFoundError
from model.wsmanager import ConnectionManager as manager
import asyncio

class User(JsonModel):
    email: Optional[EmailStr] = Field(index=True,default=None)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    userid: Optional[int] = Field(index=True,default=None)
    username: Optional[str] = Field(index=True,default=None)

    class Meta:
        database = redis.Redis(host=os.getenv('Broker_Host'),port=os.getenv('Broker_Port'),password=os.getenv('Broker_Password'))

class Battle(JsonModel):
    pixel: str = Field(index=True,primary_key=True)
    color: str = Field(index=True)

    class Meta:
        database = redis.Redis(host=os.getenv('Broker_Host'),port=os.getenv('Broker_Port'),password=os.getenv('Broker_Password'))

class ModelInterface:
    redis = redis.Redis(host=os.getenv('Broker_Host'),port=os.getenv('Broker_Port'),password=os.getenv('Broker_Password'))

    @classmethod
    async def get_stream(cls,websocket:WebSocket):
        while True:
            stream = cls.redis.xread(streams={"battle": "$"},block=0) 
            x = stream[0][1][0][1]
            x = {key.decode(): value.decode() for key, value in x.items()}
            if x is not None:
                await manager.send_message(x,websocket)
                await asyncio.sleep(0)

    @classmethod
    async def set_stream_pixelbattle(cls,pixel:str,color:str):
        cls.set_battle_pixel_color(pixel=pixel,color=color)
        cls.redis.xadd("battle",{"pixel":pixel,"color":color})
      
    @classmethod
    def set_user(cls,first_name: str,last_name: str,email: str = None,username: str = None,userid: int = None):
        user = User(email=email,username=username,userid=userid,first_name=first_name,last_name=last_name)
        user.save()
        
    @classmethod
    def set_battle_pixel_color(cls,pixel: str,color: str):
        battle = Battle(pixel=pixel,color=color)
        battle.save()     

    @classmethod
    def get_finduser(cls,userid: int = None,email: str = None):
        Migrator().run()
        if userid is not None:
            try:
                return User.find(User.userid == userid).first()
            except NotFoundError:
                return None
        if email is not None:
            try:
                return User.find(User.email == email).first()
            except NotFoundError:
                return None
            
    @classmethod
    async def get_model(cls,model):
        Migrator().run()
        return model.find().all()     
 
