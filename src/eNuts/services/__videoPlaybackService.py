from concurrent.futures import ThreadPoolExecutor
from enum import Enum, auto
from threading import Lock
from time import sleep

from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, VideoCapture
from jAGFx.collections import Buffer
from numpy import ndarray
from PySide6.QtCore import Signal

from .__streamService import StreamService

JAR_NAME: str = "scrcpy-server.jar"
FPS: int = 120
BITRATE: int = 1000000000
MAX_PACKET_RECIEVE: int = 0x10000


class eMediaStatus(Enum):
    NoMedia = auto()
    LoadingMedia = auto()
    LoadedMedia = auto()
    EndOfMedia = auto()


class ePlaybackState(Enum):
    StoppedState = auto()
    PlayingState = auto()
    PausedState = auto()


class VideoStreamingService(StreamService):
    THREADEXECUTOR: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=10)
    OnBuffering: Signal = Signal(float)  # progress 0.0~1.0
    OnMediaStatusChanged: Signal = Signal(eMediaStatus)
    OnPlaybackStateChanged: Signal = Signal(ePlaybackState)
    OnPlaybackProgress: Signal = Signal(float)

    def __init__(self, filePath: str, maxWidth: int = 800) -> None:
        super().__init__(maxWidth=maxWidth)
        self._filePath: str = filePath
        self._buffer: Buffer = None
        self._framepersecond: float = 60.0
        self._orignalFPS: float = 60.0

        self._bufferReadiness: float = 0.1
        self._framecount: int = 0
        self._loadedFrames: int = 0
        self._playbackstate: ePlaybackState = ePlaybackState.StoppedState
        self._currentPosition: int = 0

    def _initService(self):
        def _startBuffering():
            self.OnMediaStatusChanged.emit(self.MediaState)
            lPrevMediaState = self.MediaState

            lCVCapture = VideoCapture(self._filePath)
            if not lCVCapture.isOpened():
                raise IOError(f"Failed to open video file: {self._filePath}")

            self._orignalFPS = lCVCapture.get(CAP_PROP_FPS) or 60.0
            self._framepersecond = self._orignalFPS

            self._framecount = lCVCapture.get(CAP_PROP_FRAME_COUNT)

            self._buffer = Buffer(maxSize=int(self._framecount) if self._framecount > 0 else 128)

            self._loadedFrames = 0

            while lCVCapture.isOpened():
                try:
                    ret, frame = lCVCapture.read()
                    if not ret:
                        raise IOError("Failed to read frame from video file")
                    frame = frame if hasattr(frame, "shape") else frame.__array__()
                    self._buffer.append(frame)
                    self._loadedFrames += 1

                    if lPrevMediaState != self.MediaState:
                        self.OnMediaStatusChanged.emit(self.MediaState)
                        lPrevMediaState = self.MediaState

                    self.OnBuffering.emit(self._loadedFrames / self._framecount)
                except Exception as ex:
                    raise ex

            self.setCurrentPositionByFrameIndex(0)
            if lPrevMediaState != self.MediaState:
                self.OnMediaStatusChanged.emit(self.MediaState)

            lCVCapture.release()

        self.THREADEXECUTOR.submit(_startBuffering)

    def _cleanUp(self): ...

    def getFrame(self) -> ndarray:
        try:
            if self._buffer is None or not hasattr(self, "_currentPosition"):
                return None

            if self._currentPosition < 0 or self._currentPosition >= len(self._buffer):
                raise IndexError("Current position out of buffer range")

            return self._buffer[self._currentPosition]

        except Exception as ex:
            raise ex

        finally:
            if self._currentPosition >= self._buffer.MaximumSize:
                self._currentPosition = 0
            else:
                self._currentPosition += 1

    def service(self):
        if not self.IsPlayable:
            return

        if self._playbackstate != ePlaybackState.PlayingState:
            sleep(0.00001)
            return

        super().service()
        sleep(1 / self._framepersecond)

    @property
    def MediaState(self) -> eMediaStatus:
        if self._buffer is None:
            return eMediaStatus.NoMedia

        if self._loadedFrames < self._framecount:
            return eMediaStatus.LoadingMedia

        if self._currentPosition >= self._framecount:
            return eMediaStatus.EndOfMedia

        return eMediaStatus.LoadedMedia

    def Play(self):
        if not self.IsPlayable:
            return

        self._playbackstate = ePlaybackState.PlayingState
        if not self.isAlive:
            self.start()

        self.OnPlaybackStateChanged.emit(self._playbackstate)

    def Pause(self):
        if not self.IsPlayable:
            return

        self._playbackstate = ePlaybackState.PausedState
        self.OnPlaybackStateChanged.emit(self._playbackstate)

    def Stop(self):
        if not self.IsPlayable:
            return

        self._playbackstate = ePlaybackState.PausedState
        self.OnPlaybackStateChanged.emit(self._playbackstate)

    @property
    def PlaybackState(self) -> ePlaybackState:
        if not self.isAlive:
            return ePlaybackState.StoppedState

        return self._playbackstate

    @property
    def LoaddedFrames(self) -> float:
        return (self._loadedFrames / self._framecount if self._framecount > 0 else 0.0) * 100

    @property
    def IsPlayable(self) -> bool:
        return self.MediaState != eMediaStatus.NoMedia and self.LoaddedFrames >= (self._bufferReadiness * 100)

    def PlaybackReadinessPercentage(self, value: float = 0.1):
        self._bufferReadiness = value

    def setCurrentPositionByFrameIndex(self, position: int):
        if self._framecount > 0:
            self._currentPosition = position
        else:
            self._currentPosition = 0

    def setCurrentPostionByPercentage(self, percentage: float):
        self.setCurrentPositionByFrameIndex(int((percentage / 100) * self._framecount))

    def setCurrentPositionByTimeStamp(self, ms: int):
        self.setCurrentPositionByFrameIndex(int((ms / 1000) * self._framepersecond))

    @property
    def currentPosition(self) -> float:
        return self._currentPosition

    @property
    def FPS(self) -> float:
        return self._framepersecond

    @FPS.setter
    def FPS(self, value: float):
        self._framepersecond = value
