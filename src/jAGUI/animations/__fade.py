
from jAGFx.overload import OverloadDispatcher
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget

from ..types import eFade, eFadingState


class Fade(QPropertyAnimation):
    def __init__(self, component: QWidget, duration: int = 500):
        if not isinstance(component, QWidget):
            raise TypeError(f"Invalid target, expecting QWidget, got {type(component).__name__}")

        self._state: eFadingState = eFadingState.HIDDEN
        if not isinstance(component.graphicsEffect(), QGraphicsOpacityEffect):
            lOpecityEffect = QGraphicsOpacityEffect(component)
            component.setGraphicsEffect(lOpecityEffect)
            if component.graphicsEffect().opacity() == 0.0:
                self._state = eFadingState.HIDDEN
            else:
                self._state = eFadingState.VISIBLE

        super().__init__(component.graphicsEffect(), b"opacity")

        self._duration: int = duration

        def _finished():
            lIsFadingIn: bool = self.State == eFadingState.FADING_IN
            component.setVisible(lIsFadingIn)
            self._state = eFadingState.VISIBLE if lIsFadingIn else eFadingState.HIDDEN
            component.update()

        self.finished.connect(_finished)

    @property
    def State(self) -> eFadingState:
        return self._state

    @OverloadDispatcher
    def start(self, duration: int, fade: eFade):
        if self.State.IsTransitioning:
            self._stop()

        lIsFadingIn: bool = fade == eFade.FADEIN
        self._duration = duration

        try:
            lCurrOpacity: float = self.targetObject().opacity()
            self.setStartValue(lCurrOpacity)
            self.setEndValue(1.0 if lIsFadingIn else 0.0)
            self.setDuration(duration)

            self._state = eFadingState.FADING_IN if lIsFadingIn else eFadingState.FADING_OUT
            return super().start()

        except Exception as ex:
            raise Exception("Error in animation", ex)

    @start.overload
    def start(self):
        ## toggles between fade in and fade out
        lFade: eFade = eFade.FADEOUT if self.State in [eFadingState.VISIBLE, eFadingState.FADING_IN] else eFade.FADEIN
        self.start(self._duration, lFade)

    def toggle(self):
        self.start()

    def _stop(self):
        super().stop()

    def stop(self):
        if self.targetObject().opacity() < 0.5: # Or some other threshold
            self._state = eFadingState.HIDDEN
            self.targetObject().parent().setVisible(False)
        else:
            self._state = eFadingState.VISIBLE
            self.targetObject().parent().setVisible(True)

        self._stop()
