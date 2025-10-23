# ------------------------------------------------------
from inspect import currentframe
from typing import Any

# ------------------------------------------------------
from jAGFx.exceptions import jAGException


class InvalidDatatypeException(jAGException):
    def __init__(
        self,
        expected: type,
        provided: type,
        message: str | None = None,
        inner: Exception | None = None,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> None:
        lBaseMessage = f"Invalid data type, expecting {expected.__name__} got {provided.__name__}!"
        lFinalMessage = lBaseMessage
        if message:
            lFinalMessage = [lBaseMessage, message]

        super().__init__(lFinalMessage, *args, inner=inner, frame=currentframe().f_back, **kwargs)
