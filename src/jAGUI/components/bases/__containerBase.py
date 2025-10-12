from jAGFx.exceptions import jAGException
from jAGFx.overload import OverloadDispatcher
from jAGFx.utilities import getRandomNames
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QBoxLayout, QLayout, QSizePolicy, QSpacerItem, QWidget

from ..utilities import findLayoutByName, processMarker
from .__componentBase import ComponentBase


@processMarker(True, True)
class ContainerBase(ComponentBase):
    def setupUI(self: ComponentBase, layout: QLayout = None):
        super().setupUI(layout)

    @OverloadDispatcher
    def AddStretch(self):
        self.Layout.addStretch()

    @AddStretch.overload
    def AddStretch(self, horizontal: QSizePolicy.Policy = QSizePolicy.Policy.Expanding, vertical: QSizePolicy.Policy = QSizePolicy.Policy.Expanding):
        lSpacer: QSpacerItem = QSpacerItem(0, 0, horizontal, vertical)
        self.Layout.addSpacerItem(lSpacer)

    def AddLayout(self, direction: QBoxLayout.Direction, name: str = "", parentLayoutName: str = ""):
        if name is None or name.strip() == "":
            name = f"{getRandomNames(7, False)}"

        lLayout = QBoxLayout(direction)
        lLayout.setObjectName(name)

        if parentLayoutName is None or parentLayoutName.strip() == "":
            lParentLayout = self.Layout

        else:
            lParentLayout = findLayoutByName(self.layout(), parentLayoutName)

        lParentLayout.addItem(lLayout)  # type: ignore
        return lLayout

    def GetLayout(self, name: str):
        return findLayoutByName(self.layout(), name)  # type: ignore

    @OverloadDispatcher
    def AddComponent(self, comp: QWidget):
        self.AddComponent(comp, -1)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, index: int):
        layout = self.Layout if isinstance(self, ComponentBase) else self.layout()
        self.AddComponent(comp, layout, index)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layout: QLayout):
        self.AddComponent(comp, layout, -1)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layout: QLayout, index: int):
        if isinstance(comp, ComponentBase):
            comp.Parent = self
        else:
            comp.setParent(self)

        if index <= 0:
            layout.addWidget(comp)
        else:
            layout.insertWidget(index, comp)

        comp.setVisible(True)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layoutName: str, index: int):
        layout: QLayout = findLayoutByName(self.layout(), layoutName)  # type: ignore

        if layout is None:
            jAGException(f"Layout {layoutName} not found", KeyError(f"Error trying to find layout {layoutName} from {self.Name}"))

        self.AddComponent(comp, layout, index)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layoutName: str):
        self.AddComponent(comp, layoutName, -1)

    @OverloadDispatcher
    def RemoveComponent(self, comp: QWidget):
        if not comp:
            return
        comp.setVisible(False)
        self.Layout.removeWidget(comp)
        comp.setParent(None)
        comp.deleteLater()
        return comp

    @RemoveComponent.overload
    def RemoveComponent(self, objectName: str):
        comp = self.Layout.findChild(QObject, objectName)
        return self.RemoveComponent(comp)
