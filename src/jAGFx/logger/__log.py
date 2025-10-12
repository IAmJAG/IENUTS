import traceback
from inspect import currentframe
from logging import log as _log
from types import FrameType

from ..overload import OverloadDispatcher
from .__callerInformation import CallerInformation
from .__utilities import CORRATTRNAME, LOGLOCK, THREADLOCAL, StripAnsi

__all__ = [
    "log",
]


def _formatException(err: Exception):
    lErrMsg: list[str] = []
    for msg in traceback.format_exception(None, err, err.__traceback__):
        if "__processMarker.py" not in msg:
            for _msg in msg.split("\n"):
                lErrMsg.append(_msg)
            lErrMsg.append("\n")

    return [s for s in lErrMsg if s.strip() != ""]


def _XLog(level: int, message: str, extra: dict):
    _log(level, StripAnsi(f"{message}"), extra=extra)


@OverloadDispatcher
def log(message: str, level: int, err: Exception, frame: FrameType):
    lErrMsg: list[str] = _formatException(err)
    lErrMsg.insert(0, message)
    log(lErrMsg, level, frame)


@log.overload
def log(message: str, level: int, frame: FrameType):
    lIndent = " "  # * GetNestingLevel() * 2
    lCallerInfo = CallerInformation(frame)

    try:
        with LOGLOCK:
            _XLog(
                level,
                f"{lIndent}{message}",
                {
                    "caller": str(lCallerInfo).strip(),
                    "correlation": str(getattr(THREADLOCAL, CORRATTRNAME, "")),
                },
            )

    except PermissionError as e:
        raise PermissionError("Error in logging") from e

    except Exception as e:
        raise Exception("Error in logging") from e


@log.overload
def log(messages: list, level: int, frame: FrameType):
    lIndent = " "  # * GetNestingLevel() * 2

    lCallerInfo = CallerInformation(frame)

    try:
        with LOGLOCK:
            for msg in messages:
                _XLog(
                    level,
                    f"{lIndent}{msg}",
                    {
                        "caller": str(lCallerInfo),
                        "correlation": str(getattr(THREADLOCAL, CORRATTRNAME, "")),
                    },
                )

    except PermissionError as e:
        raise PermissionError("Error in logging") from e

    except Exception as e:
        raise Exception("Error in logging") from e


@log.overload
def log(messages: list, level: int, err: Exception):
    messages.extend(_formatException(err))
    log(messages, level, currentframe().f_back)


@log.overload
def log(messages: tuple, level: int):
    log(list(messages), level, currentframe().f_back)


@log.overload
def log(messages: tuple, level: int, err: Exception):
    log(list(messages), level, err, currentframe().f_back)


@log.overload
def log(messages: dict, level: int):
    log(list(messages.values()), level, currentframe().f_back)


@log.overload
def log(messages: dict, level: int, err: Exception):
    log(list(messages.values()), level, err, currentframe().f_back)
