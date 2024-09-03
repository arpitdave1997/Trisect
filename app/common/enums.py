from enum import Enum

#region Logging & Responses
class ResponseStatusCodes(Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'

class ExceptionLogCodes(Enum):
    INCORRECT_EVENT_CASE = "Hey! Looks like there's some issue with the server. How about we restart the game?"
    INCORRECT_SESSION_ID = "Hey! Looks like there's some issue with the server. How about we restart the game?"
    EXPIRED_SESSION = 'Oops! It looks like the session expired. How about we start a new game?'
    EXCEPTION_CREATE_SESSION = "It's not you, it's me! Looks like our servers are down at the moment. You can try again or come back later in some time"
    EXCEPTION_REGISTER_USER = "It's not you, it's me! Looks like our servers are down at the moment. You can try again or come back later in some time"
    EXCEPTION_UPDATE_SESSION = "It's not you, it's me! Looks like our servers are down at the moment. You can try again or come back later in some time"
#endregion

#region Gameplay
class GameplayEvents(Enum):
    INITIATE_SESSION = 'initiate_session'
    USE_SESSION = 'use_session'
    TERMINATE_SESSION = 'terminate_session'

class GameplayType(Enum):
    TWO_VS_BOT = 'one_vs_bot'
    TWO_VS_RANDOM = 'two_vs_random'

class GameplayStatus(Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    EXPIRED = 'expired'
#endregion