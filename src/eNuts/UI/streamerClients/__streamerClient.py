import weakref
from threading import Lock
from typing import Any

import numpy as np
from jAGFx.logger import debug, error
from jAGUI.components.bases import Component
from jAGUI.components.utilities import processMarker
from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QWidget

from ...services import StreamService


@processMarker(True, True)
class StreamerClient(Component, QLabel):
    OnPropertyChanged: Signal = Signal(Any, str, bool, bool)
    OnResolutionChanged: Signal = Signal(int, int)

    def __init__(self, strmr: StreamService, name: str = "", parent: QWidget = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)

        self.setText(f"Loading {strmr.Name}...")
        self._streamerLock: Lock = Lock()
        with self._streamerLock:
            self._streamer: StreamService = strmr
            self._streamer.OnStarted.connect(lambda th: debug(f"Streamer {self._streamer.Name} started"))
            self._streamer.OnFrame.connect(self._showImage)

        def _end():
            self.Stop()

        weakref.ref(self, _end)

    # region [PROPERTIIES]
    @property
    def Streamer(self) -> StreamService:
        with self._streamerLock:
            return self._streamer

    @property
    def ImageSize(self) -> QSize:
        return self._imageSize

    # endregion

    def Start(self):
        with self._streamerLock:
            self._streamer.start()

    def Stop(self):
        with self._streamerLock:
            self._streamer.stop()

    def _showImage(self, frame: np.ndarray):
        if self.IsVisible:
            if frame is not None:
                try:
                    lImage = QImage(
                        frame,
                        frame.shape[1],
                        frame.shape[0],
                        frame.shape[1] * 3,
                        QImage.Format_BGR888,
                    )
                    lPix = QPixmap(lImage)
                    lPix.setDevicePixelRatio(1 / self.Streamer.SizeRatio)
                    self.setPixmap(lPix)
                    self.OnResolutionChanged.emit(lPix.width(), lPix.height())

                except Exception as ex:
                    error("Error converting image...", ex)
