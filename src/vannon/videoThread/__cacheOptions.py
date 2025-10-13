# ==================================================================================

# ==================================================================================
from jAGFx.serializer import Serialisable

# ==================================================================================


class CacheOptions(Serialisable):
    def __init__(self, cacheDuration: int = 20000, timerInterval: int = 10,
                 averageSeekReadTimeWindow: int = 30000, timeSeekDuration: int = 10000,
                 enabled: bool = True):
        super().__init__()
        self._cacheDuration: int = cacheDuration
        self._timerInterval: int = timerInterval
        self._averageSeekReadTimeWindow: int = averageSeekReadTimeWindow
        self._timeSeekDuration: int = timeSeekDuration
        self._enabled: bool = enabled

        self.Properties.append(["CacheDuration", "TimerInterval", "AverageSeekReadTimeWindow", "TimeSeekDuration", "Enabled"])

    @property
    def CacheDuration(self) -> int:
        return self._cacheDuration

    @CacheDuration.setter
    def CacheDuration(self, value: int):
        self._cacheDuration = value

    @property
    def TimerInterval(self) -> int:
        return self._timerInterval

    @TimerInterval.setter
    def TimerInterval(self, value: int):
        self._timerInterval = value

    @property
    def AverageSeekReadTimeWindow(self) -> int:
        return self._averageSeekReadTimeWindow

    @AverageSeekReadTimeWindow.setter
    def AverageSeekReadTimeWindow(self, value: int):
        self._averageSeekReadTimeWindow = value

    @property
    def TimeSeekDuration(self) -> int:
        return self._timeSeekDuration

    @TimeSeekDuration.setter
    def TimeSeekDuration(self, value: int):
        self._timeSeekDuration = value

    @property
    def IsEnabled(self) -> bool:
        return self._enabled

    @IsEnabled.setter
    def IsEnabled(self, value: bool):
        self._enabled = value
