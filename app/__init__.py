from fastapi import FastAPI
from .routes.main import mainRouter
from .routes.users import usersRouter
from .routes.gameplay import gameplayRouter

def createApp():
    app = FastAPI()

    app.include_router(mainRouter)
    app.include_router(gameplayRouter)
    app.include_router(usersRouter)

    return app