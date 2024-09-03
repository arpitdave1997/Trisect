import base64
import time
import random
from datetime import datetime 
from app.database.supabase import Supabase
from app.common.constants import ADJ, BOT_USER_ID, NOUNS, SEARCH_CREATE_SESSION, SEARCH_OPEN_SESSION, GameplaySessionObject, UserObject
from app.common.enums import GameplayStatus, ExceptionLogCodes, GameplayType

dbClient = Supabase.initialize()

class GameplayHelper:

    @staticmethod
    def searchOpenSessions(userId: str):
        for waitTime in range(SEARCH_OPEN_SESSION):
            time.sleep(1)
            dbResponse = dbClient.table('gameplay').select('*').is_("user_two", None).neq("user_one", userId).execute()
            if dbResponse.data:
                break

        if not dbResponse.data:
            return False, None
            
        gameplayObject = GameplayHelper.mapGameplayObject(dbResponse.data[0])
        gameplayObject.userTwoId = userId
        dbResponse = dbClient.table('gameplay').update(gameplayObject.toDbObject()).eq('session_id', gameplayObject.sessionId).execute()
        if not dbResponse.data:
            raise Exception(ExceptionLogCodes.EXCEPTION_UPDATE_SESSION.value)

        return True, gameplayObject.toJson()
    
    @staticmethod
    def createOpenSession(userId: str):
        gameplayObject: GameplaySessionObject = GameplaySessionObject(
            sessionId = None,
            userOneId = userId,
            userTwoId = None,
            type = GameplayType.TWO_VS_RANDOM.value,
            gameplay = ['', '', '', '', '', '', '', '', ''],
            status = GameplayStatus.OPEN.value,
            result = None,
            nextAction = userId,
            lastUpdated = str(datetime.now())            
        )

        dbResponse = dbClient.table('gameplay').insert(gameplayObject.toDbObject()).execute()
        if not dbResponse.data:
            raise Exception(ExceptionLogCodes.EXCEPTION_UPDATE_SESSION.value)
        else:
            sessionId = dbResponse.data[0].get('session_id')

            for waitTime in range(SEARCH_CREATE_SESSION):
                time.sleep(1)
                dbResponse = dbClient.table('gameplay').select('*').eq('session_id', sessionId).execute()
                if not dbResponse.data:
                    return False, None
                elif dbResponse.data[0].get('user_two') != None:
                    break

            if dbResponse.data[0].get('user_two') != None:
                return True, GameplayHelper.mapGameplayObject(dbResponse).toJson()
            else:
                dbResponse = dbClient.table('gameplay').delete().eq('session_id', sessionId).execute()
                return False, None

    @staticmethod
    def createBotSession(userId: str):
        gameplayObject: GameplaySessionObject = GameplaySessionObject(
            sessionId = None,
            userOneId = userId,
            userTwoId = GameplayHelper.encodeUserId(BOT_USER_ID),
            type = GameplayType.TWO_VS_BOT.value,
            gameplay = ['', '', '', '', '', '', '', '', ''],
            status = GameplayStatus.OPEN.value,
            result = None,
            nextAction = userId,
            lastUpdated = str(datetime.now())            
        )
        dbResponse = dbClient.table('gameplay').insert(gameplayObject.toDbObject()).execute()
        if not dbResponse.data:
            raise Exception(ExceptionLogCodes.EXCEPTION_UPDATE_SESSION.value)
        return True, GameplayHelper.mapGameplayObject(dbResponse.data[0]).toJson()
        
    @staticmethod
    def updateSession(gameplayObject: GameplaySessionObject):
        dbResponse = dbClient.table('gameplay').update(gameplayObject.toDbObject()).eq('session_id', gameplayObject.sessionId).execute()
        if not dbResponse.data:
            raise Exception(ExceptionLogCodes.EXCEPTION_UPDATE_SESSION.value)
        
        return

    @staticmethod
    def checkSessionValidity(eventJson: dict):
        sessionValidity = True
        sessionId = eventJson.get('session_id')
        currentAction = eventJson.get('current_action')
        if not sessionId:
            raise Exception(ExceptionLogCodes.INCORRECT_SESSION_ID.value)
        
        dbResponse = dbClient.table('gameplay').select('*').eq('session_id', sessionId).execute()
        if not dbResponse.data:
            raise Exception(ExceptionLogCodes.INCORRECT_SESSION_ID.value)
        
        gameplayObject: GameplaySessionObject = GameplayHelper.mapGameplayObject(dbResponse.data[0])
        if gameplayObject.status != GameplayStatus.OPEN.value or currentAction != gameplayObject.nextAction:
            raise Exception(ExceptionLogCodes.EXPIRED_SESSION.value)
        
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
    def processNextAction(gameplayObject: GameplaySessionObject, actionPosition: str):
        actionUserType = "A" if gameplayObject.nextAction == gameplayObject.userOneId else "B"
        actionMarker = "A1" if gameplayObject.nextAction == gameplayObject.userOneId else "B1"

        if gameplayObject.gameplay[int(actionPosition) - 1] != "":
            raise Exception(ExceptionLogCodes.INCORRECT_EVENT_CASE.value) 

        for pos, el in enumerate(gameplayObject.gameplay):
            if el.startswith("A") and actionUserType == "A":
                if el == "A1":
                    gameplayObject.gameplay[pos] = "A2"
                elif el == "A2":
                    gameplayObject.gameplay[pos] = "A3"
                elif el == "A3":
                    gameplayObject.gameplay[pos] = "A4"
                elif el == "A4":
                    gameplayObject.gameplay[pos] = ""
            elif el.startswith("B") and actionUserType == "B":
                if el == "B1":
                    gameplayObject.gameplay[pos] = "B2"
                elif el == "B2":
                    gameplayObject.gameplay[pos] = "B3"
                elif el == "B3":
                    gameplayObject.gameplay[pos] = "B4"
                elif el == "B4":
                    gameplayObject.gameplay[pos] = ""

        gameplayObject.gameplay[int(actionPosition) - 1] = actionMarker

        if  (gameplayObject.gameplay[0].startswith(actionUserType) and gameplayObject.gameplay[1].startswith(actionUserType) and gameplayObject.gameplay[2].startswith(actionUserType)) or \
            (gameplayObject.gameplay[3].startswith(actionUserType) and gameplayObject.gameplay[4].startswith(actionUserType) and gameplayObject.gameplay[5].startswith(actionUserType)) or \
            (gameplayObject.gameplay[6].startswith(actionUserType) and gameplayObject.gameplay[7].startswith(actionUserType) and gameplayObject.gameplay[8].startswith(actionUserType)) or \
            (gameplayObject.gameplay[0].startswith(actionUserType) and gameplayObject.gameplay[3].startswith(actionUserType) and gameplayObject.gameplay[6].startswith(actionUserType)) or \
            (gameplayObject.gameplay[1].startswith(actionUserType) and gameplayObject.gameplay[4].startswith(actionUserType) and gameplayObject.gameplay[7].startswith(actionUserType)) or \
            (gameplayObject.gameplay[2].startswith(actionUserType) and gameplayObject.gameplay[5].startswith(actionUserType) and gameplayObject.gameplay[8].startswith(actionUserType)) or \
            (gameplayObject.gameplay[0].startswith(actionUserType) and gameplayObject.gameplay[4].startswith(actionUserType) and gameplayObject.gameplay[8].startswith(actionUserType)) or \
            (gameplayObject.gameplay[2].startswith(actionUserType) and gameplayObject.gameplay[4].startswith(actionUserType) and gameplayObject.gameplay[6].startswith(actionUserType)):

            gameplayObject.result = gameplayObject.nextAction
            gameplayObject.status = GameplayStatus.CLOSED.value
            gameplayObject.nextAction = None
        else:
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
         
