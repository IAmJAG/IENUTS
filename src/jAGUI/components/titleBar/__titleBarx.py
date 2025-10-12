from jAGFx.property import Property
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QBoxLayout, QLabel, QSizePolicy, QWidget

from ..bases import ComponentBase
from ..utilities import processMarker

TITLE_BAR_HEIGHT: int = 35

@processMarker(True, True)
class TitleBar(ComponentBase):
    def __init__(self, name: str = '', parent: QWidget = None, *args, **kwargs): # type: ignore
        super().__init__(name, parent, *args, **kwargs)

    def Load(self):
        ...

    def setupUI(self, layout = None):
        super().setupUI(layout)
        self.Layout.setDirection(QBoxLayout.Direction.LeftToRight)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFixedHeight(TITLE_BAR_HEIGHT)

        self._label = QLabel()
        self._label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setObjectName("TITLE")

        self.Layout.addWidget(self._label)

    @Property # type: ignore
    def TextAlignment(self) -> Qt.AlignmentFlag:
        return self._label.alignment()

    @TextAlignment.setter
    def TextAlignment(self, value: Qt.AlignmentFlag):
        self._label.setAlignment(value)

    @Property # type: ignore
    def Parent(self) -> QWidget:
        return self.parent()

    @Parent.setter
    def Parent(self, value: QWidget):
        self.setParent(value)

    @Property # type: ignore
    def Height(self) -> int:
        return self.height()

    @Height.setter
    def Height(self, value: int):
        self.setFixedHeight(value)

    @Property # type: ignore
    def Text(self) -> str:
        return self._label.text()

    @Text.setter
    def Text(self, value: str):
        self._label.setText(value)
