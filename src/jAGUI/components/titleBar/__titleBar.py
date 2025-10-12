# src/eNuts/UI/__titleBar.py
import os
import re

# ------------------------------------------------------
from PySide6.QtCore import QEvent, QSize, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QBoxLayout,
    QFrame,
    QLabel,
    QMenu,
    QSizePolicy,
    QWidget,
)

from jAGFx.configuration import ApplicationConfiguration, iConfiguration
from jAGFx.dependencyInjection import Provider
from jAGFx.logger import debug, error
from jAGFx.utilities.io import getICONPath, getStylePath
from jAGFx.utilities.stack import getMethodName

# ------------------------------------------------------
from ...components.bases import Component
from ...components.buttons import Button
from ...components.utilities import processMarker
from ...exception import CouldNotSetIconExpception
from ...utilities import SaveCFG
from ..utilities.constants import *

TITLEBAR_HEIGHT: int = 40

CONTROLBOX_DIR: str = "controlbox"
CLOSE_ICON_FILENAME: str = "close.png"
MINIM_ICON_FILENAME: str = "minimize.png"
MAXIM_ICON_FILENAME: str = "maximize.png"
RESTO_ICON_FILENAME: str = "restore.png"
THEME_ICON_FILENAME: str = "aesthetic.png"

QSSVARREGEX = r"--(\w+):\s*([^;]+);"  # variable regex (--<*>)
QSSLHREGEX = r"--\w+:\s*[^;]+;"  # placehorder regex (@<*>)


