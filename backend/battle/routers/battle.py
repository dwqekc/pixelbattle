from fastapi import APIRouter,Cookie,HTTPException,WebSocket
from controllers.map import get_map,get_mapWS,set_mapWS
from typing import Annotated,Union

router = APIRouter()

@router.get("/all_map")
async def all_map(Authorization: Annotated[Union[str, None], Cookie()] = None):
    if Authorization:
        data = await get_map(Authorization)
        return data
    else:
        raise HTTPException(status_code=422)

@router.websocket("/getmap")
async def websocket_endpoint(websocket: WebSocket):
    await get_mapWS(websocket)

@router.websocket("/setmap")
async def websocket_endpoint(websocket: WebSocket):
    await set_mapWS(websocket)