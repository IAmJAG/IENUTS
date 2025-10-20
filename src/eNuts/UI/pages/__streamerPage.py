from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from jAGFx.utilities.names import getRandomNames
from jAGUI.components import CommandBar
from jAGUI.types import eCommandPosition

from ...services import AndroidStreamer
from ..mwHelper import *
from ..streamerClients import AndroidClient


def StreamerPage(title: str, streamer: AndroidClient, name: str = None, recorderFunction=None):
    name = getRandomNames if name.strip() == "" else name
    lPage, lContent = CreatePage(title)
    lPage.setObjectName(streamer.Streamer.Serial)

    if streamer is None:
        streamer = QLabel(f"Welcome to eNuts! Youre at {title} Page")
    streamer.setObjectName("WELCOMETEXT")
    streamer.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lContent.layout().addWidget(streamer, 1)

    if recorderFunction:
        lStrmr: AndroidStreamer = streamer.Streamer
        lDefLamda = lambda btn: print(lStrmr.Control.back_or_turn_screen_on())
        lCommandBar: CommandBar = CommandBar()
        lCommandBar.AddCommand("Record Video", recorderFunction(streamer), pos=eCommandPosition.LEFT)
        lCommandBar.AddCommand("Enable Object Detection", lDefLamda, pos=eCommandPosition.LEFT)
        lContent.layout().addWidget(lCommandBar)

    return lPage