@processMarker(True, True)
class TitleBar(Component, QFrame):
    OBJECT_NAME = "TITLEBAR"

    def __init__(self, parent: QWidget, *args, **kwargs):
        super().__init__(self.OBJECT_NAME, parent, *args, **kwargs)
        self._iconsize: QSize = ICON_SIZE
        self._startPos = None

    def setupUI(self, layout: QBoxLayout | None = None):
        super().setupUI(layout)
        self.ContentMargins = [0, 3, 0, 2]
        try:
            cfg: ApplicationConfiguration = Provider.Resolve(iConfiguration)
            self.Layout.setDirection(QBoxLayout.Direction.LeftToRight)
            self.setFixedHeight(TITLEBAR_HEIGHT)
            lAppIcon: QLabel = QLabel(self)
            lAppIcon.setContentsMargins(5, 0, 5, 0)
            lAppIcon.setPixmap(self.MainWindow.windowIcon().pixmap(ICON_SIZE))

            lTitle: QLabel = QLabel(cfg.Title)
            lTitle.setMouseTracking(True)

            lControlBox: QWidget = QWidget()
            lControlBox.setContentsMargins(0, 0, 5, 0)
            lControlBox.setObjectName("CONTROLBOX")

            lCBLayout: QBoxLayout = QBoxLayout(
                QBoxLayout.Direction.LeftToRight, parent=lControlBox
            )
            lCBLayout.setContentsMargins(0, 0, 0, 0)
            lCBLayout.setSpacing(0)

            lITheme: Button = self._createButton(THEME_ICON_FILENAME)
            lIMinim: Button = self._createButton(MINIM_ICON_FILENAME)
            lIMaxim: Button = self._createButton(MAXIM_ICON_FILENAME)
            lIClose: Button = self._createButton(CLOSE_ICON_FILENAME)
            lIMinim.OnClicked.connect(self.MainWindow.showMinimized)
            lIMaxim.OnClicked.connect(self.ToggleMaximizeRestore)
            lIClose.OnClicked.connect(self.MainWindow.close)
            lITheme.OnClicked.connect(self._showThemeMenu)

            lCBLayout.addWidget(lITheme)
            lCBLayout.addWidget(lIMinim)
            lCBLayout.addWidget(lIMaxim)
            lCBLayout.addWidget(lIClose)

            self.Layout.addWidget(lAppIcon)
            self.Layout.addWidget(lTitle)
            self.Layout.addStretch()
            self.Layout.addWidget(lControlBox)

            self._appIcon: QLabel = lAppIcon

        except Exception as ex:
            raise Exception(f"Error occur in {self.FQN}.{getMethodName()}") from ex

    def ToggleMaximizeRestore(self, btn: Button):
        if self.MainWindow.isMaximized():
            self.MainWindow.showNormal()
            btn.setIcon(
                QIcon(getICONPath(os.path.join(CONTROLBOX_DIR, MAXIM_ICON_FILENAME)))
            )
        else:
            self.MainWindow.showMaximized()
            btn.setIcon(
                QIcon(getICONPath(os.path.join(CONTROLBOX_DIR, RESTO_ICON_FILENAME)))
            )

    def _createButton(self, icofilename: str):
        lICON: QIcon = QIcon(getICONPath(os.path.join(CONTROLBOX_DIR, icofilename)))
        if lICON.isNull():
            lICON = self.MainWindow.windowIcon()
            if lICON.isNull():
                error(
                    "Unable to set icon",
                    CouldNotSetIconExpception("Unable to set close button image."),
                )

        lBtn: Button = Button("", lICON)
        lBtn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        lBtn.setIconSize(QSize(self.height(), self.height()) - QSize(10, 10))
        lBtn.setMaximumWidth(self.height() - 5)
        return lBtn

    @property
    def IconSize(self) -> QSize:
        return self._iconsize

    @IconSize.setter
    def IconSize(self, value: QSize):
        self._iconsize = value
        self._appIcon.setPixmap(self.MainWindow.windowIcon().pixmap(value))

    def _applyQSS(self, styleName: str):
        def _preProcQSS(_qss: str):
            lVariables: dict = {}
            for match in re.finditer(QSSVARREGEX, _qss):
                lVariables[match.group(1)] = match.group(2).strip()

            _qss = re.sub(QSSLHREGEX, "", _qss)

            for lName, lValue in lVariables.items():
                _qss = _qss.replace(f"@{lName}", lValue)

            return _qss.strip()

        with open(f"{getStylePath(f'{styleName}.qss')}") as file:
            lQSS = file.read()

        try:
            lProccessedQSS = _preProcQSS(lQSS)
            QApplication.instance().setStyleSheet(lProccessedQSS)
            debug(f"applied styles from {styleName}.qss")

        except Exception as e:
            error("Error loading QSS", e)
    def _showThemeMenu(self, btn: Button):
        lMenu: QMenu = QMenu(self)
        lStylePath: str = getStylePath()
        try:
            lFiles: list = os.listdir(lStylePath)
            lQssFiles: list = [f for f in lFiles if f.endswith('.qss')]
            for lFile in lQssFiles:
                lStyleName: str = lFile[:-4]  # remove .qss
                lAction: QAction = QAction(lStyleName, self)
                lAction.triggered.connect(lambda checked=False, name=lStyleName: self._applyTheme(name))
                lMenu.addAction(lAction)
            lMenu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))
        except Exception as ex:
            error("Error showing theme menu", ex)
    def _applyTheme(self, styleName: str):
        cfg: ApplicationConfiguration = Provider.Resolve(iConfiguration)
        cfg._style = styleName
        SaveCFG()
        self._applyQSS(styleName)


    def mousePressEvent(self, lEvent):
        if (
            lEvent.button() == Qt.MouseButton.LeftButton
            and not self.MainWindow.isMaximized()
        ):
            self._startPos = lEvent.globalPosition().toPoint()
            self._originalPos = self.MainWindow.pos()
        else:
            if (
                lEvent.button() == Qt.MouseButton.LeftButton
                and lEvent.type() == QEvent.Type.MouseButtonDblClick
            ):
                self.ToggleMaximizeRestore()
            else:
                super().mousePressEvent(lEvent)

    def mouseMoveEvent(self, lEvent):
        if (
            lEvent.buttons() == Qt.MouseButton.LeftButton
            and self._startPos
            and not self.MainWindow.isMaximized()
        ):
            lDelta = lEvent.globalPosition().toPoint() - self._startPos
            lNewPos = self._originalPos + lDelta
            self.MainWindow.move(lNewPos)
        else:
            super().mouseMoveEvent(lEvent)

    def mouseReleaseEvent(self, lEvent):
        self._startPos = None
        super().mouseReleaseEvent(lEvent)  # Pass to base class
