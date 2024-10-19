from pydantic import EmailStr
from pydantic_redis.asyncio import Model, Store, RedisConfig
import os

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
    store = Store(name='db', redis_config=RedisConfig(host=os.getenv('Broker_Host'), port=os.getenv('Broker_Port'),password=os.getenv('Broker_Password',default=None)))
    store.register_model(User)
    store.register_model(Battle)

    @classmethod
    async def set_user(cls,email: str,first_name: str,last_name:str):
        await User.insert(User(email=email,first_name=first_name,last_name=last_name))
    
    @classmethod
    async def set_battle_pixel_color(cls,pixel: str,color: str):
        await Battle.insert(Battle(pixel=pixel,color=color))        
    
    @classmethod
    async def update_model(cls,model:str,_id:str,data:list):
        await model.update(_id=_id,data=data)  

    @classmethod
    async def get_model_filter(cls,model:str,filter:str):
        return await model.select(ids=[filter])
    
    @classmethod    
    async def get_model_filter_column(cls,model:str,filter:str,column:str):
        return await model.select(ids=[filter],columns=[column])    
    
    @classmethod
    async def get_model(cls,model:str):
        return await model.select()      
 
