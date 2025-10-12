from jAGFx.utilities.names import getRandomNames
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QLabel, QPushButton, QWidget


def InitializeLayout(direction: QBoxLayout.Direction, parent: QWidget = None):
    lLayout: QBoxLayout = QBoxLayout(direction)
    lLayout.setContentsMargins(0, 0, 0, 0)
    lLayout.setSpacing(0)
    if parent is not None:
        parent.setLayout(lLayout)

    return lLayout


def CreateWidget(objectName: str = ""):
    objectName = getRandomNames() if objectName.strip() == "" else objectName
    lWidget: QWidget = QWidget()
    lWidget.setContentsMargins(0, 0, 0, 0)
    InitializeLayout(QBoxLayout.Direction.TopToBottom, lWidget)
    lWidget.setObjectName(objectName)

    return lWidget


def CreateButton(caption: str = "", iconPath: str = "", iconSize: int = 32) -> QPushButton:
    lButton: QPushButton = QPushButton(caption)
    lButton.setIcon(QIcon(iconPath))
    lButton.setIconSize(QSize(iconSize, iconSize))
    lButton.setFlat(True)
    return lButton


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
