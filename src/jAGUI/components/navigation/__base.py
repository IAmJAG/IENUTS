# src/eNuts/UI/sidemenu/__sideMenu.py
from enum import Enum, auto
from types import FunctionType

from jAGUI.components.bases import ComponentBase
from jAGUI.components.utilities import processMarker
from PySide6.QtWidgets import QBoxLayout, QWidget


@processMarker(True, True)
class _navigationBar(ComponentBase):
    OBJCT_NAME = "NAVAGATIONBAR"

    class eNavigationState(Enum):
        EXPANDED = auto()
        COLLAPSED = auto()
        EXPANDING = auto()
        COLLAPSING = auto()

        @property
        def IsIdle(self) -> bool:
            return self in [_navigationBar.eNavigationState.COLLAPSED, _navigationBar.eNavigationState.EXPANDED]

    class eDrawerOrientation(Enum):
        VERTICAL = auto()
        HORIZONTAL = auto()

    def __init__(self, orientation: eDrawerOrientation, parent: QWidget = None, *lArgs, **lKwargs):
        super().__init__(self.OBJCT_NAME, parent, *lArgs, **lKwargs)
        self._collapsedsize = 50
        self._expandedsize = 200

        self._orientation: _navigationBar.eDrawerOrientation = orientation
        self._state: _navigationBar.eNavigationState = _navigationBar.eNavigationState.EXPANDED

    def Load(self):
        super().Load()
        lSize, _, lMaxi = self._getSizeMethods()

        if self.State == _navigationBar.eNavigationState.COLLAPSED:
            lMaxi(self._collapsedsize)
        else:
            lMaxi(self._expandedsize)

        lMid: int = (self._expandedsize - self._collapsedsize) // 2
        if (lSize() - self._collapsedsize) < lMid:
            self._state = _navigationBar.eNavigationState.COLLAPSED
        else:
            self._state = _navigationBar.eNavigationState.EXPANDED

    def setupUI(self, layout: QBoxLayout | None = None):
        super().setupUI(layout)

    def _getSizeMethods(self) -> tuple[FunctionType, FunctionType, FunctionType]:
        if self.Orientation == _navigationBar.eDrawerOrientation.HORIZONTAL:
            return self.width, self.setMinimumWidth, self.setMaximumWidth
        return self.height, self.setMinimumHeight, self.setMaximumHeight

    def _collapse(self):
        self._state = _navigationBar.eNavigationState.COLLAPSED

    def _expand(self):
        self._state = _navigationBar.eNavigationState.EXPANDED

    def toggle(self):
        if self.State in [_navigationBar.eNavigationState.COLLAPSED, _navigationBar.eNavigationState.COLLAPSING]:
            self._expand()

        else:
            self._collapse()

    @property
    def Orientation(self) -> eDrawerOrientation:
        return self._orientation

    @property
    def State(self) -> eNavigationState:
        return self._state
