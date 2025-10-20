import numpy as np
from PySide6.QtCore import QSize, Signal

from jAGFx.utilities.names import getRandomNames

from .__QObjectService import Service


class StreamService(Service):
    OnFrame: Signal = Signal(np.ndarray)
    OnResolutionChanged: Signal = Signal(int, int)
    OnError: Signal = Signal(Exception)

    def __init__(self, name: str = "", maxWidth: int = 800) -> None:
        super().__init__()
        self._name: str = getRandomNames() if name.strip().strip else name
        self._resolution: QSize = QSize(0, 0)
        self._maxWidth: int = maxWidth

    def getFrame(self) -> np.ndarray:
        raise NotImplementedError("_getFrame must be overridden in subclasses, this should be one pass process to retrieve the frame")

    def _initService(self):
        raise NotImplementedError("_initService must be overridden in subclasses, this should be one pass process to initialize the service")

    def _cleanUp(self):
        raise NotImplementedError("_cleanUp must be overridden in subclasses, this should be one pass process to clean up the service")

    def _service(self):
        try:
            self._initService()
            super()._service()

        except Exception as ex:
            self.OnError.emit(ex)

        finally:
            self._cleanUp()

    def service(self):
        frame = self.getFrame()
        self.OnFrame.emit(frame)
        if frame is not None and hasattr(frame, "shape"):
            self._setSize(QSize(frame.shape[1], frame.shape[0]))

    def _setSize(self, size: QSize):
        if size != self._resolution:
            self._resolution = size
            self.OnResolutionChanged.emit(self._resolution.width(), self._resolution.height())

    @property
    def Name(self) -> str:
        return self._name

    @property
    def Resolution(self) -> QSize:
        return self._resolution

    @property
    def MaximumWidth(self) -> int:
        return self._maxWidth

    @property
    def SizeRatio(self) -> float:
        return self.MaximumWidth / max(self.Resolution.width(), self.Resolution.height())
