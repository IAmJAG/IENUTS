# ==================================================================================
from PySide6.QtCore import QObject, QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QCursor, QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent

# ==================================================================================
from dataobjects import BoundingBox

# ==================================================================================
from jAGFx.property import TSProperty


class GIBoundingBox(QGraphicsRectItem, QObject):
    RESIZE_HANDLE_SIZE = 8
    OnBoxChanged: Signal = Signal(QGraphicsRectItem)
    OnSelectedChanged: Signal = Signal(QGraphicsRectItem, bool)

    def __init__(self, bb: BoundingBox):
        QGraphicsRectItem.__init__(self, bb)
        QObject.__init__(self)
        self.setAcceptHoverEvents(True)

        self._id: str = bb.Id
        self._class: str = bb.Class
        self._defaultPen: QPen = QPen(Qt.GlobalColor.green, 2, Qt.PenStyle.SolidLine)
        self._selectedPen: QPen = QPen(Qt.GlobalColor.green, 2, Qt.PenStyle.DotLine)
        self.setPen(self._defaultPen)

        self._isMoving = False
        self._isResizing = False
        self._resizeHandle = None
        self._startPoint = QPointF()
        self._tempRect = QRectF()

        self._initRect: QRectF = self.rect()

    @TSProperty
    def Id(self) -> str:
        return self._id

    @TSProperty
    def Class(self) -> str:
        return self._class

    def _getResizeHandle(self, pos):
        lRect = self.rect()
        lHandleSize = self.RESIZE_HANDLE_SIZE

        lCorners: dict[Qt.Corner, QRectF] = {
            Qt.Corner.TopLeftCorner: QRectF(lRect.topLeft().x() - lHandleSize, lRect.topLeft().y() - lHandleSize, lHandleSize * 2, lHandleSize * 2),
            Qt.Corner.TopRightCorner: QRectF(lRect.topRight().x() - lHandleSize, lRect.topRight().y() - lHandleSize, lHandleSize * 2, lHandleSize * 2),
            Qt.Corner.BottomLeftCorner: QRectF(lRect.bottomLeft().x() - lHandleSize, lRect.bottomLeft().y() - lHandleSize, lHandleSize * 2, lHandleSize * 2),
            Qt.Corner.BottomRightCorner: QRectF(lRect.bottomRight().x() - lHandleSize, lRect.bottomRight().y() - lHandleSize, lHandleSize * 2, lHandleSize * 2)
        }
        for key, rect in lCorners.items():
            if rect.contains(pos): return key

        return None

    def hoverMoveEvent(self, event: QGraphicsSceneMouseEvent):
        lPos = event.pos()
        lHandle = self._getResizeHandle(lPos)
        if lHandle:
            if lHandle in [Qt.Corner.TopLeftCorner, Qt.Corner.BottomRightCorner]:
                self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))

            elif lHandle in [Qt.Corner.TopRightCorner, Qt.Corner.BottomLeftCorner]:
                self.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))

            else:
                self.setCursor(QCursor(Qt.CursorShape.SizeAllCursor))

        else:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        super().hoverMoveEvent(event)

    def hoverEnterEvent(self, event):
        self._isHovering = True
        lPen = self._defaultPen if not self.isSelected() else self._selectedPen
        self.setPen(lPen)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        lPen = self._defaultPen if not self.isSelected() else self._selectedPen
        self.setPen(lPen)
        self._isHovering = False
        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            if value and self.scene():
                # Clear selection of other BBGraphicsItem
                for item in self.scene().items():
                    if isinstance(item, GIBoundingBox) and item != self:
                        item.setSelected(False)

            self.setPen(self._selectedPen if value else self._defaultPen)
            self.OnSelectedChanged.emit(self, value)

        return super().itemChange(change, value)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self._initRect: QRectF = self.rect()

        if event.button() == Qt.MouseButton.LeftButton:
            lHandle = self._getResizeHandle(event.pos())
            if lHandle:
                self._isResizing = True
                self._resizeHandle = lHandle
                self._startPoint = event.scenePos()
                return

            # Check if we are starting to move the box
            if self.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
                self._isMoving = True
                self._startPoint = event.scenePos()
                self._tempRect = self.rect()
                event.accept()
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        lDelta = event.scenePos() - self._startPoint

        if self._isResizing:
            lRect = self.rect()

            if self._resizeHandle == Qt.Corner.TopLeftCorner:
                lRect.setTopLeft(lRect.topLeft() + lDelta)

            elif self._resizeHandle == Qt.Corner.TopRightCorner:
                lRect.setTopRight(lRect.topRight() + lDelta)

            elif self._resizeHandle == Qt.Corner.BottomLeftCorner:
                lRect.setBottomLeft(lRect.bottomLeft() + lDelta)

            elif self._resizeHandle == Qt.Corner.BottomRightCorner:
                lRect.setBottomRight(lRect.bottomRight() + lDelta)

            self.setRect(lRect.normalized())
            self._startPoint = event.scenePos()

        elif self._isMoving:
            self._tempRect.setRect(self._tempRect.x() + lDelta.x(), self._tempRect.y() + lDelta.y(), self._tempRect.width(), self._tempRect.height())
            self.setRect(self._tempRect)
            self._startPoint = event.scenePos()

        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if self._isResizing or self._isMoving:
            if self._initRect != self.rect():
                self.OnBoxChanged.emit(self)
            self.update()

        self._isResizing = False
        self._resizeHandle = None
        super().mouseReleaseEvent(event)
