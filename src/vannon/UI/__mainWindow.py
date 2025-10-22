# ==================================================================================
from time import sleep

# ==================================================================================
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QBoxLayout

# ==================================================================================
from jAGUI.components.forms import ModernWindow
from jAGUI.components.utilities import processMarker
from utilities.mwHelper import InitializeLayout

# ==================================================================================
from ..videoThread import VideoThread
from .components import VideoStream


@processMarker(True, True)
class MainWindow(ModernWindow):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    def setupUI(self) -> None:
        super().setupUI()
        lLayout: QBoxLayout = InitializeLayout(QBoxLayout.Direction.TopToBottom)

        self.Layout.addLayout(lLayout)
        self._layout: QBoxLayout = lLayout

        lVT: VideoThread = VideoThread()
        lVS: VideoStream = VideoStream(lVT)

        self.Layout.addWidget(lVS)
        # self.Layout.addStretch()

        lVT.OnMediaLoaded.connect(lambda mi: lVT.play())
        lVT.setVideoFile("D:\\Training\\Data\\video\\buying_hp_postion.mp4")

        def _cleanUp():
            nonlocal lVT
            lVT.Stop()
            lVT = None

        self.CleanUp = _cleanUp
