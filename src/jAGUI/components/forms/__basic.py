from jAGUI.components.utilities import processMarker

from .base import FormBase


@processMarker(True, True)
class FormBasic(FormBase):
    def __init__(self, frameless: bool = False):
        super().__init__(frameless)

    def setupUI(self) -> None:
        super().setupUI()
