from ..utilities import processMarker
from .__customTitleBar import CustomTitleBar

__all__ = ["FormWithSideNavigation"]


@processMarker(True, True)
class FormWithSideNavigation(CustomTitleBar):
    def __init__(self, navCaption: str = "jAG Side Nav"):
        super().__init__()
        self._caption: str = navCaption
