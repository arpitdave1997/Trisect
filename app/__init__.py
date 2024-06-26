from fastapi import FastAPI
from .routes.main import mainRouter
from .routes.gameplay import gameplayRouter

def createApp():
    app = FastAPI()

    app.include_router(mainRouter)
    app.include_router(gameplayRouter)

    return app