from model.wsmanager import ConnectionManager as manager
from fastapi import WebSocket,HTTPException
from controllers.token import get_access_token
from model.core import ModelInterface,User,Battle

async def get_mapWS(websocket:WebSocket):
    try:
        await manager.connect(websocket)
        data = websocket.cookies.get("Authorization")
        id_info = get_access_token(data)
        if not await ModelInterface.get_model_filter(model=User,filter=id_info.get("email")):
            await manager.disconnect(websocket)        
    except:
        await manager.disconnect(websocket)  
    try:      
        await ModelInterface.get_stream(websocket)
    except:
        await manager.disconnect(websocket)

async def set_mapWS(websocket:WebSocket):
    try:
        await manager.connect(websocket)
        data = websocket.cookies.get("Authorization")
        id_info = get_access_token(data)
    except:
        await manager.disconnect(websocket)  
    try:      
        if not await ModelInterface.get_model_filter(model=User,filter=id_info.get("email")):
            await manager.disconnect(websocket)

        else:
            while True:
                data = await websocket.receive_json()
                if isinstance(data.get("pixel"),str) and isinstance(data.get("color"),str):
                    await ModelInterface.set_stream_pixelbattle(pixel=data.get("pixel"),color=data.get("color"))
    except:
        await manager.disconnect(websocket)

    
async def get_map(Authorization):
    id_info = get_access_token(Authorization)
    if not await ModelInterface.get_model_filter(model=User,filter=id_info.get("email")):
        raise HTTPException(status_code=422)
    data = await ModelInterface.get_model(model=Battle)
    return data

