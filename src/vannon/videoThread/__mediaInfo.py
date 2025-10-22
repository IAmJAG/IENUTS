# ==================================================================================

# ==================================================================================
from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, VideoCapture

# ==================================================================================
from jAGFx.serializer import Serialisable

# ==================================================================================


class MediaInfo(Serialisable):
    def __init__(self, media: VideoCapture, filePath: str) -> None:
        super().__init__()
        self._fps: float = media.get(CAP_PROP_FPS)
        self._ofps: float = media.get(CAP_PROP_FPS)
        self._frameCount: int = media.get(CAP_PROP_FRAME_COUNT)
        self._filePath: str = filePath

        self.Properties.append(["FPS", "FrameCount"])

    def getEstimatedDelay(self, speed: float = 1.0):
        return 1 / (self.FPS * speed if self.FPS > 0 else 60)

    @property
    def FPS(self) -> float:
        return float(self._fps)

    @FPS.setter
    def FPS(self, value: float):
        self._fps = value

    @property
    def FrameCount(self) -> int:
        return int(self._frameCount)

    @property
    def Filepath(self) -> str:
        return self._filePath

    @Filepath.setter
    def Filepath(self, value: str):
        self._filePath = value

    def resetFPS(self):
        self._fps = self._ofps
