from enum import Enum

class GameplayEvents(Enum):
    INITIATE_SESSION = 'initiate_session'
    USE_SESSION = 'use_session'
    TERMINATE_SESSION = 'terminate_session'

class GameplayType(Enum):
    ONE_VS_BOT = 'one_vs_bot'
    TWO_VS_OFFLINE = 'two_vs_offline'
    TWO_VS_RANDOM = 'two_vs_random'
    TWO_VS_ONLINE = 'two_vs_online'

class GameplayStatus(Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    EXPIRED = 'expired'

class ExceptionLogCodes(Enum):
    INCORRECT_EVENT_CASE = "Hey! Looks like there's some issue with the server. How about we restart the game?"
    INCORRECT_SESSION_ID = "Hey! Looks like there's some issue with the server. How about we restart the game?"
    EXPIRED_SESSION = 'Oops! It looks like the session expired. How about we start a new game?'
    EXCEPTION_CREATE_SESSION = "It's not you, it's me! Looks like our servers are down at the moment. You can try again or come back later in some time"
    EXCEPTION_UPDATE_SESSION = "It's not you, it's me! Looks like our servers are down at the moment. You can try again or come back later in some time"
    