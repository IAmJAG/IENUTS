import os
import socket
import struct
from queue import Queue
from threading import Lock
from time import sleep
from types import FunctionType

from adbutils import AdbConnection, AdbDevice, AdbError, Network, adb
from av import CodecContext, Packet, VideoFrame
from av.error import InvalidDataError
from numpy import ndarray

from jAGFx.logger import debug, error, warning
from jAGFx.service import Service

from ..scrcpy.controls import BaseAppControl

JAR_NAME: str = "scrcpy-server.jar"
FPS: int = 120
BITRATE: int = 1000000000
MAX_PACKET_RECIEVE: int = 0x10000


class AndroidStreamer(Service):
    def __init__(self, title: str, serial: str = None, maxwidth: int = 800, connectionTimeout: int = 3000, package: str = None) -> None:
        super().__init__()
        self._title: str = title
        self._serial: str = serial.strip().lower()
        self._deviceName: str = self._serial
        self._device: AdbDevice = None
        self._imageQueue: Queue = Queue(128)

        self._maxwidth: int = maxwidth

        self._serverStream: AdbConnection = None
        self._vsocket: socket.socket = None
        self._csocket: socket.socket = None
        self._csocketLock: Lock = Lock()

        self._connectionTimeout: int = connectionTimeout

        self._resolution: tuple[int, int] = (0, 0)

        self._onframe: FunctionType = None

        self._control: BaseAppControl = BaseAppControl(self)

        self._isActiveLock: Lock = Lock()
        self._isActive: bool = False

        self._packagename: str = package

    @property
    def PackageName(self) -> str:
        return self._packagename

    @property
    def ControlSocket(self) -> socket.socket:
        with self._csocketLock:
            return self._csocket

    @property
    def Control(self) -> BaseAppControl:
        if self._control is None:
            self._control = BaseAppControl(self)

        return self._control

    @Control.setter
    def Control(self, value: BaseAppControl):
        self._control = value

    @property
    def MaxWidth(self) -> int:
        return self._maxwidth

    @property
    def Resolution(self) -> tuple[int, int]:
        return self._resolution

    @property
    def SizeRatio(self) -> float:
        return self.MaxWidth / max(self.Resolution)

    def setOnFrame(self, func: FunctionType):
        self._onframe = func

    def _onFrame(self, frame: ndarray):
        if self._onframe is not None and isinstance(self._onframe, FunctionType):
            self._onframe(frame)

    @property
    def Device(self) -> AdbDevice:
        if self._device is None:
            lDevices: dict[str, AdbDevice] = {device.serial.upper(): device for device in adb.device_list()}

            if len(lDevices) == 0:
                error("No device found!!!")

            lDevice: AdbDevice = lDevices.get(self.Serial.upper(), None)

            if lDevice is None:
                warning(f"Device {self.Serial} not found. Getting default")
                lDevice = next(iter(lDevices.values()), None)

            self._device = lDevice
        return self._device

    def _initServerConnection(self) -> None:
        for _ in range(self._connectionTimeout // 100):
            try:
                self._vsocket = self.Device.create_connection(Network.LOCAL_ABSTRACT, "scrcpy")
                break

            except AdbError:
                sleep(0.1)
                pass

        else:
            raise ConnectionError("Failed to connect scrcpy-server after 3 seconds")

        lDummyByte = self._vsocket.recv(1)
        if not len(lDummyByte) or lDummyByte != b"\x00":
            raise ConnectionError("Did not receive Dummy Byte!")

        self._csocket = self.Device.create_connection(Network.LOCAL_ABSTRACT, "scrcpy")

        self._deviceName = self._vsocket.recv(64).decode("utf-8").rstrip("\x00")
        if not len(self._deviceName):
            raise ConnectionError("Did not receive Device Name!")

        lRes = self._vsocket.recv(4)
        self._resolution = struct.unpack(">HH", lRes)
        self._vsocket.setblocking(False)

    def _deployServer(self) -> None:
        lServerPath: str = os.path.join(
            os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            JAR_NAME,
        )

        if not os.path.exists(lServerPath):
            debug(f"{JAR_NAME} JAR file does not exist - {lServerPath}")

        lRemotePath: str = f"/data/local/tmp/{JAR_NAME}"
        try:
            self.Device.sync.push(lServerPath, lRemotePath)

            lCommands: list[str] = [
                f"CLASSPATH={lRemotePath}",
                "app_process",
                "/",
                "com.genymobile.scrcpy.Server",
                "2.4",
                "log_level=info",
                f"max_size={self.MaxWidth}",
                f"max_fps={FPS}",
                f"video_bit_rate={BITRATE}",
                "tunnel_forward=true",
                "send_frame_meta=false",
                "control=true",
                "audio=false",
                "show_touches=false",
                "stay_awake=false",
                "power_off_on_close=false",
                "clipboard_autosync=false",
            ]

            self._serverStream = self.Device.shell(lCommands, stream=True)
            self._serverStream.read(10)

        except Exception as ex:
            raise ex

    def start(self):
        if self.isAlive:
            return
        self._deployServer()
        self._initServerConnection()
        super().start()

    @property
    def DeviceName(self) -> str:
        return getattr(self, "_deviceName", None)

    @property
    def Serial(self) -> str:
        return self._serial

    @Serial.setter
    def Serial(self, value: str) -> None:
        self._serial = value.strip().lower()

    def service(self):
        lCodec = CodecContext.create("h264", "r")
        while self.isAlive:
            try:
                lRAWh264: bytes = self._vsocket.recv(MAX_PACKET_RECIEVE)
                if lRAWh264 == b"":
                    self.stop()
                    raise ConnectionError("Video stream is disconnected")

                lPackets: list[Packet] = lCodec.parse(lRAWh264)
                for lPacket in lPackets:
                    lFrames: list[VideoFrame] = lCodec.decode(lPacket)
                    for lFrame in lFrames:
                        self._resolution = (lFrame.shape[1], lFrame.shape[0])
                        self._onFrame(lFrame)

            except (BlockingIOError, InvalidDataError):
                sleep(0.01)
                self._onFrame(None)
                pass

            except Exception as ex:
                debug("Error in service thread", ex)

    @property
    def ImageQueue(self) -> Queue:
        return self._imageQueue

    @property
    def Title(self) -> str:
        return self._title

    @Title.setter
    def Title(self, value: str) -> None:
        self._title = value

    @property
    def IsActive(self) -> bool:
        with self._isActiveLock:
            return self._isActive

    @IsActive.setter
    def IsActive(self, value: bool):
        with self._isActiveLock:
            self._isActive = value
