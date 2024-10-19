from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from login.routers.token import router as login_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=login_router,
    prefix='/login',
)
