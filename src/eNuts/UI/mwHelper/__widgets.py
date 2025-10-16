from jAGFx.utilities.names import getRandomNames
from jAGUI.components import Button
from jAGUI.components.utilities import getIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QBoxLayout, QLabel, QWidget


def InitializeLayout(direction: QBoxLayout.Direction, parent: QWidget = None):
    lLayout: QBoxLayout = QBoxLayout(direction)
    lLayout.setContentsMargins(0, 0, 0, 0)
    lLayout.setSpacing(0)
    if parent is not None:
        parent.setLayout(lLayout)

    return lLayout


def CreateWidget(objectName: str = ""):
    objectName = getRandomNames() if objectName.strip() == "" else objectName
    lWid: QWidget = QWidget()
    lWid.setContentsMargins(0, 0, 0, 0)
    InitializeLayout(QBoxLayout.Direction.TopToBottom, lWid)
    lWid.setObjectName(objectName)

    return lWid


def CreatePage(title: str):
    lPage: QWidget = CreateWidget("PAGE")
    lContent: QWidget = CreateWidget("PAGECONTENT")

    lTitle: QLabel = QLabel(title)
    lTitle.setObjectName("PAGETITLE")
    lTitle.setFixedHeight(35)
    lTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

    lPage.layout().addWidget(lTitle)
    lPage.layout().addWidget(lContent)

    return lPage, lContent
