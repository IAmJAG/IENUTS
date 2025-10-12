from enum import Enum

__all__ = [
    "eLogLevel"
]


class eLogLevel(Enum):  # noqa: N801
    NOTSET = 0
    STATUS = 5
    DEBUG = 10
    INFO = 20
    WARNING = 30
    WARN = WARNING
    ERROR = 40
    ERR = ERROR
    CRITICAL = 50
    FATAL = CRITICAL
