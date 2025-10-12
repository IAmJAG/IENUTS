# ==================================================================================
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QBoxLayout

# ==================================================================================
from jAGUI.components.forms import ModernWindow
from jAGUI.components.utilities import processMarker

# ==================================================================================
from utilities.mwHelper import InitializeLayout


@processMarker(True, True)
class MainWindow(ModernWindow):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    def setupUI(self) -> None:
        super().setupUI()
        lLayout: QBoxLayout = InitializeLayout(QBoxLayout.Direction.TopToBottom)

        self.Layout.addLayout(lLayout)
        self._layout: QBoxLayout = lLayout

        self.Layout.addStretch()

        # region [CLOSE EVENT]
        lOldCloseEvent = self.closeEvent

        def _newCloseEvent(event: QCloseEvent):
            lOldCloseEvent(event)

        self.closeEvent = _newCloseEvent

        # endregion
