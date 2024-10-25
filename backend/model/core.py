from pydantic import EmailStr
from fastapi import WebSocket
from pydantic_redis.asyncio import Model, Store, RedisConfig
import os
import redis
from model.wsmanager import ConnectionManager as manager
import asyncio

class User(Model):
    _primary_key_field: str = 'email'
    email: EmailStr
    first_name: str
    last_name: str

class Battle(Model):
    _primary_key_field: str = 'pixel'
    pixel: str
    color: str

class ModelInterface:
    store = Store(name='db', redis_config=RedisConfig(host=os.getenv('Broker_Host'), port=os.getenv('Broker_Port'),password=os.getenv('Broker_Password')))
    redis = redis.Redis(host=os.getenv('Broker_Host'),port=os.getenv('Broker_Port'),password=os.getenv('Broker_Password'))
    store.register_model(User)
    store.register_model(Battle)

    @classmethod
    async def get_stream(cls,websocket:WebSocket):
        while True:
            stream = cls.redis.xread(streams={"battle": "$"},block=0) 
            x = stream[0][1][0][1]
            x = {key.decode(): value.decode() for key, value in x.items()}
            await manager.send_message(x,websocket)
            await asyncio.sleep(0)
    
    @classmethod
    async def set_stream_pixelbattle(cls,pixel:str,color:str):
        await cls.set_battle_pixel_color(pixel=pixel,color=color)
        cls.redis.xadd("battle",{"pixel":pixel,"color":color})
      
    @classmethod
    async def set_user(cls,email: str,first_name: str,last_name:str):
        await User.insert(User(email=email,first_name=first_name,last_name=last_name))
    
    @classmethod
    async def set_battle_pixel_color(cls,pixel: str,color: str):
        await Battle.insert(Battle(pixel=pixel,color=color))        

    @classmethod
    async def update_model(cls,model,_id:str,data:list):
        await model.update(_id=_id,data=data)  

    @classmethod
    async def delete_data(cls,model,filter:list):
        await model.delete(ids=filter)

    @classmethod
    async def get_model_filter(cls,model,filter:str):
        return await model.select(ids=[filter])
    
    @classmethod    
    async def get_model_filter_column(cls,model,filter:str,column:str):
        return await model.select(ids=[filter],columns=[column])    
    
    @classmethod
    async def get_model_column(cls,model,column:str):
        return await model.select(columns=[column]) 

    @classmethod
    async def get_model(cls,model):
        return await model.select()      
 
