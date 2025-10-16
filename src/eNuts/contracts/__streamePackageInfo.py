from socket import socket

from adbutils import AdbDevice


class iPakageInfo:
    @property
    def PackageName(self) -> str: ...

    @property
    def Title(self) -> str: ...

    @property
    def ControlSocket(self) -> socket: ...

    @property
    def Resolution(self) -> tuple[int, int]: ...

    @property
    def Device(self) -> AdbDevice: ...
