# ==================================================================================
from PySide6.QtWidgets import QBoxLayout

# ==================================================================================
from utilities.mwHelper import InitializeLayout

# ==================================================================================
from ..statusBar import StatusBar
from ..titleBar import TitleBar
from ..utilities import processMarker
from .__basic import FormBasic


@processMarker(True, True)
class ModernWindow(FormBasic):
    def __init__(self, *args):
        super().__init__(True)

    def Load(self):
        super().Load()

    def setupUI(self) -> None:
        super().setupUI()
        lTitleBar: TitleBar = TitleBar(self)
        lStatusBar = StatusBar()

        lContentLayout: QBoxLayout = InitializeLayout(QBoxLayout.Direction.TopToBottom)

        self.AddComponent(lTitleBar, 0)
        self.Layout.addLayout(lContentLayout, 1)
        self.AddComponent(lStatusBar, 0)

        self._layout = lContentLayout
