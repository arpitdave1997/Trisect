from config import Config
from app import createApp

app = createApp()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", port = Config.PORT, reload = True)
