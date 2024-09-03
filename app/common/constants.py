from datetime import datetime
from app.common.enums import GameplayType, GameplayStatus

ORIGINS = [
    "http://127.0.0.1:5501",
    "http://localhost:5501",
]

BOT_USER_ID = 'BOT_USER'
OFFLINE_USER_ID = 'OFFLINE'

ADJ = ["Brave", "Clever", "Witty", "Quick", "Bright", "Mighty", "Silent", "Swift", "Loyal", "Bold", "Sharp", "Eager", "Jolly", "Lucky", "Noble"]
NOUNS = ["Panther", "Bear", "Falcon", "Wolf", "Lion", "Tiger", "Eagle", "Dragon", "Fox", "Leopard", "Shark", "Raven", "Hawk", "Python", "Knight"]

SEARCH_OPEN_SESSION = 3
SEARCH_CREATE_SESSION = 7

class GameplaySessionObject:
    def __init__(
            self, 
            sessionId = None,
            userOneId = None,
            userTwoId = None,
            type = GameplayType.TWO_VS_RANDOM.value,
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
    
class UserObject:
    def __init__(
            self, 
            user_id = None,
            user_name = None,
            device_identifier = None,
            ip_address = None,
            online_status = None,
            last_online_timestamp = None
        ):
        self.user_id = user_id
        self.user_name = user_name
        self.device_identifier = device_identifier
        self.ip_address = ip_address
        self.online_status = online_status
        self.last_online_timestamp = last_online_timestamp

    def toJson(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'device_identifier': self.device_identifier,
            'ip_address': self.ip_address,
            'online_status': self.online_status,
            'last_online_timestamp': self.last_online_timestamp
        }
    
    def toDbObject(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'device_identifier': self.device_identifier,
            'ip_address': self.ip_address,
            'online_status': self.online_status,
            'last_online_timestamp': self.last_online_timestamp
        }
