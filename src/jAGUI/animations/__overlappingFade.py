from jAGFx.overload import OverloadDispatcher
from PySide6.QtCore import (
    QParallelAnimationGroup,
    QPauseAnimation,
    QSequentialAnimationGroup,
)
from PySide6.QtWidgets import QWidget

from ..types import eFade, eFadingState
from .__fade import Fade


class WatterFallFade(QParallelAnimationGroup):
    def __init__(self, components: list[QWidget], duration: int = 700, staggerTime: int = 100, ):
        super().__init__()
        self._components: list[QWidget] = components
        self._duration = duration
        self._staggerTime = staggerTime

        self._state: eFadingState = eFadingState.VISIBLE
        for comp in self._components:
            comp.setOpacity(1.0)
            comp.setVisible(True)

        self._setupAnimations()

        def _finished():
            if self.State == eFadingState.FADING_IN:
                self._state = eFadingState.VISIBLE

            if self.State == eFadingState.FADING_OUT:
                self._state = eFadingState.HIDDEN

        self.finished(_finished)

    @property
    def State(self) -> eFadingState:
        return self._state

    def Reverse(self):
        self._components = self._components[::-1]

    def _setupAnimations(self, fade: eFade = eFade.FADEIN):
        self.clear()
        for i, lComponent in enumerate(self._components):
            lSeqGroup = QSequentialAnimationGroup(self)

            lPauseAni = QPauseAnimation(i * self._staggerTime, self)
            lFadeAni: Fade = Fade(lComponent, self._duration, fade)

            lSeqGroup.addAnimation(lPauseAni)
            lSeqGroup.addAnimation(lFadeAni)

            self.addAnimation(lSeqGroup)

    @OverloadDispatcher
    def start(self, duration: int = 700, staggerTime: int = 100, fade: eFade = eFade.FADEIN):
        if self.State.IsTransitioning:
            self._stop()

        lIsFadingIn: bool = fade == eFade.FADEIN
        try:

            self._duration = duration
            self._staggerTime = staggerTime
            self._setupAnimations(fade)

            self._state = eFadingState.FADING_IN if lIsFadingIn else eFadingState.FADING_OUT
            return super().start()

        except Exception as ex:
            raise Exception("Error in animation", ex)

    @start.overload
    def start(self):
        lFade: eFade
        if self.State in [eFadingState.FADING_IN, eFadingState.VISIBLE]:
            lFade = eFade.FADEOUT
        else:
            lFade = eFade.FADEIN

        self.start(self._duration, self._staggerTime, lFade)

    def _stop(self):

        super().stop()
