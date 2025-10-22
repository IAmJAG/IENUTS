# ==================================================================================
from inspect import currentframe
from types import FrameType
from typing import Any

# ==================================================================================
from .__exceptionBase import jAGException


class ModuleException(jAGException):
    """Exception for module-level errors with fully qualified name (FQN) information."""

    __slots__ = ["_attribute", "_filename", "_inner", "_linenumber", "_fqn"]

    def __init__(
        self,
        message: str | list[str] | None = None,
        inner: Exception | None = None,
        frame: FrameType | None = None,
        module: str | None = None,
        klass: str | None = None,
        member: str | None = None,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> None:
        lFrame: FrameType = currentframe().f_back if frame is None else frame

        module = lFrame.f_globals.get("__name__", "<unknown>") if module is None else module
        klass = lFrame.f_locals.get("self").__class__.__name__ if "self" in lFrame.f_locals else "<unknown>" if klass is None else klass
        member = lFrame.f_code.co_name if member is None else member

        self._fqn = f"{module}.{'' if klass == '<unknown>' else klass}{member}"

        lCMsg: str = f"Unexpected error occurred from {module}.{klass}.{member}"

        if message is None:
            lMessage = lCMsg

        else:
            if isinstance(message, list):
                lMessage = [lCMsg] + message

            else:
                lMessage = [lCMsg, message]

        super().__init__(lMessage, inner, frame, *args, **kwargs)

    @property
    def FQN(self) -> str:
        return self._fqn


    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(message={self.Message!r}, "
            f"filename={self.Filename!r}, attribute={self.Attribute!r}, "
            f"lineNumber={self.LineNumber}, inner={self.InnerException!r})"
        )
