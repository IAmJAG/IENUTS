from PySide6.QtWidgets import QBoxLayout, QWidget

from ..bases import ContainerBase
from ..utilities import processMarker

HEADER_HEIGHT = 50


@processMarker(True, True)
class Central(ContainerBase):
    OBJECT_NAME = "CENTRAL"

    def __init__(self, name: str = "", parent: QWidget = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)

    def setupUI(self, layout: QBoxLayout = None):
        super().setupUI(layout)
        self.setObjectName(self.OBJECT_NAME)
        self.setMouseTracking(True)
        self.Layout.setObjectName(f"{self.FQN}-BASELAYOUT")
