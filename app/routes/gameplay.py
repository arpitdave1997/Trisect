import json
from fastapi import APIRouter, WebSocket
from app.static.constants import GameplayEvents, GameplayType
from app.database.supabase import Supabase

gameplayRouter = APIRouter(tags=['Gameplay APIs'])

dbClient = Supabase.initialize()

@gameplayRouter.websocket("/gameplay", name = "Gameplay Events WebSocket")
async def gameplayEvents(webSocket: WebSocket):
    await webSocket.accept()
    try:
        eventData = json.loads(await webSocket.receive_text())
        eventCase = eventData.get('case')

        match eventCase:
            case GameplayEvents.INITIATE_SESSION.value:
                GameplayHandler.initiateSession(webSocket, eventData)
            case GameplayEvents.RETRIEVE_SESSION.value:
                GameplayHandler.retrieveSession(webSocket, eventData)
            case _:
                raise Exception
    except Exception as e:
        await webSocket.send_json({'status':False, 'message': e})
    finally:
        await webSocket.close()

class GameplayHandler:

    @staticmethod
    def initiateSession(webSocket: WebSocket, eventData: dict):
        try:
            sessionId = None

            gameplayType = eventData.get('gameplay_type')
            userOneId = eventData.get('user_one')
            userTwoId = eventData.get('user_two', None)

            while True:
                match gameplayType:
                    case GameplayType.ONE_VS_BOT.value:
                        pass
                    case GameplayType.TWO_VS_OFFLINE.value:
                        pass
                    case GameplayType.TWO_VS_ONLINE.value:
                        pass
                    case GameplayType.TWO_VS_RANDOM.value:
                        pass
                    case _:
                        raise Exception

        except Exception as e:
            raise Exception(e)

    @staticmethod
    def retrieveSession(webSocket: WebSocket, eventData: dict):
        return {
            'response': 'Response Message'
        }