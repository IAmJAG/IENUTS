
# ==================================================================================
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QBoxLayout, QWidget

# ==================================================================================
from dataobjects import BoundingBox

# ==================================================================================
from jAGFx.property import TSProperty

# ==================================================================================
from jAGUI.components import ComponentBase
from jAGUI.components.utilities import processMarker

# ==================================================================================
from ....contracts import iVideoThread
from .__playbackControl import PlaybackControls
from .__videoStream import VideoStream


@processMarker(True, True)
class PlaybackView(ComponentBase):
    OnListItemSelected: Signal = Signal(str)  # bboxId
    OnItemUpdate: Signal = Signal(int, BoundingBox)  # frameIndex, bbox

    def __init__(self, vt: iVideoThread, parent: QWidget = None, *args, **kwargs):
        super().__init__("", parent, *args, **kwargs)

        self._videoThread: iVideoThread = vt
        self._currentFrameIndex: int = -1

    def setupUI(self, layout: QBoxLayout = None):
        super().setupUI(layout)
        self.Layout.setDirection(QBoxLayout.Direction.TopToBottom)

        lMediaView: VideoStream = VideoStream(self.VideoThread)
        lPlayCntrl: PlaybackControls = PlaybackControls(self.VideoThread)

        self.Layout.addWidget(lMediaView)
        self.Layout.addWidget(lPlayCntrl)

    @TSProperty
    def ShowBoundingBox(self) -> bool:
        return self._showBoundingBox

    @ShowBoundingBox.setter
    def ShowBoundingBox(self, value: bool):
        self._showBoundingBox = value

    @TSProperty
    def VideoThread(self) -> iVideoThread:
        return self._videoThread
