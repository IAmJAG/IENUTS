import socket
import struct
from time import sleep

from ..contracts import iPakageInfo
from ..scrcpy import const


class ControlSender:
    def __init__(self, parent: iPakageInfo):
        self._parent: iPakageInfo = parent

    @property
    def Parent(self) -> iPakageInfo:
        return self._parent

    def _send_package(self, control_type: int, package: bytes) -> None:
        package = struct.pack(">B", control_type) + package
        if self.Parent.ControlSocket is not None:
            self.Parent.ControlSocket.send(package)

    def keycode(self, keycode: int, action: int = const.ACTION_DOWN, repeat: int = 0) -> bytes:
        package = struct.pack(">Biii", action, keycode, repeat, 0)
        self._send_package(const.TYPE_INJECT_KEYCODE, package)
        return package

    def text(self, text: str) -> bytes:
        buffer = text.encode("utf-8")
        package = struct.pack(">i", len(buffer)) + buffer
        self._send_package(const.TYPE_INJECT_TEXT, package)
        return package

    def touch(self, x: int, y: int, action: int = const.ACTION_DOWN, touch_id: int = 0x1234567887654321) -> bytes:
        x, y = max(x, 0), max(y, 0)
        package = struct.pack(
            ">BqiiHHHii",
            action,
            touch_id,
            int(x),
            int(y),
            int(self.Parent.Resolution.width()),
            int(self.Parent.Resolution.height()),
            0xFFFF,
            1,
            1,
        )
        self._send_package(const.TYPE_INJECT_TOUCH_EVENT, package)
        return package

    def scroll(self, x: int, y: int, h: int, v: int) -> bytes:
        x, y = max(x, 0), max(y, 0)
        package = struct.pack(
            ">iiHHii",
            int(x),
            int(y),
            int(self.Parent.Resolution[0]),
            int(self.Parent.Resolution[1]),
            int(h),
            int(v),
        )
        self._send_package(const.TYPE_INJECT_SCROLL_EVENT, package)
        return package

    def back_or_turn_screen_on(self, action: int = const.ACTION_DOWN) -> bytes:
        package = struct.pack(">B", action)
        self._send_package(const.TYPE_BACK_OR_SCREEN_ON, package)
        return package

    def expand_notification_panel(self) -> bytes:
        package = b""
        self._send_package(const.TYPE_EXPAND_NOTIFICATION_PANEL, package)
        return package

    def expand_settings_panel(self) -> bytes:
        package = b""
        self._send_package(const.TYPE_EXPAND_SETTINGS_PANEL, package)
        return package

    def collapse_panels(self) -> bytes:
        package = b""
        self._send_package(const.TYPE_COLLAPSE_PANELS, package)
        return package

    def get_clipboard(self) -> str:
        s: socket.socket = self.Parent.ControlSocket

        with self.Parent._csocketLock:
            s.setblocking(False)
            while True:
                try:
                    s.recv(1024)
                except BlockingIOError:
                    break
            s.setblocking(True)

            package = struct.pack(">B", const.TYPE_GET_CLIPBOARD)
            s.send(package)
            (code,) = struct.unpack(">B", s.recv(1))
            assert code == 0
            (length,) = struct.unpack(">i", s.recv(4))

            return s.recv(length).decode("utf-8")

    def set_clipboard(self, text: str, paste: bool = False) -> bytes:
        buffer = text.encode("utf-8")
        package = struct.pack(">?i", paste, len(buffer)) + buffer
        self._send_package(const.TYPE_SET_CLIPBOARD, package)
        return package

    def set_screen_power_mode(self, mode: int = const.POWER_MODE_NORMAL) -> bytes:
        package = struct.pack(">b", mode)
        self._send_package(const.TYPE_SET_SCREEN_POWER_MODE, package)
        return package

    def rotate_device(self) -> bytes:
        package = b""
        self._send_package(const.TYPE_ROTATE_DEVICE, package)
        return package

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, move_step_length: int = 5, move_steps_delay: float = 0.005, touch_id: int = 0x1234567887654321) -> None:
        self.touch(start_x, start_y, const.ACTION_DOWN)
        next_x, next_y = start_x, start_y

        end_x = min(end_x, self.Parent.Resolution[0])
        end_y = min(end_y, self.Parent.Resolution[1])

        decrease_x = start_x > end_x
        decrease_y = start_y > end_y

        while True:
            next_x = next_x - move_step_length if decrease_x else next_x + move_step_length
            next_y = next_y - move_step_length if decrease_y else next_y + move_step_length

            next_x = max(min(next_x, end_x), end_x)
            next_y = max(min(next_y, end_y), end_y)

            self.touch(next_x, next_y, const.ACTION_MOVE, touch_id)

            if next_x == end_x and next_y == end_y:
                self.touch(next_x, next_y, const.ACTION_UP, touch_id)
                break
            sleep(move_steps_delay)
