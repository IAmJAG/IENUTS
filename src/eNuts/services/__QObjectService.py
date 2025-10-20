import weakref

# ------------------------------------------------------
from threading import Lock, RLock, Thread

from PySide6.QtCore import QObject, Signal

# ------------------------------------------------------
from jAGFx.logger import error


class Service(QObject):
    OnStarted: Signal = Signal(Thread)
    OnTerminated: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._terminatedLock: Lock = RLock()
        self._terminated: bool = True
        self._thread: Thread = None

        weakref.ref(self, self.stop)

    def _service(self):
        try:
            while not self.IsTerminated():
                self.service()

        except Exception as ex:
            error("Error in service thread", ex)

    def IsTerminated(self):
        with self._terminatedLock:
            return self._terminated

    def Terminate(self):
        with self._terminatedLock:
            self._terminated = True

    @property
    def isAlive(self):
        return not self._terminated

    def service(self):
        raise NotImplementedError("Service.service must be overridden in subclasses")

    def start(self, *param):
        if self.isAlive:
            return

        with self._terminatedLock:
            self._terminated = False
            self._thread = Thread(target=self._service, daemon=True, args=param)
            self._thread.start()

    def stop(self):
        if not self.isAlive:
            return

        if self._thread is not None and self._thread.is_alive():
            self._thread.join(0.01)
            self._thread = None

        with self._terminatedLock:
            self._terminated = True
