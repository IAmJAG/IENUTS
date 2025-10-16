import re
from json import load
from os import path

from jAGFx.contracts.configuration import iConfiguration
from jAGFx.dependencyInjection import Provider
from jAGFx.logger import AddFilter, error
from PySide6.QtWidgets import QApplication

from eNuts.configuration import ENUTSConfig

DEFLOGGERCFGFILENAME = "logger.cfg"
QSSPATH: str = ".\\config\\style.qss"


def loadConfig():
    import atexit
    from logging import Handler, getHandlerByName
    from logging.config import dictConfig
    from logging.handlers import QueueHandler

    from jAGFx.types import eAnsiColors, eLogLevel

    cfg = None
    if path.exists("config/logger.cfg"):
        with open("config/logger.cfg") as f:
            cfg = load(fp=f)

    def cleanup():
        nonlocal lHandler
        if isinstance(lHandler, QueueHandler) and lHandler.listener is not None:
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
                        "class": "jAGFx.logger.ColoredFormatter",
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

    try:
        if cfg:
            dictConfig(cfg)

    except Exception as ex:
        raise Exception("Error configuring logger:\n\t") from ex

    lHandler: Handler | QueueHandler | None = getHandlerByName("offThread")

    if isinstance(lHandler, QueueHandler):
        if lHandler is None or lHandler.listener is None:
            raise Exception("Logger handler is already running. Please stop the logger before reconfiguring it.")

        lHandler.listener.start()
        atexit.register(cleanup)


cfg: ENUTSConfig = Provider.Resolve(iConfiguration)
lDefaultFilterLevel: str = cfg.Logger.DefaultLogLevel

for lModule, lFilters in cfg.Logger.Filters.items():
    AddFilter(lModule, lDefaultFilterLevel)
    for lKey, lLevel in lFilters.items():
        lNamespace = f"{lModule.strip()}{lKey.strip()}"
        AddFilter(lNamespace, lLevel)
