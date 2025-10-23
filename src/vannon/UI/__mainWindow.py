# ==================================================================================

# ==================================================================================
from PySide6.QtWidgets import QBoxLayout

# ==================================================================================
from jAGUI.components.forms import ModernWindow
from jAGUI.components.utilities import processMarker
from utilities.mwHelper import InitializeLayout

# ==================================================================================
from ..videoThread import VideoThread
from .components import PlaybackView


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
        lPV: PlaybackView = PlaybackView(lVT)

        self.Layout.addWidget(lPV)
        # self.Layout.addStretch()

        def _cleanUp():
            nonlocal lVT
            lVT.Stop()
            lVT = None

        self.CleanUp = _cleanUp
