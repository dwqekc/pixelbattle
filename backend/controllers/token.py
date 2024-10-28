import jwt
import os
import datetime
from controllers.googletoken import get_access_token as google_access
from controllers.telegramtoken import tgget_access_token
from model.core import ModelInterface
from model.schemas import TypeAuth

SECRET_KEY = os.getenv("SECRET_KEY_JWT")

def get_access_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        decode_type: str = payload.get('type')
        if decode_type == TypeAuth.google.value:
            decode_token: str = payload.get('token')
            id_info = google_access(decode_token)
            if not ModelInterface.get_finduser(email=id_info.get("email")):
                raise RuntimeError
            return id_info
        if decode_type == TypeAuth.telegram.value:
            decode_userid: str = payload.get('userid')
            user = tgget_access_token(decode_userid)
            if not ModelInterface.get_finduser(userid=user.userid): 
                raise RuntimeError
            return user
    except:
        raise RuntimeError