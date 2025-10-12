from inspect import currentframe
from typing import Any

from ..exceptions import jAGException


class invalidParentTypeError(jAGException):  # noqa: N801
    def __init__(
        self,
        message: str | None = None,
        inner: Exception | None = None,
        *args: list[Any],
        **kwargs: dict[str, Any]
    ) -> None:

        lBaseMessage = "Invalid parent type"
        lFinalMessage = lBaseMessage if message is None else [lBaseMessage, message]
        super().__init__(lFinalMessage, *args, inner=inner, frame=currentframe().f_back, **kwargs)
