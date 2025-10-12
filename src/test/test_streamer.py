# ==================================================================================
import time
import unittest

# ==================================================================================
import numpy as np

# ==================================================================================
from streamer import Streamer, StreamerOptions


class MockStreamer(Streamer):
    def __init__(self, fpsTimeRange: float = 60, options: StreamerOptions = None, frameDelay: float = 0.1):
        super().__init__(fpsTimeRange, options)
        self._frameDelay = frameDelay
        self._frameCount = 0

    def GetFrame(self) -> np.ndarray:
        time.sleep(self._frameDelay)
        self._frameCount += 1
        return np.zeros((10, 10), dtype=np.uint8)


class TestStreamer(unittest.TestCase):
    def test_performance(self):
        lOptions = StreamerOptions()
        lOptions.ExitOnError = False
        lStreamer = MockStreamer(options=lOptions, frameDelay=0.01)  # fast frames

        lStreamer.start()
        time.sleep(1.0)  # run for 1 second
        lFps = lStreamer.FPS
        lStreamer.Stop()

        self.assertGreater(lFps, 50, "FPS should be high for fast frames")

    def test_responsiveness(self):
        lStreamer = MockStreamer(frameDelay=0.1)

        lStartTime = time.time()
        lStreamer.start()
        lStartDuration = time.time() - lStartTime
        self.assertLess(lStartDuration, 0.01, "Start should be responsive")

        time.sleep(0.5)  # let it run a bit
        lStopTime = time.time()
        lStreamer.Stop()
        lStopDuration = time.time() - lStopTime
        self.assertLess(lStopDuration, 0.01, "Stop should be responsive")

    def test_force_stop(self):
        lStreamer = MockStreamer(frameDelay=1.0)  # slow frames

        lStreamer.start()
        time.sleep(0.1)  # let it start

        lStopTime = time.time()
        lStreamer.Stop(timeout=0.5)  # force stop after 0.5s
        lStopDuration = time.time() - lStopTime

        self.assertLess(lStopDuration, 1.0, "Force stop should be quick")
        self.assertFalse(lStreamer.IsRunning, "Streamer should not be running after force stop")

def main():
    unittest.main()


if __name__ == '__main__':
    main()
