from inspect import currentframe
from typing import Any

from jAGFx.exceptions import jAGException


class IconNotFoundException(jAGException):
    def __init__(
        self,
        message: str = "",
        inner: Exception = None,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> None:
        message = "Could not find icon" if message.strip() == "" else message

        super().__init__(message, *args, inner=inner, frame=currentframe().f_back, **kwargs)


class CouldNotSetIconExpception(jAGException):
    def __init__(
        self,
        message: str = "",
        inner: Exception = None,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> None:
        message = "Icon could not be set" if message.strip() == "" else message
        super().__init__(message, *args, inner=inner, frame=currentframe().f_back, **kwargs)
