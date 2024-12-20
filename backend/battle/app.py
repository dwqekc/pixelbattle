from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from battle.routers.battle import router as battle_router

app = FastAPI(root_path="/api")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=battle_router,
    prefix='/battle',
)
