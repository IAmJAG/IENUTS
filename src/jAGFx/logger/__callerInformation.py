from inspect import currentframe
from types import FrameType

from .__utilities import SKIPMODULES, GetCallerInfoFromFrame


class CallerInformation:
    def __init__(self, frame: FrameType | None = None):
        lModuleName, lClassName, lMemberName = "", "", ""

        if frame is None:
            frame = currentframe()
            frame = frame.f_back if frame is not None else frame

        if frame is not None:
            lModuleName, lClassName, lMemberName = GetCallerInfoFromFrame(frame)
            while (
                frame is not None
                and lModuleName != ""
                and lModuleName.startswith(SKIPMODULES)
            ):
                frame = frame.f_back
                if frame:
                    lModuleName, lClassName, lMemberName = GetCallerInfoFromFrame(frame)

        self._module: str = lModuleName
        self._class: str = lClassName
        self._member: str = lMemberName

    @property
    def Module(self) -> str:
        return self._module.strip() if self._module else ""

    @property
    def Class(self) -> str:
        return self._class.strip() if self._class else ""

    @property
    def Member(self) -> str:
        return self._member.strip() if self._member else ""

    @property
    def __repr__(self):
        return f"CallerInformation:\
            {self._module}\
            {'' if self._class is None or self._class == '' else f'.{self._class}'}\
            {'' if self._member is None or self._member == '' else f'.{self._member}'}"

    def __str__(self):
        return f"{self.Module}{'' if self.Class == '' else f'.{self.Class}'}{'' if self.Member == '' else f'.{self.Member}'}"
