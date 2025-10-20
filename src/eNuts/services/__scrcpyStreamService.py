import os
import socket
import struct
from threading import Lock
from time import sleep

from adbutils import AdbConnection, AdbDevice, AdbError, Network, adb, device
from av import CodecContext, Packet, VideoFrame
from av.error import InvalidDataError
from numpy import ndarray
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication

from jAGFx.logger import debug, error, warning

from ..scrcpy.controls import BaseAppControl
from .__streamService import StreamService

JAR_NAME: str = "scrcpy-server.jar"
FPS: int = 120
BITRATE: int = 1000000000
MAX_PACKET_RECIEVE: int = 0x10000


class SCRCPYStreamService(StreamService):
    def __init__(self, adbSerial: str = None, maxWidth: int = 800, connectionTimeout: int = 3000) -> None:
        super().__init__(name=adbSerial, maxWidth=maxWidth)
        self._adbserial: str = adbSerial

        self._device: AdbDevice = None

        self._serverStream: AdbConnection = None
        self._vsocket: socket.socket = None
        self._csocket: socket.socket = None
        self._csocketLock: Lock = Lock()
        self._codec: CodecContext = None

        self._connectionTimeout: int = connectionTimeout
        self._control: BaseAppControl = BaseAppControl(self)

    def _initServerConnection(self) -> None:
        debug("Connecting to scrcpy server...")
        for _ in range(self._connectionTimeout // 100):
            try:
                self._vsocket = self.Device.create_connection(Network.LOCAL_ABSTRACT, "scrcpy")
                break

            except AdbError:
                sleep(0.1)
                pass

        else:
            raise ConnectionError(f"Failed to connect scrcpy-server after {self._connectionTimeout / 1000} seconds")

        debug("Connected to scrcpy server, waiting for handshake...")

        lDummyByte = self._vsocket.recv(1)
        if not len(lDummyByte) or lDummyByte != b"\x00":
            raise ConnectionError("Did not receive Dummy Byte!")

        debug("Handshake success. Received dummy byte.")

        debug("Creating control socket...")
        self._csocket = self.Device.create_connection(Network.LOCAL_ABSTRACT, "scrcpy")

        self._deviceName = self._vsocket.recv(64).decode("utf-8").rstrip("\x00")
        if not len(self._deviceName):
            raise ConnectionError("Did not receive Device Name!")

        debug(f"Control established to device: {self._deviceName}")

        lRes = self._vsocket.recv(4)
        self._size = struct.unpack(">HH", lRes)
        self._vsocket.setblocking(False)

    def _deployServer(self) -> None:
        lServerPath: str = os.path.join(
            "\\WS\\nutsLAB\\eNuts\\src\\eNuts" ,
            JAR_NAME,
        )

        if not os.path.exists(lServerPath):
            debug(f"{JAR_NAME} JAR file does not exist - {lServerPath}")

        lRemotePath: str = f"/data/local/tmp/{JAR_NAME}"
        try:
            debug(f"Deploying {JAR_NAME} to device...")
            self.Device.sync.push(lServerPath, lRemotePath)
            lCommands: list[str] = [
                f"CLASSPATH={lRemotePath}",
                "app_process",
                "/",
                "com.genymobile.scrcpy.Server",
                "2.4",
                "log_level=info",
                f"max_size={self.MaximumWidth}",
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

            debug("Starting scrcpy server...")
            self._serverStream = self.Device.shell(lCommands, stream=True)
            self._serverStream.read(10)

            debug("scrcpy server started successfully")

        except Exception as ex:
            raise ex

    # region [PROPERTIES]
    @property
    def ADBSerial(self) -> str:
        return self._adbserial

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
    def SizingRatio(self) -> float:
        return self.MaximumWidth / max(self.size)

    @property
    def Name(self) -> str:
        return self.DeviceName or super().Name

    @property
    def Device(self) -> AdbDevice:
        if self._device is None:
            lDevices: dict[str, AdbDevice] = {device.serial.upper(): device for device in adb.device_list()}

            if len(lDevices) == 0:
                error("No ADB Device found!")
                return None

            lDevice: AdbDevice = lDevices.get(self.ADBSerial.upper(), None)

            if lDevice is None:
                warning(f"Device {self.ADBSerial} not found. Returning default")
                lDevice = next(iter(lDevices.values()), None)

            self._device = lDevice

        return self._device

    @property
    def DeviceName(self) -> str:
        return getattr(self, "_deviceName", None)

    @property
    def Serial(self) -> str:
        if not hasattr(self, "_serial"):
            self._serial: str = self.Device.shell(["getprop", "ro.serialno"])

        if self._serial is None:
            self._serial = self._adbserial

        return self._serial

    # endregion [PROPERTIES]

    def _cleanUp(self):
        if self._serverStream is not None:
            self._serverStream.close()
            self._serverStream = None

        if self._vsocket is not None:
            self._vsocket.close()
            self._vsocket = None

        with self._csocketLock:
            if self._csocket is not None:
                self._csocket.close()
                self._csocket = None

        self._codec = None
        self.OnTerminated.emit()

    def _initService(self):
        try:
            debug("Initializing scrcpy service...")
            self._deployServer()
            self._initServerConnection()
            self._codec: CodecContext = CodecContext.create("h264", "r")
            self._lastFrame: ndarray = None
            self.OnStarted.emit(self._thread)
            self._cntr = 0

        except Exception as ex:
            warning("Error occurred while starting scrcpy service", ex)

    def service(self):
        try:
            lRAWh264: bytes = self._vsocket.recv(MAX_PACKET_RECIEVE)
            if lRAWh264 == b"":
                self.stop()
                raise ConnectionError("Video stream is disconnected")

            lPackets: list[Packet] = self._codec.parse(lRAWh264)
            for lPacket in lPackets:
                lFrames: list[VideoFrame] = self._codec.decode(lPacket)
                for lFrame in lFrames:
                    lArrFrame: ndarray = lFrame.to_ndarray(format="bgr24")
                    self.OnFrame.emit(lArrFrame)
                    self._lastFrame = lArrFrame
                    self._setSize(QSize(lArrFrame.shape[1], lArrFrame.shape[0]))

        except (BlockingIOError, InvalidDataError):
            sleep(0.00001)
            self.OnFrame.emit(self._lastFrame)

        except Exception as ex:
            error("Error in service thread", ex)
