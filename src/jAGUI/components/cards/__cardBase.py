# ==================================================================================
from typing import override

# ==================================================================================
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent, QPixmap
from PySide6.QtWidgets import QBoxLayout, QLabel, QSizePolicy, QWidget

# ==================================================================================
from jAGFx.property import Property

# ==================================================================================
from ..bases import ComponentBase
from ..utilities import processMarker


@processMarker(True, True)
class cardBase(ComponentBase):
    clicked: Signal = Signal()

    def __init__(self, title: str, iconPath: str, name: str = "", parent: QWidget = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)
        self._title: QLabel = title
        self._iconPath: str = iconPath

    @override
    def setupUI(self, layout: QBoxLayout = None):
        super().setupUI(layout)
        self.Layout.setDirection(QBoxLayout.Direction.TopToBottom)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumWidth(160)
        self.setMinimumHeight(160 + 60)

        lPixmap: QPixmap = QPixmap(self._iconPath)
        lPixmap = lPixmap.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self._title: QLabel = QLabel(self._title, alignment=Qt.AlignmentFlag.AlignCenter)
        self._title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._iconLabeL: QLabel = QLabel()
        self._iconLabeL.setPixmap(lPixmap)

        self.Layout.addWidget(self._iconLabeL)
        self.Layout.addWidget(self._title)

    # region [PROPERTIES]
    @Property
    def Title(self) -> str:
        return self._title.Text

    @Title.setter
    def Title(self, value: str):
        self._title.Text = value

    # endregion

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
