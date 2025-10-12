from PySide6.QtWidgets import QBoxLayout, QWidget

from jAGFx.overload import OverloadDispatcher

from ..statusBar import StatusBar
from ..titleBar import TitleBar
from ..utilities import processMarker
from .base import FormBase

__all__ = ["CustomTitleBar"]


@processMarker(True, True)
class CustomTitleBar(FormBase):
    def __init__(self):
        super().__init__()

    def Load(self): ...

    def setupUI(self) -> None:
        super().setupUI()

        lTitleBar: TitleBar = TitleBar()
        lTitleBar.Text = "e   N   u   t   s"
        lTitleBar.setObjectName("FORMTITLEBAR")

        lStatusBar = StatusBar()

        lBodyLayout: QBoxLayout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        lBodyLayout.setContentsMargins(0, 0, 0, 0)
        lBodyLayout.setSpacing(0)

        self.AddComponent(lTitleBar)
        self.Layout.addLayout(lBodyLayout)
        self.AddComponent(lStatusBar)
        self._layout = lBodyLayout

        self._tmpQW = QWidget(objectName="TEMPSTRETCH")
        self.AddComponent(self._tmpQW)

    @OverloadDispatcher
    def AddComponent(self, comp: QWidget):
        self.AddComponent(comp, self.Layout, -1)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layout: QBoxLayout):
        self.AddComponent(comp, layout, -1)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, index: int):
        self.AddComponent(comp, self.Layout, index)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layoutName: str, index: int):
        self.AddComponent(comp, layoutName, index)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layout: QBoxLayout, index: int):
        super().AddComponent(comp, layout, index)
        if len(layout.children()) > 1 and self._tmpQW is not None:
            self.RemoveComponent(self._tmpQW)
            self._tmpQW = None

    @OverloadDispatcher
    def RemoveComponent(self, comp: QWidget):
        super().RemoveComponent(comp)
        if len(self.Layout.children()) < 1 and self._tmpQW is None:
            self._tmpQW = QWidget(objectName="TEMPSTRETCH")
            self.AddComponent(self._tmpQW)

    @RemoveComponent.overload
    def RemoveComponent(self, objectName: str):
        return super().RemoveComponent(objectName)
