# ==================================================================================
import ctypes
import inspect
from collections import deque
from threading import RLock, Thread

# ==================================================================================
from time import sleep, time

# ==================================================================================
from numpy import ndarray

# ==================================================================================
from jAGFx.signal import Signal

# ==================================================================================
from ..utilities import threadRaiseAsync
from .__streamerOptions import StreamerOptions


class Streamer(Thread):
    OnError: Signal = Signal(Exception)
    OnFrame: Signal = Signal(ndarray, int)

    def __init__(self, options: StreamerOptions = None):
        if self.__class__ == Streamer:
            raise TypeError("Streamer must be subclassed")

        super().__init__()
        self._options = options or StreamerOptions()
        self._timedFrame: deque[float] = deque()
        self._errorTimes: deque[float] = deque()
        self._isrunning: bool = False

        self._currentFrame: int = 0

        self._runningLock: RLock = RLock()
        self._optionsLock: RLock = RLock()
        self._currentLock: RLock = RLock()

        def _updateFPS(ndarray):
            lCurrentTime = time()
            self._timedFrame.append(lCurrentTime)
            lCutoff = lCurrentTime - self.Options.FPSTimeRange
            while self._timedFrame and self._timedFrame[0] < lCutoff:
                self._timedFrame.popleft()

        self.OnFrame.connect(_updateFPS)

    def GetFrame(self) -> ndarray:
        raise NotImplementedError()

    def run(self) -> None:
        with self._runningLock:
            self._isrunning: bool = True

        lErrors: int = 0
        lSuccesses: int = 0

        try:
            while self.IsRunning:
                try:
                    lFrame = self.GetFrame()

                    # Emit only if frame is not None
                    if lFrame: self.OnFrame(lFrame)

                    lSuccesses += 1
                    if lSuccesses >= self.Options.SuccessThreshold:
                        lErrors = 0
                        lSuccesses = 0


                except Exception as ex:
                    self.OnError.emit(ex)

                    lErrors += 1
                    lSuccesses = 0
                    lCurrentTime = time()
                    self._errorTimes.append(lCurrentTime)
                    lCutoff = lCurrentTime - self.Options.ErrorTimeWindow
                    while self._errorTimes and self._errorTimes[0] < lCutoff:
                        self._errorTimes.popleft()

                    if self.Options.ExitOnError and (lErrors >= self.Options.ErrorThreshold or len(self._errorTimes) >= self.Options.ErrorTimeThreshold):
                        return

        except Exception as ex:
            raise ex

        finally:
            with self._runningLock:
                self._isrunning: bool = False

    @property
    def CurrentFrame(self) -> int:
        with self._currentLock:
            return self._currentFrame

    def ResetFrameId(self):
        with self._currentLock:
            self._currentFrame = 0

    @property
    def IsRunning(self) -> bool:
        with self._runningLock:
            return self._isrunning

    @property
    def FPS(self) -> float:
        lCurrentTime = time()
        lCutoff = lCurrentTime - self.Options.FPSTimeRange
        while self._timedFrame and self._timedFrame[0] < lCutoff:
            self._timedFrame.popleft()

        if len(self._timedFrame) < 2: return 0.0
        lDuration = max(lCurrentTime - self._timedFrame[0], 1e-6)
        return len(self._timedFrame) / lDuration

    @property
    def Options(self) -> StreamerOptions:
        with self._optionsLock:
            return self._options

    def Stop(self, timeout: float = -1):
        with self._runningLock:
            self._isrunning = False

        if timeout >= 0:
            if self.is_alive():
                sleep(timeout)
                threadRaiseAsync(self.ident, SystemExit)
