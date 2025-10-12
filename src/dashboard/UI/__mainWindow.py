# ==================================================================================
import subprocess
import sys

# ==================================================================================
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

# ==================================================================================
from jAGFx.configuration import iConfiguration
from jAGFx.dependencyInjection import Provider
from jAGFx.logger import debug
from jAGFx.utilities.io import getICONPath
from jAGUI.components.cards import cardBase
from jAGUI.components.forms import ModernWindow
from jAGUI.components.layouts import FlowLayout
from jAGUI.components.utilities import processMarker

# ==================================================================================
from ..configuration import DashboardConfiguration


@processMarker(True, True)
class MainWindow(ModernWindow):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    def setupUI(self) -> None:
        super().setupUI()
        lLayout: FlowLayout = FlowLayout()
        lLayout.setExpandingDirections(Qt.Orientation.Vertical)

        self.Layout.addLayout(lLayout)
        self._layout: FlowLayout = lLayout

        lNewCard: cardBase = cardBase("Video Annotator", getICONPath("logo"))
        lNewCard.clicked.connect(lambda: self._launchApp("vannon"))
        self.Layout.addWidget(lNewCard)


        self.Layout.setSpacing(3)
        self.Layout.setContentsMargins(5, 5, 5, 5)
        lLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lOldCloseEvent = self.closeEvent
        def _newCloseEvent(event: QCloseEvent):
            lOldCloseEvent(event)
        self.closeEvent = _newCloseEvent

        self._setupTrayIcon()

    def _launchApp(self, appName):
        lCmd = [sys.executable, sys.argv[0], "--launch", appName]

        try:
            subprocess.Popen(lCmd)

        except OSError as e:
            debug(f"Error launching application as separate process: {e}")
            return

    def _setupTrayIcon(self):
        cfg: DashboardConfiguration = Provider.Resolve(iConfiguration)

        self._trayIcon: QSystemTrayIcon = QSystemTrayIcon(QIcon(getICONPath(cfg.Icon)), self)
        self._trayIcon.setToolTip(cfg.Title)

        lMenu = QMenu()
        lShowAction = lMenu.addAction("Show Dashboard")
        lShowAction.triggered.connect(self.showNormal)
        lExitAction = lMenu.addAction("Exit")
        lExitAction.triggered.connect(QApplication.instance().quit)
        self._trayIcon.setContextMenu(lMenu)
        self._trayIcon.show()
