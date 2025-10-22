# ==================================================================================
import inspect

# ==================================================================================
from PySide6.QtCore import QCoreApplication, QRectF, QThread, Signal
from PySide6.QtGui import QColor, QMouseEvent, QPen, Qt, QTransform
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView

# ==================================================================================
from jAGFx.property import TSProperty


class GraphicsView(QGraphicsView):
    OnBoxCreated: Signal = Signal(QRectF)
    Invoke: Signal = Signal(str, object, object)

    def __init__(self, parent=None):
        lScene: QGraphicsScene = QGraphicsScene(parent)
        lCanvas: QGraphicsPixmapItem = QGraphicsPixmapItem()

        lScene.addItem(lCanvas)
        super().__init__(scene=lScene, parent=parent)

        self._canvas = lCanvas
        self._isDrawing: bool = False

        self._drawingPen: QPen = QPen(Qt.GlobalColor.green, 3, Qt.PenStyle.DotLine)

        def _invoke(methodName: str, args, kwargs):
                method = getattr(self, methodName)
                if callable(method):
                    return method(*args, **kwargs)

                raise TypeError(f"{methodName} is not callable.")

        self.Invoke.connect(_invoke)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() != Qt.MouseButton.LeftButton or not self.DrawingEnabled:
            super().mousePressEvent(event)
            return

        lScenePos = self.mapToScene(event.position().toPoint())
        lItem = self.scene().itemAt(lScenePos, QTransform())
        self._isDrawing = lItem is self.Canvas

        if self._isDrawing:
            self._tempRectItem = QGraphicsRectItem(lScenePos.x(), lScenePos.y(), 0, 0)
            self._tempRectItem.setPen(self._drawingPen)
            self._startPoint = lScenePos
            self.scene().addItem(self._tempRectItem)

            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._isDrawing:
            lStartPoint = self._startPoint
            lEndPoint = self.mapToScene(event.pos())
            lRect = QRectF(lStartPoint, lEndPoint).normalized()
            self._tempRectItem.setRect(lRect)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._isDrawing and event.button() == Qt.MouseButton.LeftButton:
            lFinalRect: QRectF = self._tempRectItem.rect().normalized()
            self.scene().removeItem(self._tempRectItem)
            self._isDrawing = False

            if lFinalRect.width() > 5 and lFinalRect.height() > 5:
                self.OnBoxCreated.emit(lFinalRect)

            event.accept()
        else:
            super().mouseReleaseEvent(event)

    # region [PROPERTIES]
    @TSProperty
    def Canvas(self) -> QGraphicsPixmapItem:
        return self._canvas

    @TSProperty
    def DrawingEnabled(self) -> bool:
        return self.hasMouseTracking()

    @DrawingEnabled.setter
    def DrawingEnabled(self, enable: bool):
        self.setMouseTracking(enable)

    # endregion

    def setDrawingPen(self, color: QColor, lineWidth: int = 2, style: Qt.PenStyle = Qt.PenStyle.DotLine):
        self._drawingPen = QPen(color, lineWidth, style)

    @property
    def InvokeRequired(self) -> bool:
        return QThread.currentThread() != QCoreApplication.instance().thread()

    def invoke(self, *args, **kwargs):
        frame = inspect.currentframe()
        caller_frame = frame.f_back if frame else None
        method_name = caller_frame.f_code.co_name if caller_frame else None

        if not method_name or not hasattr(self, method_name):
            raise AttributeError("No current method set or method does not exist.")

        self.Invoke.emit(method_name, args, kwargs)
