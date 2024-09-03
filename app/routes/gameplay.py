from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.common.enums import GameplayEvents, ExceptionLogCodes
from app.common.helpers import GameplayHelper
from app.database.supabase import Supabase

gameplayRouter = APIRouter(tags=['Gameplay APIs'])

dbClient = Supabase.initialize()

@gameplayRouter.websocket("/gameplay", name = "Gameplay Events WebSocket")
async def gameplayEvents(webSocket: WebSocket):
    await webSocket.accept()
    try:
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
    except WebSocketDisconnect as w:
        pass
    except Exception as e:
        await webSocket.send_json({'status': 'error', 'message': str(e)})
        await webSocket.close()


class GameplayHandler:

    @staticmethod
    async def initiateSession(webSocket: WebSocket, eventData: dict):
        userId = eventData.get('user_id')

        existingSessionFlag, sessionObject = GameplayHelper.searchOpenSessions(userId)
        if not existingSessionFlag:
            createSessionFlag, sessionObject = GameplayHelper.createOpenSession(userId)
            if not createSessionFlag:
                sessionObject = GameplayHelper.createBotSession(userId)

        await webSocket.send_json(sessionObject)
        return

    @staticmethod
    async def useSession(webSocket: WebSocket, eventData: dict):
        userId = eventData.get('user_id')
        sessionId = eventData.get('session_id')

        while True:
            sessionValidity, gameplayObject = GameplayHelper.checkSessionValidity(eventData)
            if not sessionValidity:
                raise Exception(ExceptionLogCodes.EXPIRED_SESSION.value)
            
            gameplayObject = GameplayHelper.processNextAction(gameplayObject, eventData.get('action_position'))
            GameplayHelper.updateSession(gameplayObject)
            await webSocket.send_json(gameplayObject.toJson())
        return 
    
    @staticmethod
    def terminateSession(webSocket: WebSocket, eventData: dict):
        return {
            'response': 'Response Message'
        }