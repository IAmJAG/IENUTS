import weakref

# ------------------------------------------------------
from multiprocessing import Lock
from threading import Thread, current_thread, main_thread

# ------------------------------------------------------
from jAGFx.logger import error


class Service:
    def __init__(self, func=None, params: tuple = None) -> None:
        self._eobj: object = None
        self._eobjLock = Lock()
        self._parameters = params
        self._function = func

        self._thread: Thread
        if self._parameters is None:
            self._thread = Thread(target=self.service, daemon=True)
        else:
            self._thread = Thread(target=self.service, daemon=True, args=self._parameters)

        weakref.ref(self, self.stop)

    @property
    def EOBJ(self) -> object:
        with self._eobjLock:
            return self._eobj

    @property
    def isAlive(self):
        return self.EOBJ is not None

    def service(self):
        if current_thread() == main_thread():
            Warning(BlockingIOError("This method will block the entire thread"))

        func = self._function

        try:
            while self.EOBJ is not None:
                func()

        except Exception as ex:
            error("Error in service thread", ex)

    def start(self):
        with self._eobjLock:
            self._eobj = object()
        self._thread.start()

    def stop(self):
        with self._eobjLock:
            self._eobj = None
