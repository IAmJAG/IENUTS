import os

# ------------------------------------------------------
from typing import Any

# ------------------------------------------------------
from PySide6.QtCore import QSettings, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QMainWindow, QSpacerItem, QWidget

# ------------------------------------------------------
from jAGFx.configuration import ApplicationConfiguration, iConfiguration
from jAGFx.dependencyInjection import Provider
from jAGFx.exceptions import jAGException
from jAGFx.overload import OverloadDispatcher
from jAGFx.utilities.io import getICONPath

# ------------------------------------------------------
from ....contracts import iComponent
from ...central import Central
from ...utilities import findLayoutByName, processMarker

__all__ = ["FormBase"]


@processMarker(True, True)
class FormBase(QMainWindow, iComponent):
    OnPropertyChanged: Signal = Signal(Any, str, bool, bool)

    def __init__(self, frameless: bool = False):
        super().__init__()
        try:
            super().setObjectName("MAINWINDOW")

            if frameless:
                self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

            cfg: ApplicationConfiguration = Provider.Resolve(iConfiguration)
            self.Title = cfg.Title
            self.Icon = QIcon(os.path.join(getICONPath(), f"{cfg.Icon}.png"))
            self._company: str = cfg.Company
            self._appId: str = cfg.AppId
            self._logo: str = cfg.Icon
            self._qsettings = QSettings(self.Company, self.ApplicationId)

        except Exception as ex:
            raise jAGException(
                f"Error in {__name__}{self.__class__.__name__}.__init__", ex
            ) from ex

    def Load(self): ...

    def setupUI(self) -> None:
        self._central: Central = Central()
        self.setCentralWidget(self._central)
        self.restoreWindowsState()

    @property
    def Orientation(self) -> QBoxLayout.Direction:
        if isinstance(QBoxLayout, self.layout):
            return self.Layout.direction()
        return None

    @Orientation.setter
    def Orientation(self, value: QBoxLayout.Direction):
        if isinstance(QBoxLayout, self.layout):
            self.Layout.setDirection(value)

    @property
    def Layout(self) -> QBoxLayout:
        if hasattr(self, "_layout"):
            return self._layout

        return self.centralWidget().layout()

    @Layout.setter
    def Layout(self, value: QBoxLayout) -> None:
        if hasattr(self, "_layout"):
            self._layout = value
        else:
            self.centralWidget().setLayout(value)

    @property
    def Central(self):
        return self.centralWidget()

    @property
    def Title(self):
        return self.windowTitle()

    @Title.setter
    def Title(self, value: str):
        self.setWindowTitle(value)

    @property
    def Icon(self) -> QIcon:
        return self.windowIcon()

    @Icon.setter
    def Icon(self, value: QIcon):
        self.setWindowIcon(value)

    @property
    def Name(self) -> str:
        return self.objectName()

    @Name.setter
    def Name(self, value: str):
        self.setObjectName(value)

    def saveWindowState(self) -> None:
        self.Settings.setValue("geometry", self.geometry())
        self.Settings.setValue("windowState", self.windowState())

    def restoreWindowsState(self) -> None:
        if self.Settings.contains("geometry"):
            self.setGeometry(self.Settings.value("geometry"))

        if self.Settings.contains("windowState"):
            self.setWindowState(self.Settings.value("windowState"))

    def CleanUp(self): ...

    def closeEvent(self, event):
        self.CleanUp()
        self.saveWindowState()
        return super().closeEvent(event)

    @property
    def FQN(self) -> str:
        return "[ROOT]"

    @property
    def Settings(self) -> QSettings:
        return self._qsettings

    @Settings.setter
    def Settings(self, value: QSettings):
        self._qsettings = value

    @property
    def Company(self) -> str:
        return self._company

    @Company.setter
    def Company(self, value: str):
        self.Company = value

    @property
    def ApplicationId(self) -> str:
        return self._appId

    @ApplicationId.setter
    def ApplicationId(self, value: str):
        self._appId = value

    @property
    def Logo(self) -> str:
        return self._logo

    @Logo.setter
    def Logo(self, value: str) -> None:
        self._logo = value

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
        layout: QBoxLayout = findLayoutByName(self.Layout, layoutName)
        self.AddComponent(comp, layout, index)

    @AddComponent.overload
    def AddComponent(self, comp: QWidget, layout: QBoxLayout, index: int):
        layout = self.Layout if layout is None else layout

        # check the last item in the layout
        lItemLastAdded = layout.itemAt(layout.count() - 1)
        if isinstance(lItemLastAdded, QSpacerItem):
            layout.removeItem(lItemLastAdded)

        lIsWidget: bool = isinstance(comp, QWidget)

        if hasattr(comp, "Parent"):
            comp.Parent = self.centralWidget()
        else:
            if lIsWidget:
                comp.setParent(self.centralWidget())

        if index <= 0:
            layout.addWidget(comp)
        else:
            layout.insertWidget(index, comp)

        comp.setVisible(lIsWidget)

    @OverloadDispatcher
    def RemoveComponent(self, comp: QWidget):
        if not comp:
            return
        comp.setVisible(False)
        self.Layout.removeWidget(comp)
        comp.setParent(None)  # type: ignore
        return comp

    @RemoveComponent.overload
    def RemoveComponent(self, objectName: str):
        comp = self.Layout.findChild(QWidget, objectName)
        return self.RemoveComponent(comp)
