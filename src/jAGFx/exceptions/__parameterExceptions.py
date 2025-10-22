# ==================================================================================
from inspect import currentframe
from typing import Any

# ==================================================================================
from .__exceptionBase import jAGException


class invalidParameterTypeException(jAGException):
    """Exception raised when a parameter has an incorrect type."""

    def __init__(
        self,
        expected: type,
        provided: type,
        message: str | None = None,
        inner: Exception | None = None,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> None:
        lBaseMessage = f"Invalid parameter type. Expecting {expected.__name__} got {provided.__name__}"
        lFinalMessage = lBaseMessage
        if message is not None:
            lFinalMessage = [lBaseMessage, message]

        super().__init__(
            lFinalMessage, *args, inner=inner, frame=currentframe().f_back, **kwargs
        )


class parameterRequiredException(jAGException):
    """Exception raised when a required parameter is missing or None."""

    def __init__(
        self,
        name: str,
        message: str | None = None,
        inner: Exception | None = None,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> None:
        lBaseMessage = f"Parameter required. Expecting {name} got None"
        lFinalMessage = lBaseMessage
        if message is not None:
            lFinalMessage = [lBaseMessage, message]

        super().__init__(
            lFinalMessage, *args, inner=inner, frame=currentframe().f_back, **kwargs
        )
