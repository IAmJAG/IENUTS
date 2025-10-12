from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QPainter, QPalette, QPen
from PySide6.QtWidgets import QBoxLayout, QStyleOption, QWidget

from ..bases import ComponentBase
from ..utilities import processMarker

RESIZE_GRIP_SIZE = 10

@processMarker(True, True)
class ResizeGrip(ComponentBase):
    def __init__(self, name: str = '', parent: QWidget = None, *args, **kwargs): #type: ignore
        super().__init__(name, parent, *args, **kwargs)

        # Resizing state specific to this grip
        self._isResizing = False
        self._resizeStartPos = None
        self._resizeStartGeo = None

    def Load(self):
        super().Load()
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.SizeFDiagCursor)

    def setupUI(self, layout = None):
        super().setupUI(layout)
        self.Layout.setDirection(QBoxLayout.Direction.LeftToRight)
        self.setFixedSize(RESIZE_GRIP_SIZE, RESIZE_GRIP_SIZE)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._isResizing = True
            self._resizeStartPos = event.globalPosition().toPoint()
            self._resizeStartGeo = self.MainWindow.geometry()
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._isResizing and event.buttons() & Qt.MouseButton.LeftButton:
            lDelta = event.globalPosition().toPoint() - self._resizeStartPos # type: ignore[reportGeneralTypeIssues]
            lNewWidth = self._resizeStartGeo.width() + lDelta.x() # type: ignore
            lNewHieght = self._resizeStartGeo.height() + lDelta.y() # type: ignore

            # Enforce minimum size of the main window
            lNewWidth = max(lNewWidth, self.MainWindow.minimumWidth())
            lNewHieght = max(lNewHieght, self.MainWindow.minimumHeight())

            self.MainWindow.resize(lNewWidth, lNewHieght)
            event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self._isResizing:
            self._isResizing = False
            self._resizeStartPos = None
            self._resizeStartGeo = None
            event.accept()
        else:
            event.ignore()

    def paintEvent(self, event):
        lPainter = QPainter(self)
        lPainter.setRenderHint(QPainter.RenderHint.Antialiasing)

        lOption = QStyleOption()
        lOption.initFrom(self)

        lEffectiveFC = lOption.palette.color(QPalette.ColorRole.ButtonText) #type: ignore
        lPen = QPen(lEffectiveFC, 1)
        lPen.setCosmetic(True)
        lPainter.setPen(lPen)

        # Draw lines from bottom-left to top-right
        lPainter.drawLine(self.width(), 0, 0, self.height())
        lPainter.drawLine(self.width(), 5, 5, self.height())
        lPainter.drawLine(self.width(), 10, 10, self.height())
