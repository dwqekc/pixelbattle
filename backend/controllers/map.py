from model.wsmanager import ConnectionManager as manager
from fastapi import WebSocket,HTTPException
from controllers.token import get_access_token
from model.core import ModelInterface,User,Battle
import datetime
from model.schemas import InfoAccount

async def get_mapWS(websocket:WebSocket):
    try:
        await manager.connect(websocket)
        data = websocket.cookies.get("Authorization")
        get_access_token(data)       
    except:
        await manager.disconnect(websocket)  
    try:      
        await ModelInterface.get_stream(websocket)
    except:
        await manager.disconnect(websocket)


async def set_mapWS(websocket:WebSocket):
    try:
        await manager.connect(websocket)
        cookie = websocket.cookies.get("Authorization")
        get_access_token(cookie)
        while True:
            data = await websocket.receive_json()
            if isinstance(data.get("pixel"),str) and isinstance(data.get("color"),str):
                user = get_access_token(cookie)
                date_now = datetime.datetime.now(datetime.timezone.utc)
                date_user = user.last_activity + datetime.timedelta(seconds=InfoAccount.delay.value)
                if date_now >= date_user:
                    user.last_activity = datetime.datetime.now(datetime.timezone.utc)
                    user.save()
                    await manager.send_message({"wait":False,"last_activity":f"{date_user}"},websocket)
                    await ModelInterface.set_stream_pixelbattle(pixel=data.get("pixel"),color=data.get("color"))
                else:
                    timedelta = date_user-date_now
                    await manager.send_message({"wait":True,"last_activity":f"{date_user}","wait_time":timedelta.total_seconds()},websocket)              
    except:
        await manager.disconnect(websocket)     

    
async def get_map(Authorization):
    try:
        user = get_access_token(Authorization)
        date_user = user.last_activity + datetime.timedelta(seconds=InfoAccount.delay.value)
        data = await ModelInterface.get_model(model=Battle)
        return {"last_activity":date_user,"data_map":data}
    except:
        raise HTTPException(status_code=422)

