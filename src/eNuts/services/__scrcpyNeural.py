# ==================================================================================
from .__scrcpyStreamService import SCRCPYStreamService


class CVNeural(SCRCPYStreamService):
    def start(self, *param):
        self.OnStarted.connect(self._onStarted)
        super().start(*param)

    def _onStarted(self):
        ...
