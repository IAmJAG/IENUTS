from enum import Enum, auto

class eFade(Enum):
    FADEIN = 0x00
    FADEOUT = 0x01

class eScale(Enum):
    EXPAND = 0x00
    COLLAPSE = 0x01


class AnimationStateMixin:
    @property
    def IsIdle(self):
        # You might need a more robust way to identify them, e.g., a specific attribute
        return self.value in (0x00, 0x01) # Or self.name in ('COLLAPSED', 'EXPANDED') etc.

    @property
    def IsTransitioning(self):
        return not self.IsIdle

class eAnimationState(AnimationStateMixin, Enum):
    OFF = 0x00
    ON = 0x01
    TRANSITIONING_OFF = 0x02
    TRANSITIONING_ON = 0x03

class eRetractableState(AnimationStateMixin, Enum):
    COLLAPSED = eAnimationState.OFF
    EXPANDED = eAnimationState.ON
    COLLAPSING = 0x02
    EXPANDING = 0x03

class eFadingState(AnimationStateMixin, Enum):
    HIDDEN = eAnimationState.OFF
    VISIBLE = eAnimationState.ON
    FADING_OUT = 0x02
    FADING_IN = 0x03
