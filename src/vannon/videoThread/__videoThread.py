# ==================================================================================
from threading import RLock
from time import monotonic, sleep

# ==================================================================================
from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, VideoCapture
from numpy import ndarray

# ==================================================================================
from jAGFx.logger import debug
from jAGFx.serializer import Serialisable
from jAGFx.signal import Signal
from streamer import Streamer, StreamerOptions

# ==================================================================================
from .__mediaInfo import MediaInfo
from .__mediaState import eMediaState
from .__playbackState import ePlaybackState


class VideoThread(Streamer):
    OnPlaybackStateChanged: Signal = Signal(ePlaybackState)
    OnMediaLoaded: Signal = Signal(MediaInfo)
    OnMediaStateChanged: Signal = Signal(eMediaState)

    def __init__(self, options: StreamerOptions = None):
        super().__init__(options)
        self._vcap: VideoCapture = None
        self._mediaInfo: MediaInfo = None

        self._nextFrame: int = -1
        self._seekRequest: int = -1
        self._playbackState: ePlaybackState = ePlaybackState.STOPPED
        self._mediaState: eMediaState = eMediaState.UNLOADED

        # region [LOCKS]
        self._vcapLock: RLock = RLock()
        self._nextLock: RLock = RLock()
        self._seekLock: RLock = RLock()
        self._playLock: RLock = RLock()
        self._mediLock: RLock = RLock()
        # endregion

    def _getFrame(self, position: int = -1):
        lFrame: ndarray = None
        lRet: bool = False
        with self._vcapLock:
            if self._vcap is not None:
                if position  >= 0 and position != self.NextFrame:
                    self._vcap.set(CAP_PROP_POS_FRAMES, position)

                lRet, lFrame = self._vcap.read()

        lFrame = lFrame if lRet else None
        lFrame = None if lFrame is not None and lFrame.ndim == 0 else lFrame

        return lFrame

    def _setNextFrame(self):
        with self._currentLock:
            self._currentFrame = self.NextFrame

        if self.PlaybackState & ePlaybackState.BACKWARD:
            self.NextFrame -= 1

        else:
            self.NextFrame += 1

    def run(self) -> None:
        lStartTime = monotonic() * 1000

        def _xGetFrame() -> ndarray:
            nonlocal lStartTime
            lFrame: ndarray
            try:
                if self.IsSeeking:
                    lFrame = self._getFrame(self.SeekRequest)
                    self._setNextFrame()
                    self.SeekRequest = -1

                else:
                    if self.PlaybackState & ePlaybackState.PLAYING:
                        lFrame = self._getFrame()
                        self._setNextFrame()

                        if self.NextFrame >= self.MediaInfo.FrameCount:
                            with self._vcapLock:
                                self._vcap.set(CAP_PROP_POS_FRAMES, 0)
                                self.NextFrame = 0
                                self.ResetFrameId()
                                self.PlaybackState = ePlaybackState.STOPPED

                lTimeEllapsed: float = (monotonic() * 1000) - lStartTime
                lTimeLeft = (self.MediaInfo.getEstimatedDelay() * 1000) - lTimeEllapsed

                if lTimeLeft > 0:
                    lSleepDuration = max(0.0, lTimeLeft / 1000)
                    sleep(lSleepDuration)

                lStartTime = monotonic() * 1000

                return lFrame

            except Exception as e:
                debug(f"VideoThread: Error in main loop iteration: {e}")
                # must raise here so that streamer may capture the error to trigger error handling logics
                raise e

        self.GetFrame = _xGetFrame

        return super().run()

    @property
    def NextFrame(self) -> int:
        with self._nextLock:
            return self._nextFrame

    @NextFrame.setter
    def NextFrame(self, value: int):
        with self._nextLock:
            self._nextFrame = value

    @property
    def MediaInfo(self) -> MediaInfo:
        return self._mediaInfo

    @property
    def IsSeeking(self) -> bool:
        with self._seekLock:
            return self._seekRequest >= 0

    @property
    def SeekRequest(self) -> int:
        with self._seekLock:
            return self._seekRequest

    @SeekRequest.setter
    def SeekRequest(self, value: int):
        with self._seekLock:
            self._seekRequest = value

    @property
    def PlaybackState(self) -> ePlaybackState:
        with self._playLock:
            return self._playbackState

    @PlaybackState.setter
    def PlaybackState(self, value: ePlaybackState):
        with self._playLock:
            lPPlaybackState: ePlaybackState = self._playbackState
            self._playbackState = value
            if lPPlaybackState != value:
                self.OnPlaybackStateChanged.emit(self._playbackState)

    @property
    def MediaState(self) -> eMediaState:
        with self._mediLock:
            return self._mediaState

    @MediaState.setter
    def MediaState(self, value: eMediaState):
        with self._mediLock:
            lPMediaState: eMediaState = self._mediaState
            self._mediaState = value
            if lPMediaState != value:
                self.OnMediaStateChanged.emit(self._mediaState)

    def play(self):
        self.PlaybackState = ePlaybackState.PLAYING

    def pause(self):
        self.PlaybackState = ePlaybackState.PAUSED

    def stop(self):
        self.PlaybackState = ePlaybackState.STOPPED

    def setVideoFile(self, filePath: str):
        self.PlaybackState = ePlaybackState.STOPPED
        self.MediaState = eMediaState.UNLOADED

        lVidCap: VideoCapture = VideoCapture(filePath)
        if not lVidCap.isOpened():
            raise Exception(f"VideoThread: Could not open video file: {filePath}")

        with self._vcapLock:
            self._mediaInfo = MediaInfo(lVidCap, filePath)
            self._vcap = lVidCap

            self.OnMediaLoaded.emit(self.MediaInfo)

            lFirstFrame: ndarray = self._getFrame(0)
            if lFirstFrame is not None:
                self._setNextFrame()
                self.OnFrame.emit(lFirstFrame, 0)
                self.MediaState = eMediaState.LOADED

            if not self.is_alive():
                self.start()

    def seek(self, frameIndex: int):
        if 0 <= frameIndex < self.MediaInfo.FrameCount:
            with self._seekLock:
                self._seekRequest = frameIndex
