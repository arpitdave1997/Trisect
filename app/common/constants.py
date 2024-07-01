from datetime import datetime
from app.common.enums import GameplayType, GameplayStatus

BOT_USER_ID = 'BOT'
OFFLINE_USER_ID = 'OFFLINE'

class GameplaySessionObject:
    def __init__(
            self, 
            sessionId = None,
            userOneId = None,
            userTwoId = None,
            type = GameplayType.TWO_VS_OFFLINE.value,
            gameplay = ['', '', '', '', '', '', '', '', ''],
            status = GameplayStatus.EXPIRED.value,
            result = None,
            nextAction = None,
            lastUpdated = str(datetime.now())
        ):
        self.sessionId = sessionId
        self.userOneId = userOneId
        self.userTwoId = userTwoId
        self.type = type
        self.gameplay = gameplay
        self.status = status
        self.result = result
        self.nextAction = nextAction
        self.lastUpdated = lastUpdated

    def toJson(self):
        return {
            'session_id': self.sessionId,
            'user_one': self.userOneId,
            'user_two': self.userTwoId,
            'type': self.type,
            'gameplay': self.gameplay,
            'status': self.status,
            'result': self.result,
            'next_action': self.nextAction,
            'last_updated': self.lastUpdated,
        }
    
    def toDbObject(self):
        return {
            'user_one': self.userOneId,
            'user_two': self.userTwoId,
            'type': self.type,
            'gameplay': self.gameplay,
            'status': self.status,
            'result': self.result,
            'next_action': self.nextAction,
            'last_updated': self.lastUpdated,
        }