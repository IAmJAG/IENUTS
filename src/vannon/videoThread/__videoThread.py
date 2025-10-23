# ==================================================================================
from threading import RLock, Thread
from time import monotonic, sleep, time

# ==================================================================================
from cv2 import CAP_PROP_POS_FRAMES, VideoCapture
from numpy import ndarray

# ==================================================================================
from jAGFx.exceptions import jAGException
from jAGFx.logger import debug
from jAGFx.signal import Signal
from streamer import Streamer, StreamerOptions

# ==================================================================================
from .__cacheOptions import CacheOptions
from .__mediaInfo import MediaInfo
from .__mediaState import eMediaState
from .__playbackState import ePlaybackState


class VideoThread(Streamer):
    OnPlaybackStateChanged: Signal = Signal(ePlaybackState)
    OnMediaLoaded: Signal = Signal(MediaInfo)
    OnMediaStateChanged: Signal = Signal(eMediaState)

    def __init__(self, options: StreamerOptions = None, cacheOptions: CacheOptions = None):
        super().__init__(options)
        self._vcap: VideoCapture = None
        self._mediaInfo: MediaInfo = None

        self._nextFrame: int = 0
        self._seekRequest: int = -1
        self._playbackState: ePlaybackState = ePlaybackState.STOPPED
        self._mediaState: eMediaState = eMediaState.UNLOADED
        self._playbackSpeed: float = 1.0
        self._targetFrameTime: float = 0.0

        # region [CACHE]
        self._cache: dict[int, ndarray] = {}
        self._cacheOptions: CacheOptions = cacheOptions or CacheOptions()
        self._timeSeeks: dict[float, tuple[float, float]] = {}
        self._averageSeekReadTime: float = 0.0
        self._frameTimeTimeLeft: float = 0.0
        self._cacheTimer: Thread = None
        # endregion

        # region [LOCKS]
        self._vcapLock: RLock = RLock()
        self._nextLock: RLock = RLock()
        self._seekLock: RLock = RLock()
        self._playLock: RLock = RLock()
        self._mediLock: RLock = RLock()
        self._cacheLock: RLock = RLock()
        self._frameTimeLock: RLock = RLock()
        self._speedLock: RLock = RLock()
        # endregion

    def updateCurrentFrame(self):
        raise jAGException("Current frame is being managed at _setNextFrame")

    def _getFrame(self, position: int = -1)-> ndarray:
        lFrame: ndarray = None
        lRet: bool = False
        lSeekTime: float = 0.0
        lReadTime: float = 0.0

        # Check cache first (if enabled)
        if position >= 0 and self._cacheOptions.IsEnabled:
            lFrame = self.GetCachedFrame(position)
            if lFrame is not None:
                return lFrame

        with self._vcapLock:
            if self._vcap is not None:
                if int(position) != int(self._vcap.get(CAP_PROP_POS_FRAMES)):
                    lStartSeek = monotonic() * 1000
                    self._vcap.set(CAP_PROP_POS_FRAMES, position)
                    lSeekTime = (monotonic() * 1000) - lStartSeek

                lStartRead = monotonic() * 1000
                lRet, lFrame = self._vcap.read()
                lReadTime = (monotonic() * 1000) - lStartRead

                # Track seek/read times (only non-zero values)
                if lSeekTime > 0 or lReadTime > 0:
                    self._updateAverageSeekReadTime(lSeekTime, lReadTime)

        lFrame = lFrame if lRet else None
        lFrame = None if lFrame is not None and lFrame.ndim == 0 else lFrame

        # Track seek/read times and cache frame (if enabled)
        if self._cacheOptions.IsEnabled:
            # Cache the frame if retrieved
            if lFrame is not None and position >= 0:
                self.AddToCache(position, lFrame)

        return lFrame

    def _setNextFrame(self, current: int = -1):
        self.NextFrame = current if current >= 0 else self.NextFrame

        self.CurrentFrame = self.NextFrame

        if self.PlaybackState & ePlaybackState.BACKWARD == ePlaybackState.BACKWARD:
            self.NextFrame -= 1

        else:
            self.NextFrame += 1

    def run(self) -> None:
        lStartTime = monotonic() * 1000
        debug("[VideoThread]: started")

        def _xGetFrame() -> ndarray:
            nonlocal lStartTime
            lFrame: ndarray = None
            try:
                if self.IsSeeking:
                    lFrame = self._getFrame(self.SeekRequest)
                    self._setNextFrame(self.SeekRequest)
                    self.SeekRequest = -1
                    self._targetFrameTime = monotonic()
                    return lFrame

                else:
                    if self.PlaybackState & ePlaybackState.PLAYING:
                        lFrame = self._getFrame(self.NextFrame)
                        self._setNextFrame()

                        if self.NextFrame >= self.MediaInfo.FrameCount:
                            with self._vcapLock:
                                self._vcap.set(CAP_PROP_POS_FRAMES, 0)
                                self.NextFrame = 0
                                self.ResetFrameId()
                                self.PlaybackState = ePlaybackState.STOPPED

                # Precise timing with target timestamps
                if self._targetFrameTime == 0.0:
                    self._targetFrameTime = monotonic()

                # Calculate frame interval based on speed
                lFrameInterval = self.MediaInfo.getEstimatedDelay(self.PlaybackSpeed)
                self._targetFrameTime += lFrameInterval

                # Sleep until target time
                lCurrentTime = monotonic()
                lSleepDuration = max(0.0, self._targetFrameTime - lCurrentTime)
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
    def FPS(self):
        return self.MediaInfo.FPS

    @property
    def NextFrame(self) -> int:
        with self._nextLock:
            return self._nextFrame

    @NextFrame.setter
    def NextFrame(self, value: int):
        with self._nextLock:
            self._nextFrame = value if value >=0 else 0

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

    @property
    def PlaybackSpeed(self) -> float:
        with self._speedLock:
            return self._playbackSpeed

    def setPlaybackSpeed(self, speed: float):
        with self._speedLock:
            self._playbackSpeed = max(0.1, speed)  # Minimum 0.1x speed
            self._targetFrameTime = monotonic()


    def EnableCache(self):
        if not self._cacheOptions.IsEnabled:
            self._startCacheTimer()
            self._cacheOptions.IsEnabled = True

    def DisableCache(self):
        if self._cacheOptions.IsEnabled:
            self._stopCache()
            self._cacheOptions.IsEnabled = False

    def play(self):
        self.PlaybackState = ePlaybackState.PLAYING

    def pause(self):
        self.PlaybackState = ePlaybackState.PAUSED

    def stopPlayback(self):
        self.PlaybackState = ePlaybackState.STOPPED

    def setVideoFile(self, filePath: str):
        self.PlaybackState = ePlaybackState.STOPPED
        self.MediaState = eMediaState.UNLOADED

        lVidCap: VideoCapture = VideoCapture(filePath)
        if not lVidCap.isOpened():
            raise Exception(f"VideoThread: Could not open video file: {filePath}")

        with self._vcapLock:
            self.ClearCache()  # Clear cache when unloading media
            self._mediaInfo = MediaInfo(lVidCap, filePath)
            self._vcap = lVidCap
            self.NextFrame = 0

            self.OnMediaLoaded.emit(self.MediaInfo)

            lFirstFrame: ndarray = self._getFrame(self.NextFrame)
            if lFirstFrame is not None:
                self.MediaState = eMediaState.LOADED
                self._setNextFrame()
                self.OnFrame.emit(lFirstFrame, self.CurrentFrame)


            if not self.is_alive():
                if self._cacheOptions.IsEnabled:
                    self._startCacheTimer()

                self.start()

    def seek(self, frameIndex: int):
        if 0 <= frameIndex < self.MediaInfo.FrameCount:
            with self._seekLock:
                self._seekRequest = frameIndex
                # Reset timing on seek
                self._targetFrameTime = monotonic()

    def GetCachedFrame(self, frameIndex: int) -> ndarray | None:
        with self._cacheLock:
            return self._cache.get(frameIndex, None)

    def AddToCache(self, frameIndex: int, frame: ndarray):
        with self._cacheLock:
            self._cache[frameIndex] = frame

    def ClearCache(self):
        with self._cacheLock:
            self._cache.clear()
            self._timeSeeks.clear()
            self._averageSeekReadTime = 0.0

    def UpdateCache(self):
        if not self._cacheOptions.IsEnabled or self.MediaInfo is None or self._vcap is None:
            return

        lTotalCacheFrames = int((self._cacheOptions.CacheDuration / 1000) * self.MediaInfo.FPS)
        lCurrentFrame = self.CurrentFrame

        lLeftFrames = min(lTotalCacheFrames // 2, lCurrentFrame)
        lRightFrames = lTotalCacheFrames - lLeftFrames

        lStartFrame = max(0, lCurrentFrame - lLeftFrames)
        lEndFrame = min(self.MediaInfo.FrameCount - 1, lCurrentFrame + lRightFrames)

        # Determine priority direction
        lPriorityDirection = 1  # Default forward
        if self.PlaybackState & ePlaybackState.BACKWARD == ePlaybackState.BACKWARD:
            lPriorityDirection = -1

        # Find next uncached frame in priority direction
        lFrameToCache = -1
        if lPriorityDirection > 0:
            # Forward priority: cache right first
            for lFrame in range(lCurrentFrame + 1, lEndFrame + 1):
                if lFrame not in self._cache:
                    lFrameToCache = lFrame
                    break

            if lFrameToCache == -1:
                # No right frames, cache left
                for lFrame in range(lCurrentFrame - 1, lStartFrame - 1, -1):
                    if lFrame not in self._cache:
                        lFrameToCache = lFrame
                        break
        else:
            # Backward priority: cache left first
            for lFrame in range(lCurrentFrame - 1, lStartFrame - 1, -1):
                if lFrame not in self._cache:
                    lFrameToCache = lFrame
                    break

            if lFrameToCache == -1:
                # No left frames, cache right
                for lFrame in range(lCurrentFrame + 1, lEndFrame + 1):
                    if lFrame not in self._cache:
                        lFrameToCache = lFrame
                        break

        # Cache the frame if found
        if lFrameToCache >= 0:
            lFrame = self._getFrame(lFrameToCache)
            if lFrame is not None:
                self.AddToCache(lFrameToCache, lFrame)

    def _updateAverageSeekReadTime(self, seekTime: int, readTime: int):
        lCurrentTime = time() * 1000
        self._timeSeeks[lCurrentTime] = (seekTime, readTime)

        lCutoffTime = lCurrentTime - self._cacheOptions.TimeSeekDuration

        # Clean old entries
        self._timeSeeks = {k: v for k, v in self._timeSeeks.items() if k >= lCutoffTime}

        if not self._timeSeeks:
            self._averageSeekReadTime = 1000 / self.MediaInfo.FPS if self.MediaInfo else 0.0
            return

        # Calculate average of non-zero seek+read times
        lTotalSeekTime = 0.0
        lSeekCount = 0
        lTotalReadTime = 0.0
        lReadCount = 0
        for lSeekTime, lReadTime in self._timeSeeks.values():

            if lSeekTime > 0:
                lTotalSeekTime += lSeekTime
                lSeekCount += 1

            if lReadTime > 0:
                lTotalReadTime += lReadTime
                lReadCount += 1

        lAvgSeekTime = lTotalSeekTime / lSeekCount if lSeekCount > 0 else 0
        lAvgReadTime = lTotalReadTime / lReadCount if lReadCount > 0 else 0

        self._averageSeekReadTime = lAvgSeekTime + lAvgReadTime if lAvgSeekTime > 0 or lAvgReadTime > 0 else (1000 / self.MediaInfo.FPS if self.MediaInfo else 0.0)

    def _startCacheTimer(self):
        if self._cacheTimer is not None and self._cacheTimer.is_alive():
            return

        def _cacheTimerLoop():
            while self.MediaState == eMediaState.LOADED and self._cacheOptions.IsEnabled:
                with self._frameTimeLock:
                    if self._frameTimeTimeLeft > self._averageSeekReadTime:
                        self.UpdateCache()

                sleep(self._cacheOptions.TimerInterval / 1000)

        debug("starting cache timer")
        self._cacheTimer = Thread(target=_cacheTimerLoop, daemon=True)
        self._cacheTimer.start()
        debug(f"cache timer started ({self._cacheTimer.ident})")

    def _stopCache(self):
        # Stop cache timer
        if self._cacheTimer and self._cacheTimer.is_alive():
            self._cacheTimer.join(0.001)

        self._cacheTimer = None  # Daemon thread will stop with main thread

    def Stop(self, timeout: float = -1):
        self._stopCache()
        return super().Stop(timeout)
