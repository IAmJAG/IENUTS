# ==================================================================================
from jAGFx.configuration import Configuration

__all__ = ["StreamerOptions"]


class StreamerOptions(Configuration):
    def __init__(self):
        super().__init__()
        self._exitOnError: bool = False
        self._errorThreshold: int = 1
        self._errorTimeWindow: float = 60.0
        self._errorTimeThreshold: int = 5
        self._successThreshold: int = 3
        self._fpsTimeRange: float = 60.0

        self.Properties.extend([
            "ExitOnError",
            "ErrorThreshold",
            "ErrorTimeWindow",
            "ErrorTimeThreshold",
            "SuccessThreshold",
            "FPSTimeRange"
        ])

    @property
    def ExitOnError(self) -> bool:
        return self._exitOnError

    @ExitOnError.setter
    def ExitOnError(self, value: bool):
        self._exitOnError = value

    @property
    def ErrorThreshold(self) -> int:
        return self._errorThreshold

    @ErrorThreshold.setter
    def ErrorThreshold(self, value: int):
        self._errorThreshold = value

    @property
    def ErrorTimeWindow(self) -> float:
        return self._errorTimeWindow

    @ErrorTimeWindow.setter
    def ErrorTimeWindow(self, value: float):
        self._errorTimeWindow = value

    @property
    def ErrorTimeThreshold(self) -> int:
        return self._errorTimeThreshold

    @ErrorTimeThreshold.setter
    def ErrorTimeThreshold(self, value: int):
        self._errorTimeThreshold = value

    @property
    def SuccessThreshold(self) -> int:
        return self._successThreshold

    @SuccessThreshold.setter
    def SuccessThreshold(self, value: int):
        self._successThreshold = value

    @property
    def FPSTimeRange(self) -> float:
        return self._fpsTimeRange

    @FPSTimeRange.setter
    def FPSTimeRange(self, value: float):
        self._fpsTimeRange = value
