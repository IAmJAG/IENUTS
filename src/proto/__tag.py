# ==================================================================================
from typing import Protocol


class iTag(Protocol):
    @property
    def Code(self) -> int: ...

    @property
    def Text(self) -> str: ...

    @property
    def Description(self) -> str: ...

    @Description.setter
    def Description(self, value: str) -> None: ...
