from json import load
from os import path

# ==================================================================================
from jAGFx.configuration import ApplicationConfiguration

# ==================================================================================
from jAGFx.contracts.configuration import iConfiguration
from jAGFx.dependencyInjection import Provider
from jAGFx.logger import AddFilter

DEFLOGGERCFGFILENAME = "logger.cfg"
QSSPATH: str = ".\\assets\\styles\\basic.qss"


def loadConfig(filename: str = "log"):
    import atexit
    from logging import Handler, getHandlerByName
    from logging.config import dictConfig
    from logging.handlers import QueueHandler

    from jAGFx.types import eAnsiColors, eLogLevel

    lCfg = None
    if path.exists(f"config/{DEFLOGGERCFGFILENAME}"):
        with open(f"config/{DEFLOGGERCFGFILENAME}") as lF:
            lCfg = load(fp=lF)

    def Cleanup():
        nonlocal nlHandler
        if isinstance(nlHandler, QueueHandler) and nlHandler.listener is not None:
            nlHandler.listener.stop()
            nlHandler = None

    if lCfg is None:
        try:
            with open(DEFLOGGERCFGFILENAME) as lF:
                lCfg = load(fp=lF)

        except (AttributeError, KeyError, FileNotFoundError):
            lCfg = {
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
                        "filename": "./LOGS/{filename}.log",
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
        if lCfg:
            if "handlers" in lCfg:
                if "file" in lCfg["handlers"]:
                    if "filenameTemplate" in lCfg["handlers"]["file"]:
                        lCfg["handlers"]["file"]["filenameTemplate"] = lCfg["handlers"]["file"]["filenameTemplate"].replace("{filename}", cfg.AppId)

                    if "filename" in lCfg["handlers"]["file"]:
                        lCfg["handlers"]["file"]["filename"] = lCfg["handlers"]["file"]["filename"].replace("{filename}", cfg.AppId)

            dictConfig(lCfg)

    except Exception as lEx:
        raise Exception("Error configuring logger:\n\t") from lEx

    nlHandler: Handler | QueueHandler | None = getHandlerByName("offThread")

    if isinstance(nlHandler, QueueHandler):
        if nlHandler is None or nlHandler.listener is None:
            raise Exception("Logger handler is already running. Please stop the logger before reconfiguring it.")

        nlHandler.listener.start()
        atexit.register(Cleanup)


cfg: ApplicationConfiguration = Provider.Resolve(iConfiguration)
lDefaultFilterLevel: str = cfg.Logger.DefaultLogLevel

for lModule, lFilters in cfg.Logger.Filters.items():
    AddFilter(lModule, lDefaultFilterLevel)
    for lKey, lLevel in lFilters.items():
        lNamespace = f"{lModule.strip()}{lKey.strip()}"
        AddFilter(lNamespace, lLevel)
