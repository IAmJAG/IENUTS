from jAGFx.utilities.names import getRandomNames
from jAGUI.components import Button
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from ..mwHelper import *


def PageBase(title: str, name: str = None):
    name = getRandomNames if name.strip() == "" else name
    lPage, lContent = CreatePage(title)
    lPage.setObjectName(name)

    lWelcomeLabel = QLabel(f"Welcome to eNuts! Youre at {title} Page")
    lWelcomeLabel.setObjectName("WELCOMETEXT")
    lWelcomeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lContent.layout().addWidget(lWelcomeLabel)
    return lPage
