# ==================================================================================
from inspect import currentframe
from types import FrameType
from typing import Any

__all__ = ["jAGException"]


class jAGException(Exception):
    """Base exception class for jAGFx framework providing contextual error information."""

    __slots__ = ["_attribute", "_filename", "_inner", "_linenumber"]

    def __init__(
        self,
        message: str | list[str] | None = None,
        inner: Exception | None = None,
        frame: FrameType | None = None,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> None:
        lFrame: FrameType = currentframe().f_back if frame is None else frame

        self._filename: str = lFrame.f_code.co_filename
        self._attribute: str = lFrame.f_code.co_name
        self._linenumber: int = lFrame.f_lineno

        lCMsg: str = f"Unexpected error occur in {self._filename}: {self._attribute}, line {self._linenumber}"

        if message is None:
            lMessage = lCMsg

        else:
            if isinstance(message, list):
                lMessage = [lCMsg] + message
            else:
                lMessage = [lCMsg, message]

        self._inner = inner
        super().__init__(lMessage, *args, **kwargs)

    @property
    def Message(self) -> str:
        return self.args[0]

    @property
    def Filename(self) -> str:
        return self._filename

    @property
    def Attribute(self) -> str:
        return self._attribute

    @property
    def LineNumber(self) -> int:
        return self._linenumber

    @property
    def InnerException(self) -> Exception | None:
        return self._inner

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(message={self.Message!r}, "
            f"filename={self.Filename!r}, attribute={self.Attribute!r}, "
            f"lineNumber={self.LineNumber}, inner={self.InnerException!r})"
        )
