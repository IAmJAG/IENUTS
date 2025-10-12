import atexit
import re
import sys
import traceback
from inspect import currentframe
from json import load
from logging import CRITICAL, DEBUG, Handler, getHandlerByName
from logging import log as _log
from logging.config import dictConfig
from logging.handlers import QueueHandler
from re import Pattern
from threading import Lock, local
from types import FrameType

from ..types import eAnsiColors, eLogLevel

THREADLOCAL: local = local()

__all__ = [
    "CORRATTRNAME",
    "CORRATTRNEST",
    "LOGLEVEL",
    "SKIPMODULES",
    "THREADLOCAL",
    "GetCallerInfoFromFrame",
    "StripAnsi",
]

LOGLEVEL: int = DEBUG
LOGLOCK = Lock()
CORRATTRNAME = "__correlationId__"
CORRATTRNEST = "__correlationNest__"

SKIPMODULES = (
    "jAGFx.logger",
    "jAGFx.overload",
    "_pydevd_bundle",
    "pydevd_pydevd_extension",
)
DEFLOGGERCFGFILENAME = "logger.cfg"

EXITONERROR: bool = True


def StripAnsi(text):
    ansi_re: Pattern = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_re.sub("", text) if isinstance(text, str) else text


def ExitOnError(err: Exception):
    if EXITONERROR:
        lExitCode: int = -1
        if hasattr(err, "errno"):
            lExitCode = err.errno

        lIndent = " " * GetNestingLevel() * 2
        lCurentFrame = currentframe()
        try:
            lCallerInfoType = globals()["CallerInformation"]
            lCallerInfo = lCallerInfoType(lCurentFrame.f_back)

        except KeyError:
            lCallerInfo = lCurentFrame.f_back

        # with LOGLOCK:
        #     for line in traceback.format_exception(err):
        #         lClean = StripAnsi(line)
        #         _log(CRITICAL, f"{lIndent}{lClean}", {"caller": str(lCallerInfo)})

        sys.exit(lExitCode)


def GetCallerInfoFromFrame(frame: FrameType) -> tuple[str, str, str]:
    lModuleName = frame.f_globals.get("__name__", "")
    lMemberName = frame.f_code.co_name or ""

    lLocalSelf = frame.f_locals.get("self", "")  # Get the class instance if it exists
    lClassName = (
        ""
        if isinstance(lLocalSelf, str) and lLocalSelf.strip() == ""
        else lLocalSelf.__class__.__name__
    )

    return lModuleName, lClassName, lMemberName


# def GetNestingLevel() -> int:
#     lLevel = 0
#     lFrame = currentframe()
#     while lFrame:
#         lFrame = lFrame.f_back
#         lModule = getmodule(lFrame)
#         if hasattr(lFrame, "f_code"):
#             if lFrame.f_code.co_name == "<module>":
#                 if lModule:
#                     if lModule.__name__ == "__main__":
#                         return lLevel

#         if lModule and not lModule.__name__.startswith(SKIPMODULES):
#             lLevel += 1

#     return lLevel


def getFQN(frame: FrameType) -> str:
    lFQN: str = ""
    if frame:
        lModuleName = frame.f_globals.get("__name__", "")
        lClassName = ""
        if "self" in frame.f_locals:
            lClassName = frame.f_locals["self"].__class__.__name__

        lFuncName = frame.f_code.co_name
        lFQN = f"{lModuleName}.{lClassName + '.' if lClassName else ''}{lFuncName}"

    return lFQN


def GetNestingLevel() -> int:
    lLevel = 0
    lFrame = currentframe()
    lCallerFrame = lFrame.f_back if lFrame else None
    lFrame = lCallerFrame
    lFramesFQN: list[str] = []
    while lFrame:
        lCFrameFQN = getFQN(lFrame)
        if lCFrameFQN.startswith(SKIPMODULES):
            lFrame = lFrame.f_back
            continue

        lFramesFQN.append(lCFrameFQN)
        lLevel += 1
        lFrame = lFrame.f_back

    for lFQN in reversed(lFramesFQN):
        if not lFQN.startswith(SKIPMODULES):
            return lLevel - 2

        lLevel -= 1

    return 0


