
from model.core import ModelInterface
import os
from fastapi import HTTPException
import jwt
import os
import datetime
import google.auth.transport.requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from model.schemas import TypeAuth

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = os.getenv("OAUTHLIB_INSECURE_TRANSPORT", default="1")
SECRET_KEY = os.getenv("SECRET_KEY_JWT")

CLIENT_CONFIG = {
    "web": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")]
    }
}

flow = Flow.from_client_config(client_config=CLIENT_CONFIG, scopes=['openid','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile'],
    redirect_uri=CLIENT_CONFIG['web']['redirect_uris'][0])
interface = ModelInterface()


def create_link():
    authorization_url,state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent')
    return authorization_url

async def create_access_token(request):
    try:
        flow.fetch_token(authorization_response=str(request.url))
        credentials = flow.credentials
        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=google.auth.transport.requests.Request(),
            audience=CLIENT_CONFIG['web']['client_id']
        )
        if not ModelInterface.get_finduser(email=id_info.get("email")):  
            ModelInterface.set_user(type=TypeAuth.google.value,first_name=id_info.get("given_name"),last_name=id_info.get("family_name"),email=id_info.get("email"))     
        expire = credentials.expiry.replace(tzinfo=datetime.timezone.utc)
        to_encode = {"type":"google","token":credentials._id_token}
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256") 
        return encoded_jwt,expire
    except Exception as e:
        raise HTTPException(status_code=422,detail=str(e))

def get_access_token(Authorization):
    id_info = id_token.verify_oauth2_token(
        id_token=Authorization,
        request=google.auth.transport.requests.Request(),
        audience=CLIENT_CONFIG['web']['client_id']
    )
    return id_info
