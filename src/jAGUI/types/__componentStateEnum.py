from enum import Enum


class eComponentState(Enum):
    DISABLED = 0x00
    ENABLED = 0x01
    FOCUS = 0x02
    SELECTED = 0x04
    HOVER = 0x08
    PRESSED = 0x10
