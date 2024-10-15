from utils.utils import EnhancedStrEnum

class LogType(EnhancedStrEnum):
    CRITICAL: str = 'CRITICAL'
    DEBUG: str = 'DEBUG'
    ERROR: str = 'ERROR'
    INFO: str = 'INFO'
    WARN: str = 'WARN'