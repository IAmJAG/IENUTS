from jAGFx.overload import OverloadDispatcher
from PySide6.QtCore import QEasingCurve, QEvent, QObject, QPropertyAnimation
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QWidget

from ..types import eOrientation, eRetractableState, eScale


class Scale(QPropertyAnimation):
    def __init__(self, component: QWidget, minValue: int, maxValue: int, duration: int = 250, orientation: eOrientation = eOrientation.HORIZONTAL):
        if not issubclass(type(component), QWidget):
            raise TypeError(f"Invalid target, expecting QWidget, got {type(component).__name__}")

        lProp: bytes = b"maximumHeight" if orientation == eOrientation.VERTICAL else b"maximumWidth"

        super().__init__(component, lProp)
        self.setDuration(duration)
        self._minValue: int = minValue
        self._maxValue: int = maxValue
        self._duration: int = duration
        self._orientation: eOrientation = orientation

        self._state: eRetractableState = eRetractableState.EXPANDED
        lValue = self.targetObject().width() if self.Orientation == eOrientation.HORIZONTAL else self.targetObject().height()
        self._upateState(lValue)

        component.installEventFilter(self)

        def _finished():
            if self.State == eRetractableState.EXPANDING:
                self._state = eRetractableState.EXPANDED
                lFinalValue: int = self._maxValue
            else:
                self._state = eRetractableState.COLLAPSED
                lFinalValue: int = self._minValue

            if self._orientation == eOrientation.VERTICAL:
                component.setMaximumHeight(lFinalValue)
            else:
                component.setMaximumWidth(lFinalValue)

            component.update()

        self.finished.connect(_finished)

    def _upateState(self, value: int):
        if self.State.IsIdle:
            lMidValue: int = (self._maxValue - self._minValue) / 2
            if value >= lMidValue:
                self._state = eRetractableState.EXPANDED
            else:
                self._state = eRetractableState.COLLAPSED

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched == self.targetObject() and event.type() == QEvent.Type.Resize:
            if self.State.IsIdle:
                lResizeEvent: QResizeEvent = event
                lValue: int = lResizeEvent.size().width() if self._orientation == eOrientation.HORIZONTAL else lResizeEvent.size().height()
                self._upateState(lValue)

        return super().eventFilter(watched, event)

    @property
    def State(self) -> eRetractableState:
        return self._state

    @property
    def Orientation(self) -> eOrientation:
        return self._orientation

    @OverloadDispatcher
    def start(self, duration: int, scale: eScale = eScale.EXPAND):
        if self.State.IsTransitioning:
            self._stop()

        self.targetObject().setVisible(True)

        lStartValue: int = self.targetObject().width() if self.Orientation == eOrientation.HORIZONTAL else self.targetObject().height()
        lEndValue: int = self._maxValue if scale == eScale.EXPAND else self._minValue
        self._duration = duration

        self.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.setStartValue(lStartValue)
        self.setEndValue(lEndValue)
        self.setDuration(duration)

        self._state = eRetractableState.COLLAPSING if lEndValue < lStartValue else eRetractableState.EXPANDING
        return super().start()

    @start.overload
    def start(self):
        if self.State in [eRetractableState.COLLAPSED, eRetractableState.COLLAPSING]:
            self.start(self._duration, eScale.EXPAND)
        else:
            self.start(self._duration, eScale.COLLAPSE)

    def _stop(self):
        super().stop()

    def stop(self):
        if self.State == eRetractableState.EXPANDING:
            lFinalValue: int = self._maxValue
        else:
            lFinalValue: int = self._minValue

        if self._orientation == eOrientation.VERTICAL:
            self.targetObject().setMaximumHeight(lFinalValue)
        else:
            self.targetObject().setMaximumWidth(lFinalValue)

        self._stop()

    def toggle(self):
        self.start()