class UsersHelper:

    @staticmethod
    def fetchUserInfo(deviceIdentifier: str):
        dbResponse = dbClient.table('users').select('*').eq('device_identifier', deviceIdentifier).execute()
        if not dbResponse.data:
            return False, None

        userObject = UsersHelper.mapUserObject(dbResponse.data[0])
        return True, userObject

    @staticmethod
    def createUser(deviceIdentifier: str):
        userObject: UserObject = UserObject(
            user_id = UsersHelper.encodeUserId(deviceIdentifier),
            user_name = UsersHelper.generateUserName(),
            device_identifier = deviceIdentifier,
            ip_address = None,
            online_status = True,
            last_online_timestamp = str(datetime.now())
        )

        dbResponse = dbClient.table('users').insert(userObject.toDbObject()).execute()
        if not dbResponse.data:
            raise Exception(ExceptionLogCodes.EXCEPTION_CREATE_SESSION.value)

        return userObject

    @staticmethod
    def generateUserName():
        adjective = random.choice(ADJ)
        noun = random.choice(NOUNS)
        
        username = f"{adjective}{noun}"
        return username

    @staticmethod
    def updateUserActivity(userId: str):
        dbResponse = dbClient.table('users').select('*').eq('user_id', userId).execute()
        if not dbResponse.data:
            return False
    
        dbResponse = dbClient.table('users').update({'last_online_timestamp': str(datetime.now())}).eq('user_id', userId).execute()
        if not dbResponse.data:
            return False
        
        return True
        
    @staticmethod
    def mapUserObject(dbData: dict):
        userObject: UserObject = UserObject(
            user_id = dbData.get('user_id'),
            user_name = dbData.get('user_name'),
            device_identifier = dbData.get('device_identifier'),
            ip_address = dbData.get('ip_address'),
            online_status = dbData.get('online_status'),
            last_online_timestamp = dbData.get('last_online_timestamp')
        )

        return userObject    

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

