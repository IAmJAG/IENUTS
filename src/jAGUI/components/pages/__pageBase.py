from typing import override

from jAGFx.overload import OverloadDispatcher
from jAGFx.property import Property
from PySide6.QtWidgets import QBoxLayout, QLabel, QLayout, QSizePolicy, QWidget

from ..bases import ContainerBase
from ..titleBar import TitleBar
from ..utilities import processMarker


@processMarker(True, True)
class PageBase(ContainerBase):
    def __init__(self, title: str, name: str = "", parent: QWidget = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)
        self._title = title

    def Load(self):
        del self._title

    @override
    def setupUI(self, layout: QBoxLayout = None):
        super().setupUI(layout)
        self.layout().setDirection(QBoxLayout.Direction.TopToBottom)
        self.layout().setContentsMargins(1, 0, 1, 0)

        self._titleBar: QLabel = QLabel(self._title, parent=self)
        self._titleBar.setFixedHeight(30)

        self._content: ContainerBase = ContainerBase()
        self._content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._content.setParent(self)
        self._content.setObjectName("PAGECONTENT")

        self.layout().addWidget(self._titleBar)
        self.layout().addWidget(self._content)

    # region [PROPERTIES]
    @Property
    def Title(self) -> str:
        return self._titleBar.Text

    @Title.setter
    def Title(self, value: str):
        self._titleBar.Text = value

    # endregion

    @Property
    def Layout(self) -> QBoxLayout:
        return self._content.layout()

    @OverloadDispatcher
    def AddComponent(self, comp: QWidget):
        layout: QBoxLayout = self.Layout
        super().AddComponent(comp, layout)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, index: int):
        layout: QBoxLayout = self.Layout
        super().AddComponent(comp, layout, index)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layout: QLayout):
        super().AddComponent(comp, layout, -1)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layout: QLayout, index: int):
        super().AddComponent(comp, layout, index)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layoutName: str, index: int):
        super().AddComponent(comp, layoutName, index)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layoutName: str):
        super().AddComponent(comp, layoutName, -1)
