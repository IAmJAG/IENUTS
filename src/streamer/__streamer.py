# ==================================================================================
import weakref

# ==================================================================================
from collections import deque
from threading import RLock, Thread

# ==================================================================================
from time import sleep, time

# ==================================================================================
from numpy import ndarray

# ==================================================================================
from jAGFx.signal import Signal
from utilities import threadRaiseAsync

# ==================================================================================
from .__streamerOptions import StreamerOptions

CMAX_FRAME: int = 1000


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

        self.OnFrame.connect(self._updateFPS)

        weakref.ref(self, lambda: self.Stop(0.01))

    def _updateFPS(self, rawimage: ndarray, frmid: int):
        lCurrentTime = time()
        self._timedFrame.append(lCurrentTime)
        lCutoff = lCurrentTime - self.Options.FPSTimeRange
        while self._timedFrame and self._timedFrame[0] < lCutoff:
            self._timedFrame.popleft()

    def GetFrame(self) -> ndarray:
        self.updateCurrentFrame()
        raise NotImplementedError()

    def run(self) -> None:
        with self._runningLock:
            self._isrunning: bool = True

        lErrors: int = 0
        lSuccesses: int = 0
        try:
            while self.IsRunning and weakref.ref(self):
                try:
                    lFrame: ndarray = self.GetFrame()

                    # Emit only if frame is not None
                    if lFrame is not None:
                        self.OnFrame.emit(lFrame, self.CurrentFrame)

                    lSuccesses += 1
                    if lSuccesses >= self.Options.SuccessThreshold:
                        lErrors = 0
                        lSuccesses = 0
                        self._errorTimes.clear()

                except KeyboardInterrupt:
                    with self._runningLock:
                        self._isrunning: bool = False

                except Exception as ex:
                    self.OnError.emit(ex)

                    lErrors += 1
                    lSuccesses = 0
                    lCurrentTime = time()

                    if len(self._errorTimes) == 0:
                        lCutoff = lCurrentTime - self.Options.ErrorTimeWindow

                    self._errorTimes.append(lCurrentTime)
                    while self._errorTimes and self._errorTimes[0] < lCutoff:
                        self._errorTimes.popleft()

                    if self.Options.ExitOnError and (lErrors >= self.Options.ErrorThreshold or len(self._errorTimes) >= self.Options.ErrorTimeThreshold):
                        return

        except Exception as ex:
            raise ex

        finally:
            self.Stop(0.0001)
            with self._runningLock:
                self._isrunning: bool = False

    def updateCurrentFrame(self):
        self.CurrentFrame += 1
        if self.CurrentFrame > CMAX_FRAME:
            self.ResetFrameId()

    @property
    def CurrentFrame(self) -> int:
        with self._currentLock:
            return self._currentFrame

    @CurrentFrame.setter
    def CurrentFrame(self, value: int):
        with self._currentLock:
            self._currentFrame = value

    def ResetFrameId(self):
        self.CurrentFrame = 0

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
            lOldIdent = self.ident

            sleep(timeout)
            # only attempt to raise if the thread is still alive and the ident didn't change
            if not (self.is_alive() and lOldIdent is not None and self.ident == lOldIdent):
                return
            threadRaiseAsync(self.ident, SystemExit)
