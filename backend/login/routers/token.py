from fastapi import Request,APIRouter
from fastapi.responses import RedirectResponse
from controllers.token import create_access_token,create_link,get_access_token
import datetime
import os

router = APIRouter()

@router.get("/google")
async def login_google():
    authorization_url = create_link()
    return {"url":authorization_url}

@router.get("/callback")
async def google_callback(request:Request):
    Authorization,expires = await create_access_token(request)
    timestamp_utc = expires.replace(tzinfo=datetime.timezone.utc)
    response = RedirectResponse(os.getenv("REDIRECT_APP"))
    response.set_cookie(key="Authorization", value=Authorization,expires=timestamp_utc)
    return response
