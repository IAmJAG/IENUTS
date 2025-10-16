from .const import (
    KEYCODE_CTRL_LEFT,
    KEYCODE_DEL,
    KEYCODE_ENTER,
    KEYCODE_SHIFT_LEFT,
    KEYCODE_SPACE,
    KEYCODE_TAB,
)


def mapCode(code):
    if code == -1:
        return -1
    if 48 <= code <= 57:
        return code - 48 + 7
    if 65 <= code <= 90:
        return code - 65 + 29
    if 97 <= code <= 122:
        return code - 97 + 29

    hard_code = {
        32: KEYCODE_SPACE,
        16777219: KEYCODE_DEL,
        16777248: KEYCODE_SHIFT_LEFT,
        16777220: KEYCODE_ENTER,
        16777217: KEYCODE_TAB,
        16777249: KEYCODE_CTRL_LEFT,
    }
    if code in hard_code:
        return hard_code[code]

    print(f" key: {code}")

    return -1
