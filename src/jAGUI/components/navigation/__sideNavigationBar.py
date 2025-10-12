import os
from threading import RLock

from jAGFx.utilities.io import getICONPath
from jAGUI.components import Button, ContainerBase
from jAGUI.components.utilities import processMarker
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QWidget

from ...types import eIconAlignment
from .__base import _navigationBar

ICONPATH: str = "UIUX"
ICONCOLLAPSED: str = "show.png"  # expand
ICONEXPANDED: str = "hide.png"  # collapse
ICONTRANSITION: str = "logoxx.png"

DRAWERBUTTONHEIGHT: int = 50


@processMarker(True, True)
class SideNavigationBar(_navigationBar):
    OnStateChanged: Signal = Signal(_navigationBar, _navigationBar.eNavigationState, _navigationBar.eNavigationState)

    def __init__(self, text: str, ico: str | QIcon = "logo.png", parent: QWidget = None, *lArgs, **lKwargs):
        super().__init__(_navigationBar.eDrawerOrientation.HORIZONTAL, parent, *lArgs, **lKwargs)
        self._text: str = text
        self._icon: QIcon = ico if isinstance(ico, QIcon) else QIcon(getICONPath(ico))
        self._iconalignment: eIconAlignment = eIconAlignment.LEFT

        lprop: bytes
        if self.Orientation == _navigationBar.eDrawerOrientation.VERTICAL:
            lprop = b"minimumHeight"
        else:
            lprop = b"minimumWidth"

        self._stateLock: RLock = RLock()

        def _finished():
            lSize, _, _ = self._getSizeMethods()
            lMid: int = (self._expandedsize - self._collapsedsize) // 2
            if (lSize() - self._collapsedsize) < lMid:
                self.State = _navigationBar.eNavigationState.COLLAPSED
            else:
                self.State = _navigationBar.eNavigationState.EXPANDED

        self._animation: QPropertyAnimation = QPropertyAnimation(self, lprop, self)
        self.AnimationDuration = 300
        self.EasingCurve = QEasingCurve.Type.InOutExpo

        self._animation.finished.connect(_finished)
        self.OnStateChanged.connect(self._getStateChanged())

    def Load(self):
        super().Load()
        del self._text
        del self._icon
        del self._iconalignment

    def setupUI(self, layout: QBoxLayout | None = None):
        super().setupUI(layout)
        lDrawerButton: Button = Button(self._text, self._icon)
        lDrawerButton.setIconSize(QSize(DRAWERBUTTONHEIGHT, DRAWERBUTTONHEIGHT) - QSize(10, 15))
        lDrawerButton.OnClicked.connect(self.toggle)
        lDrawerButton.setFixedHeight(DRAWERBUTTONHEIGHT)
        lDrawerButton.setObjectName("TOGGLEBUTTON")

        lMenuContainer: ContainerBase = ContainerBase(parent=self)
        lMenuContainer.ContentMargins = [0, 5, 0, 0]
        lMenuContainer.ContentSpacing = 1
        lMenuContainer.setObjectName("MENUCONTENTS")

        self.Layout.addWidget(lDrawerButton)
        self.Layout.addWidget(lMenuContainer)

        self._drawerButton: Button = lDrawerButton
        self._layout = lMenuContainer.Layout

    @property
    def Layout(self) -> QBoxLayout:
        if hasattr(self, "_layout") and self._layout is not None:
            return self._layout
        return super().Layout

    @Layout.setter
    def Layout(self, value: QBoxLayout):
        if hasattr(self, "_layout"):
            self._layout = value

        super().Layout = value

    def toggle(self, btn: Button):
        super().toggle()

    def _getStateChanged(self):
        def _stateChanged(_self: _navigationBar, old: _navigationBar.eNavigationState, new: _navigationBar.eNavigationState):
            # lICOPath: str = os.path.join(ICONPATH, ICONTRANSITION)
            lICOPath: str = None
            if self.State.IsIdle:
                if self.State == SideNavigationBar.eNavigationState.COLLAPSED:
                    lICOPath = os.path.join(ICONPATH, ICONCOLLAPSED)
                else:
                    lICOPath = os.path.join(ICONPATH, ICONEXPANDED)

                self._drawerButton.setIcon(QIcon(getICONPath(lICOPath)))

        return _stateChanged

    def _collapse(self):
        lSize, _, _ = self._getSizeMethods()
        self._animation.setStartValue(lSize())
        self._animation.setEndValue(self._collapsedsize)
        self.State = SideNavigationBar.eNavigationState.COLLAPSING
        self._animation.start()

    def _expand(self):
        lSize, _, _ = self._getSizeMethods()
        self._animation.setStartValue(lSize())
        self._animation.setEndValue(self._expandedsize)
        self.State = SideNavigationBar.eNavigationState.EXPANDING
        self._animation.start()

    @property
    def AnimationDuration(self) -> int:
        self._animation.duration()

    @AnimationDuration.setter
    def AnimationDuration(self, value: int):
        self._animation.setDuration(value)

    @property
    def EasingCurve(self) -> QEasingCurve:
        self._animation.easingCurve()

    @EasingCurve.setter
    def EasingCurve(self, value: QEasingCurve):
        self._animation.setEasingCurve(value)

    @property
    def State(self) -> _navigationBar.eNavigationState:
        return super().State

    @State.setter
    def State(self, value: _navigationBar.eNavigationState):
        with self._stateLock:
            lPState: SideNavigationBar.eNavigationState = self._state
            self._state = value
            self.OnStateChanged.emit(self, lPState, self._state)
