import json
from fastapi import APIRouter, WebSocket
from app.common.enums import GameplayEvents, GameplayType, GameplayStatus, ExceptionLogCodes
from app.common.constants import GameplaySessionObject, BOT_USER_ID, OFFLINE_USER_ID
from app.common.helpers import GameplayHelper
from app.database.supabase import Supabase

gameplayRouter = APIRouter(tags=['Gameplay APIs'])

dbClient = Supabase.initialize()

@gameplayRouter.websocket("/gameplay", name = "Gameplay Events WebSocket")
async def gameplayEvents(webSocket: WebSocket):
    await webSocket.accept()
    try:
        while True:
            eventData: dict = await webSocket.receive_json()
            eventCase: str = eventData.get('case')

            match eventCase:
                case GameplayEvents.INITIATE_SESSION.value:
                    await GameplayHandler.initiateSession(webSocket, eventData)
                case GameplayEvents.USE_SESSION.value:
                    await GameplayHandler.useSession(webSocket, eventData)
                case GameplayEvents.TERMINATE_SESSION.value:
                    GameplayHandler.terminateSession(webSocket, eventData)
                case _:
                    raise Exception(ExceptionLogCodes.INCORRECT_EVENT_CASE.value)
    except Exception as e:
        await webSocket.send_json({'status': 'error', 'message': str(e)})
    finally:
        await webSocket.close()

class GameplayHandler:

    @staticmethod
    async def initiateSession(webSocket: WebSocket, eventData: dict):
        gameplayObject = GameplaySessionObject()

        gameplayObject.type = eventData.get('type')
        gameplayObject.status = GameplayStatus.OPEN.value
        gameplayObject.userOneId = GameplayHelper.encodeUserId(eventData.get('device_identifier'))
        gameplayObject.nextAction = gameplayObject.userOneId

        match gameplayObject.type:
            case GameplayType.ONE_VS_BOT.value:
                gameplayObject.userTwoId = GameplayHelper.encodeUserId(BOT_USER_ID)
            case GameplayType.TWO_VS_OFFLINE.value:
                gameplayObject.userTwoId = GameplayHelper.encodeUserId(OFFLINE_USER_ID)
            case GameplayType.TWO_VS_ONLINE.value:
                pass
            case GameplayType.TWO_VS_RANDOM.value:
                pass
        
        gameplayObject.sessionId = GameplayHelper.createSession(gameplayObject)
        await webSocket.send_json(gameplayObject.toJson())
        return

    @staticmethod
    async def useSession(webSocket: WebSocket, eventData: dict):
        sessionValidity, gameplayObject = GameplayHelper.checkSessionValidity(eventData)
        if not sessionValidity:
            raise Exception(ExceptionLogCodes.EXPIRED_SESSION.value)
        
        gameplayObject = GameplayHelper.processNextAction(gameplayObject, eventData.get('gameplay'))
        GameplayHelper.updateSession(gameplayObject)
        await webSocket.send_json(gameplayObject.toJson())
        return 
    
    @staticmethod
    def terminateSession(webSocket: WebSocket, eventData: dict):
        return {
            'response': 'Response Message'
        }