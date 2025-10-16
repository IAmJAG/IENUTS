from threading import Lock, Thread
from time import sleep

from adbutils import AdbDevice, adb
from jAGFx.logger import warning
from jAGFx.singleton import SingletonF
from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QApplication


@SingletonF
class DeviceMonitor(QObject):
    OnDeviceAdded: Signal = Signal(AdbDevice)
    OnDeviceRemoved: Signal = Signal(AdbDevice)

    def __init__(self) -> None:
        super().__init__()
        self._enderLock: Lock = Lock()
        self._ender: object = None
        self._thread: Thread = Thread(target=self._run, daemon=True)

    @property
    def Ender(self) -> object:
        with self._enderLock:
            return self._ender

    def _run(self):
        lDevices: dict[str, AdbDevice] = dict[str, AdbDevice]()
        lAppIns: QApplication = QApplication.instance()

        while self.Ender is not None:
            try:
                lNewList: dict[str, AdbDevice] = {device.serial: device for device in adb.device_list()}
                lMarkedRemove: list[AdbDevice] = list[AdbDevice]()

                for srl in lDevices:
                    if srl not in lNewList:
                        lMarkedRemove.append(lDevices[srl])

                for srl in lNewList.keys():
                    if srl not in lDevices:
                        _device: AdbDevice = lNewList[srl]
                        if _device is not None:
                            lDevices.update({srl: _device})
                            self.OnDeviceAdded.emit(_device)

                for device in lMarkedRemove:
                    self.OnDeviceRemoved.emit(lDevices.pop(device.serial))

                if lAppIns is not None:
                    lAppIns.processEvents()

            except KeyboardInterrupt:
                with self._enderLock:
                    self._ender = None

            except Exception as ex:
                warning("Error occur in device monitor, pausing monitor for 3 seconds", ex)
                sleep(3)

    def start(self):
        if self.Ender is None:
            self._ender: object = object()
            self._thread.start()
            return

        warning("Already running...")

    def stop(self):
        with self._enderLock:
            self._ender = None
            self._thread.join(0.01)
