# ------------------------------------------------------
from inspect import currentframe
from typing import Any

# ------------------------------------------------------
from jAGFx.exceptions import jAGException


class InvalidFileException(jAGException):
    def __init__(
        self,
        message: str | None = None,
        inner: Exception | None = None,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> None:
        lBaseMessage = "Video file not supported"
        lFinalMessage = lBaseMessage
        if message:
            lFinalMessage = [lBaseMessage, message]

        super().__init__(lFinalMessage, *args, inner=inner, frame=currentframe().f_back, **kwargs)
