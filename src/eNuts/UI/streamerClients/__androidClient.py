import weakref
from threading import Lock
from typing import Any

import numpy as np
from jAGFx.logger import error
from jAGUI.components.bases import Component
from jAGUI.components.utilities import processMarker
from PySide6.QtCore import Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QWidget

from ...services import AndroidStreamer


@processMarker(True, True)
class AndroidClient(Component, QLabel):
    onResize: Signal = Signal(int, int)
    onImage: Signal = Signal(np.ndarray)
    OnPropertyChanged: Signal = Signal(Any, str, bool, bool)

    def __init__(self, strmr: AndroidStreamer, name: str = "", parent: QWidget = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)

        self.setText(f"Loading {strmr.Title}...")
        self._streamerLock: Lock = Lock()

        def _onFrame(frame: np.ndarray):
            try:
                self.onImage.emit(frame)

            except RuntimeError:
                pass

            except Exception as ex:
                error("Exception on emitting image", ex)

        with self._streamerLock:
            self._streamer: AndroidStreamer = strmr
            self._streamer.setOnFrame(_onFrame)
            self.onImage.connect(self._showImage)

        def _end():
            self.StopSteam()

        weakref.ref(self, _end)

    # region [PROPERTIIES]
    @property
    def Streamer(self) -> AndroidStreamer:
        with self._streamerLock:
            return self._streamer

    # endregion

    def Start(self):
        with self._streamerLock:
            self.setText("Starting...")
            self._streamer.start()

    def Stop(self):
        with self._streamerLock:
            self._streamer.stop()

    def _showImage(self, frame: np.ndarray):
        lCanContinue = not (QApplication.instance() is None or not self.IsVisible)

        if not lCanContinue:
            return

        QApplication.instance().processEvents()
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
                self.onResize.emit(*self.Streamer.Resolution)

            except Exception as ex:
                error("Error converting image...", ex)
