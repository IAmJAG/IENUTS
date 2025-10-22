from functools import wraps
from inspect import currentframe
from logging import CRITICAL, DEBUG, ERROR, FATAL, INFO, WARNING
from time import perf_counter

from ..overload import OverloadDispatcher
from .__log import log
from .__utilities import ExitOnError


# DEBUG
@OverloadDispatcher
def debug(message: str | tuple | list | dict, err: Exception):
    log(message=message, level=DEBUG, err=err, frame=currentframe())


@debug.overload
def debug(message: str | tuple | list | dict = ""):
    log(message=message, level=DEBUG, frame=currentframe())


# INFO
@OverloadDispatcher
def info(message: str | tuple | list | dict, err: Exception):
    log(message=message, level=INFO, err=err)


@info.overload
def info(message: str | tuple | list | dict):
    log(message=message, level=INFO, frame=currentframe())


# WARNING
@OverloadDispatcher
def warning(message: str | tuple | list | dict, err: Exception):
    log(message=message, level=WARNING, err=err, frame=currentframe().f_back)


@warning.overload
def warning(message: str | tuple | list | dict):
    log(message=message, level=WARNING, frame=currentframe())


# ERROR
@OverloadDispatcher
def error(message: str | tuple | list | dict):
    frame = currentframe()
    log(message=message, level=ERROR, frame=frame)


@error.overload
def error(message: str | tuple | list | dict, err: Exception):
    frame = currentframe()
    log(message=message, level=ERROR, err=err, frame=frame)
    if err:
        ExitOnError(err)

@error.overload
def error(message: str | tuple | list | dict, err: Exception, frame):
    log(message=message, level=ERROR, err=err, frame=frame)
    if err:
        ExitOnError(err)


# CRITICAL
@OverloadDispatcher
def critical(message: str | tuple | list | dict):
    log(message=message, level=CRITICAL, frame=currentframe())


@critical.overload
def critical(message: str | tuple | list | dict, err: Exception):  # type: ignore
    log(message=message, level=CRITICAL, err=err)

    if err:
        ExitOnError(err)


# FATAL
@OverloadDispatcher
def fatal(message: str | tuple | list | dict, err: Exception):  # type: ignore
    log(message=message, level=FATAL, err=err)
    if err:
        ExitOnError(err)


@fatal.overload
def fatal(message: str | tuple | list | dict):
    log(message=message, level=FATAL, frame=currentframe())


def benchmark(func):
    """
    A decorator that prints the time a function takes to execute.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        lStartTime = perf_counter()
        debug(f">>{func.__name__!r}")
        lReturn = func(*args, **kwargs)
        lEndTime = perf_counter()
        lRunTime = lEndTime - lStartTime
        debug(f"<<{func.__name__!r}: {lRunTime:.4f} secs")
        return lReturn

    return wrapper
