import os

from ..contracts.configuration import iConfiguration
from ..serializer import Serialisable

__all__ = ["Configuration"]


class Configuration(Serialisable, iConfiguration):
    def __init__(self):
        super().__init__()
        self._sections: dict[str, iConfiguration] = {}

        self._pid: int = os.getpid()

        self.Properties.append("Sections")

    @property  # type: ignore
    def Sections(self) -> set[str]:
        return self._sections

    # region [PICKLE READINESS]
    def __getstate__(self):
        lDicState = super().__getstate__()
        lInstanceState = {}
        return (lDicState, lInstanceState)

    def __setstate__(self, state):
        dict_state, instance_state = state
        self.__setstate__(dict_state)
        self.__dict__.update(instance_state)

    # endregion
