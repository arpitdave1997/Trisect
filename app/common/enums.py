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