def Initialize(cfg: dict | None = None):
    def cleanup():
        nonlocal lHandler
        if lHandler and isinstance(lHandler, QueueHandler):
            lHandler.listener.stop()
            lHandler = None

    if cfg is None:
        try:
            with open(DEFLOGGERCFGFILENAME) as f:
                cfg = load(fp=f)

        except (AttributeError, KeyError, FileNotFoundError):
            cfg = {
                "version": 1,
                "disable_existing_loggers": True,
                "formatters": {
                    "console": {
                        "class": "jAGFx.Logger.ColoredFormatter",
                        "format": "[{asctime}][{levelname:<8}] {message}",
                        "timeformat": "%Y%m%d%H%M%S%z",
                        "secformat": "%s %03d",
                        "datefmt": "%Y%m%d",
                        "style": "{",
                        "colorCodes": {
                            "DEFAULT": {
                                eLogLevel.NOTSET: eAnsiColors.COLOR_WHITE,  # Default color
                                eLogLevel.STATUS: eAnsiColors.COLOR_WHITE,  # STATUS
                                eLogLevel.DEBUG: eAnsiColors.COLOR_BLUE,  # DEBUG
                                eLogLevel.INFO: eAnsiColors.COLOR_GREEN,  # INFO
                                eLogLevel.WARNING: eAnsiColors.COLOR_YELLOW,  # WARNING
                                eLogLevel.ERROR: eAnsiColors.COLOR_RED,  # ERROR
                                eLogLevel.CRITICAL: eAnsiColors.COLOR_BRIGHT_RED,  # CRITICAL
                            },
                            "asctime": {eLogLevel.NOTSET: eAnsiColors.COLOR_MAGENTA},
                            "levelname": {
                                eLogLevel.NOTSET: eAnsiColors.COLOR_WHITE,  # Default color
                                eLogLevel.STATUS: eAnsiColors.COLOR_WHITE,  # STATUS
                                eLogLevel.DEBUG: eAnsiColors.COLOR_BLUE,  # DEBUG
                                eLogLevel.INFO: eAnsiColors.COLOR_GREEN,  # INFO
                                eLogLevel.WARNING: eAnsiColors.COLOR_YELLOW,  # WARNING
                                eLogLevel.ERROR: eAnsiColors.COLOR_RED,  # ERROR
                                eLogLevel.CRITICAL: eAnsiColors.COLOR_BRIGHT_RED,  # CRITICAL
                            },
                        },
                    },
                    "file": {
                        "style": "{",
                        "format": "[{asctime}][{caller}][{levelname:<8}][{thread:>08}] {message}",
                        "timeformat": "%H%M%S%z",
                        "secformat": "%s %03d",
                        "datefmt": "%Y%m%d",
                    },
                },
                "filters": {"ModuleFilter": {"class": "jAGFx.Logger.LogFilter"}},
                "handlers": {
                    "stdout": {
                        "class": "logging.StreamHandler",
                        "level": "NOTSET",
                        "stream": "ext://sys.stderr",
                        "formatter": "console",
                    },
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "NOTSET",
                        "filename": "./LOGS/jAGFx.log",
                        "maxBytes": 100000,
                        "backupCount": 5,
                        "formatter": "file",
                    },
                    "offThread": {
                        "class": "logging.handlers.QueueHandler",
                        "handlers": ["stdout", "file"],
                        "filters": ["ModuleFilter"],
                        "respect_handler_level": True,
                    },
                },
                "loggers": {"root": {"level": "NOTSET", "handlers": ["offThread"]}},
            }

        finally:
            ...
            # if cfg:
            #     cfg["formatters"]["console"]["()"] = ColoredFormatter
            #     cfg["filters"]["ModuleFilter"]["()"] = LogFilter

    try:
        if cfg:
            dictConfig(cfg)

    except Exception as e:
        print("Error configuring logger:\n\t", e)

    lHandler: Handler | QueueHandler | None = getHandlerByName("offThread")

    if isinstance(lHandler, QueueHandler):
        lHandler.listener.start()
        atexit.register(cleanup)
