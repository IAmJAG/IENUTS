from PySide6.QtCore import Qt

from ..types import eIconAlignment
from .__component import iComponent


class iPushButton(iComponent):
    @property
    def Text(self) -> str: ...

    @Text.setter
    def Text(self, value: str): ...

    @property
    def IconAlignment(self) -> eIconAlignment: ...

    @IconAlignment.setter
    def IconAlignment(self, value: eIconAlignment): ...

    @property
    def TextAlignment(self): ...

    @TextAlignment.setter
    def TextAlignment(self, val: Qt.AlignmentFlag): ...
