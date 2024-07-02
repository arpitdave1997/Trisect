import base64
from app.database.supabase import Supabase
from app.common.constants import GameplaySessionObject
from app.common.enums import GameplayStatus

dbClient = Supabase.initialize()

class GameplayHelper:

    @staticmethod
    def createSession(gameplayObject: GameplaySessionObject):
        dbResponse = dbClient.table('gameplay').insert(gameplayObject.toDbObject()).execute()
        if dbResponse.count == 0:
            raise Exception('[GAMEPLAY] : Issue while creating new Session record in DB')
        
        return dbResponse.data[0]['session_id']
        
    @staticmethod
    def updateSession(gameplayObject: GameplaySessionObject):
        dbResponse = dbClient.table('gameplay').update(gameplayObject.toDbObject()).eq('session_id', gameplayObject.sessionId).execute()
        if dbResponse.count == 0:
            raise Exception('[GAMEPLAY] : Issue while updating existing Session record in DB')
        
        return

    @staticmethod
    def checkSessionValidity(eventJson: dict):
        sessionValidity = True
        sessionId = eventJson.get('session_id')
        currentAction = eventJson.get('current_action')
        if not sessionId:
            raise Exception('[GAMEPLAY] : Session ID is not passed')
        
        dbResponse = dbClient.table('gameplay').select('*').eq('session_id', sessionId).execute()
        if dbResponse.count == 0:
            raise Exception('[GAMEPLAY] : No record present with this Session ID')
        
        gameplayObject: GameplaySessionObject = GameplayHelper.mapGameplayObject(dbResponse.data[0])
        if gameplayObject.status != GameplayStatus.OPEN.value or gameplayObject.result != None or currentAction != gameplayObject.nextAction:
            raise Exception('[GAMEPLAY] : Session is either closed, expired or it is not your turn')
        
        return sessionValidity, gameplayObject

    @staticmethod
    def mapGameplayObject(dbData: dict):
        gameplayObject: GameplaySessionObject = GameplaySessionObject(
            sessionId = dbData.get('session_id'),
            userOneId = dbData.get('user_one'),
            userTwoId = dbData.get('user_two'),
            type = dbData.get('type'),
            status = dbData.get('status'),
            result = dbData.get('result'),
            gameplay = dbData.get('gameplay'),
            lastUpdated = dbData.get('last_updated'),
            nextAction = dbData.get('next_action')
        )

        return gameplayObject
    
    @staticmethod
    def processNextAction(gameplayObject: GameplaySessionObject, gameplay: list[str]):
        if  (gameplay[0].startswith(gameplayObject.nextAction) and gameplay[1].startswith(gameplayObject.nextAction) and gameplay[2].startswith(gameplayObject.nextAction)) or \
            (gameplay[3].startswith(gameplayObject.nextAction) and gameplay[4].startswith(gameplayObject.nextAction) and gameplay[5].startswith(gameplayObject.nextAction)) or \
            (gameplay[6].startswith(gameplayObject.nextAction) and gameplay[7].startswith(gameplayObject.nextAction) and gameplay[8].startswith(gameplayObject.nextAction)) or \
            (gameplay[0].startswith(gameplayObject.nextAction) and gameplay[3].startswith(gameplayObject.nextAction) and gameplay[6].startswith(gameplayObject.nextAction)) or \
            (gameplay[1].startswith(gameplayObject.nextAction) and gameplay[4].startswith(gameplayObject.nextAction) and gameplay[7].startswith(gameplayObject.nextAction)) or \
            (gameplay[2].startswith(gameplayObject.nextAction) and gameplay[5].startswith(gameplayObject.nextAction) and gameplay[8].startswith(gameplayObject.nextAction)) or \
            (gameplay[0].startswith(gameplayObject.nextAction) and gameplay[4].startswith(gameplayObject.nextAction) and gameplay[8].startswith(gameplayObject.nextAction)) or \
            (gameplay[2].startswith(gameplayObject.nextAction) and gameplay[4].startswith(gameplayObject.nextAction) and gameplay[6].startswith(gameplayObject.nextAction)):

            gameplayObject.result = gameplayObject.nextAction
            gameplayObject.status = GameplayStatus.CLOSED.value

        gameplayObject.gameplay = gameplay
        gameplayObject.nextAction = gameplayObject.userTwoId if gameplayObject.nextAction == gameplayObject.userOneId else gameplayObject.userOneId

        return gameplayObject

    @staticmethod
    def encodeUserId(deviceIdentifier: str):
        inputBytes = deviceIdentifier.encode('utf-8')
        encodedBytes = base64.urlsafe_b64encode(inputBytes)
        encodedString = encodedBytes.decode('utf-8')
        return encodedString 
       
    @staticmethod
    def decodeUserId(deviceHash: str):
        encodedBytes = deviceHash.encode('utf-8')
        decodedBytes = base64.urlsafe_b64decode(encodedBytes)
        decodedString = decodedBytes.decode('utf-8')
        return decodedString
        