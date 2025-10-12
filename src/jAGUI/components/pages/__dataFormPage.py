from logging import INFO
from typing import Callable, override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QBoxLayout, QWidget, QPushButton, QScrollArea

from ..bases import ContainerBase
from ..commandBar import CommandBar
from ..logger import logViewer
from ..titleBar import TitleBar
from ..utilities import processMarker
from .__pageBase import PageBase


@processMarker(True, True)
class dataFormPage(PageBase):
    def __init__(
        self,
        title: str,
        subTitle: str,
        name: str = '',
        parent: QWidget = None,
        *args, **kwargs
    ):
        super().__init__(title=title, name=name, parent=parent, *args, **kwargs)
        self._subtitle = subTitle

    def Load(self):
        del self._subtitle

    @override
    def setupUI(self, layout: QBoxLayout = None):
        super().setupUI(layout)

        self._subTitle: TitleBar = TitleBar()
        self._subTitle.Text = self._subtitle
        self._subTitle.TextAlignment = Qt.AlignmentFlag.AlignVCenter
        self._subTitle.setObjectName("EXTRACTINGTITLE")

        self._subformcontent: ContainerBase = ContainerBase()

        self._commandbar: CommandBar = CommandBar()
        self._commandbar.setFixedHeight(45)
        self._logviewer: logViewer = logViewer()

        self._ncontent: ContainerBase = ContainerBase()
        self._scrollArea: QScrollArea = QScrollArea()
        self._scrollArea.setWidgetResizable(True)
        self._scrollArea.setWidget(self._ncontent)

        self.AddComponent(self._subTitle)
        self.AddComponent(self._scrollArea)
        self.AddComponent(self._commandbar)
        self.AddComponent(self._logviewer)

    def Status(self, text: str, logLevel = INFO):
        self._logviewer.Status(text, logLevel)

    def AddCommand(self, text: str, cb: Callable[[QPushButton], None], name: str = ''):
        self._commandbar.AddCommand(text, cb, name)

    @property
    def Content(self) -> ContainerBase:
        return self._ncontent

    @Content.setter
    def Content(self, value: ContainerBase):
        self._ncontent = value
        self._scrollArea.setWidget(self._ncontent)

    @property
    def Buttons(self) -> dict[str, QPushButton]:
        return self._commandbar.Buttons

    @property
    def SubTitle(self) -> str:
        return self._subTitle.Text

    @SubTitle.setter
    def SubTitle(self, value: str):
        self._subTitle.Text = value
