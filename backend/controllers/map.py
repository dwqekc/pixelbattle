from model.wsmanager import ConnectionManager as manager
from fastapi import WebSocket,HTTPException
from controllers.token import get_access_token
from model.core import ModelInterface,User,Battle

async def get_mapWS(websocket:WebSocket):
    try:
        await manager.preconnect(websocket)
        data = websocket.cookies.get("Authorization")
        id_info = get_access_token(data)
        if not await ModelInterface.get_model_filter(model=User,filter=id_info.get("email")):
            await manager.predisconnect(websocket)
    except:
        await manager.predisconnect(websocket)
    else:
        await manager.connect(websocket)
        while True:
            data = await websocket.receive_json()
            if isinstance(data.get("pixel"),str) and isinstance(data.get("color"),str):
                if not await ModelInterface.get_model_filter(model=Battle,filter=data.get("pixel")):
                    await ModelInterface.set_battle_pixel_color(pixel=data.get("pixel"),color=data.get("color"))
                else:
                    await ModelInterface.update_model(model=Battle, _id=data.get("pixel"), data={"color": data['color']})
                await manager.broadcast({"pixel":data.get("pixel"),"color":data.get("color")})

async def get_map(Authorization):
    id_info = get_access_token(Authorization)
    if not await ModelInterface.get_model_filter(model=User,filter=id_info.get("email")):
        raise HTTPException(status_code=422)
    data = await ModelInterface.get_model(model=Battle)
    return data

