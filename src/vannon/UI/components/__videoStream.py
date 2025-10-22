# ==================================================================================
import cv2 as cv

# ==================================================================================
from numpy import ndarray

# ==================================================================================
from PySide6.QtCore import QEvent, QObject, QPointF, QRectF, Signal
from PySide6.QtGui import QCursor, QPen, QPixmap, Qt
from PySide6.QtWidgets import QBoxLayout, QGraphicsItem

# ==================================================================================
from dataobjects import BoundingBox
from jAGFx.logger import debug
from jAGFx.property import TSProperty
from jAGUI.components.utilities import processMarker
from utilities import NDArrayToPixmap, findContourRect

# ==================================================================================
from ...videoThread import VideoThread, ePlaybackState
from .__graphicsView import GraphicsView
from .graphicsItems import GIBoundingBox

AREA_TOLERANCE: int = 100
POSI_TOLERANCE: int = 10

@processMarker(True, True)
class VideoStream(GraphicsView):
    RESIZE_HANDLE_SIZE = 8

    # where int is the new index
    OnFrameIndexChanged: Signal = Signal(int)

    # frameIndex, box added
    OnItemAdded: Signal = Signal(int, object)
    OnItemUpdate: Signal = Signal(int, object)

    # frame index, bounding box id
    OnItemRemove: Signal = Signal(int, str)

    def __init__(self, vt: VideoThread, parent=None):
        super().__init__(parent)

        self._rawImage: cv.Mat = None  # current frame in ndarray format - used for snapping feature
        self._frameIndex: int = -1
        self._tmpVT: VideoThread = vt
        self._clipboard: list[QRectF] = list[QRectF]()

        self.installEventFilter(self)

    def Load(self):
        del self._tmpVT

    def _onFrame(self, frame: ndarray, frameIndex: int):
        if self.InvokeRequired:
            self.invoke(frame, frameIndex)
            return

        if frame is None or frame.size == 0:
            self._rawImage = None
            print("Frame not available")
            return

        if self.FrameIndex != frameIndex:
            self._rawImage = frame

            for gitem in self.scene().items():
                if gitem != self.Canvas:
                    self.scene().removeItem(gitem)

            self.FrameIndex = frameIndex

            lPixmap: QPixmap = self.ProcessImage(frame)
            self.Canvas.setPixmap(lPixmap)

            self.scene().setSceneRect(0, 0, lPixmap.width(), lPixmap.height())
            self.fitInView(self.scene().sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def setupUI(self, layout: QBoxLayout = None):

        def _onBoxCreated(rect: QRectF):
            if self.RawImage is None or self.RawImage.size == 0:
                debug("Frame not available, cannot add box")
                return

            return self.AddGraphicItem(rect)

        def _playbackChanged(state: ePlaybackState):
            self.DrawingEnabled = (state & ePlaybackState.PLAYING) != ePlaybackState.PLAYING

        self._tmpVT.OnFrame.connect(self._onFrame)
        self._tmpVT.OnPlaybackStateChanged.connect(_playbackChanged, blocking=False)
        self.OnBoxCreated.connect(_onBoxCreated)

    @TSProperty
    def FrameIndex(self) -> int:
        return self._frameIndex

    @FrameIndex.setter
    def FrameIndex(self, value: int):
        self._frameIndex = value
        self.OnFrameIndexChanged.emit(value)

    @TSProperty
    def RawImage(self) -> cv.Mat:
        return self._rawImage

    @TSProperty
    def Clipboard(self) -> list[QRectF]:
        return self._clipboard

    def ProcessImage(self, frame: ndarray):
        return NDArrayToPixmap(frame)

    def selectGraphicsItemById(self, bboxId: str):
        for item in self.scene().items():
            if isinstance(item, GIBoundingBox) and item.Id == bboxId:
                item.setSelected(True)
                break

    def AddGraphicItem(self, rect: QRectF):
        lBBox: BoundingBox = BoundingBox("object", findContourRect(self.RawImage, rect))

        def _onBoxChanged(_box: GIBoundingBox):
            lBox: BoundingBox = BoundingBox("object", _box.rect())
            lBox._id = _box.Id
            self.OnItemUpdate.emit(self.FrameIndex, lBox)

        lBBGI: GIBoundingBox = GIBoundingBox(lBBox)
        lBBGI.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        lBBGI.setPen(QPen(Qt.GlobalColor.green, 2, Qt.PenStyle.SolidLine))

        lBBGI.OnBoxChanged.connect(_onBoxChanged)

        self.scene().addItem(lBBGI)
        self.OnItemAdded.emit(self.FrameIndex, lBBox)
        return lBBox

    def eventFilter(self, source: QObject, event: QEvent):
        super().eventFilter(source, event)
        def _copySelectedBox():
            self._clipboard.clear()
            for lItem in self.scene().selectedItems():
                if isinstance(lItem, GIBoundingBox):
                    self._clipboard.append(lItem.rect())

        def _pasteClipboard():
            lMousePos = self.mapToScene(self.mapFromGlobal(QCursor.pos()))
            for lRect in self._clipboard:
                lNewRect: QRectF = QRectF(lMousePos.x(), lMousePos.y(), lRect.width(), lRect.height())
                self.OnBoxCreated.emit(BoundingBox("object", lNewRect))
                lMousePos = lMousePos + QPointF(5, 5)

        def _deleteSelectedBoxes():
            lSelectedItems = self.scene().selectedItems()
            if lSelectedItems:
                for lItem in lSelectedItems:
                    if isinstance(lItem, GIBoundingBox):
                        self.scene().removeItem(lItem)
                        lCIndex = self.FrameIndex
                        self.OnItemRemove.emit(lCIndex, lItem.Id)

        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Delete:
                _deleteSelectedBoxes()
                return True
            elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_C:
                _copySelectedBox()
                return True
            elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_V:
                _pasteClipboard()
                return True
        return super().eventFilter(source, event)
