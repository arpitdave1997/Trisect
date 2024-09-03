from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.common.constants import ORIGINS
from .routes.main import mainRouter
from .routes.users import usersRouter
from .routes.gameplay import gameplayRouter

def createApp():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins = ORIGINS,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
    )

    app.include_router(mainRouter)
    app.include_router(gameplayRouter)
    app.include_router(usersRouter)

    return app