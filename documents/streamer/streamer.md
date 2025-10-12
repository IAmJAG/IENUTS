# Streamer Documentation

## Overview

The `Streamer` class is an abstract base class designed for continuous data streaming operations. It extends Python's `Thread` class and provides a signal-based mechanism for emitting frames and handling errors. The streamer runs in a loop, continuously calling a frame retrieval function and emitting the results through signals, allowing connected slots to process the data asynchronously.

**Important**: `Streamer` must be subclassed and cannot be instantiated directly. Subclasses must implement the `GetFrame()` method to provide specific streaming logic.

Key features:
- Thread-safe operation with signal-slot communication
- Force termination capability for immediate loop stopping
- Configurable error handling with thresholds and time windows
- Enforced subclassing for custom frame retrieval logic
- Windowed FPS calculation over a configurable time range
- Real-time FPS monitoring and updating using efficient deque-based timestamp storage
- Success threshold reset mechanism for error recovery

## Class Description

```python
class Streamer(Thread):
    # Signals
    OnError: Signal = Signal(Exception)
    OnFrame: Signal = Signal(ndarray)

    # Properties
    IsRunning: bool
    FPS: float

    # Methods
    def __init__(self, options: StreamerOptions = None)
    def GetFrame(self) -> ndarray
    def run(self) -> None
    def Stop(self, timeout: float = -1)
```

## StreamerOptions

The `StreamerOptions` class provides configuration options for error handling and recovery behavior in the streamer.

```python
class StreamerOptions(Configuration):
    # Properties
    ExitOnError: bool
    ErrorThreshold: int
    ErrorTimeWindow: float
    ErrorTimeThreshold: int
    SuccessThreshold: int
    FPSTimeRange: float
```

### Properties

#### ExitOnError
- **Type**: `bool`
- **Default**: `False`
- **Description**: Whether the streamer should exit when error thresholds are exceeded

#### ErrorThreshold
- **Type**: `int`
- **Default**: `1`
- **Description**: Number of consecutive errors that trigger exit (when `ExitOnError` is `True`)

#### ErrorTimeWindow
- **Type**: `float`
- **Default**: `60.0`
- **Description**: Time window in seconds for counting errors

#### ErrorTimeThreshold
- **Type**: `int`
- **Default**: `5`
- **Description**: Number of errors within the time window that trigger exit (when `ExitOnError` is `True`)

#### SuccessThreshold
- **Type**: `int`
- **Default**: `3`
- **Description**: Number of consecutive successful frames that reset the error counter

#### FPSTimeRange
- **Type**: `float`
- **Default**: `60.0`
- **Description**: Time window in seconds for FPS calculation

## Signals

### OnError
- **Type**: `Signal(Exception)`
- **Description**: Emitted when an exception occurs during frame processing
- **Parameters**:
  - `exception`: The exception object that was raised
- **Usage**: Connect error handling slots to this signal to manage streaming failures

### OnFrame
- **Type**: `Signal(ndarray)`
- **Description**: Emitted for each successfully retrieved frame
- **Parameters**:
  - `frame`: The frame data as a numpy ndarray
- **Usage**: Connect frame processing slots to this signal to handle incoming frame data

## Properties

### IsRunning
- **Type**: `bool`
- **Description**: Indicates whether the streamer thread is currently running
- **Access**: Read-only property
- **Returns**: `True` if the thread is active and the internal running flag is set, `False` otherwise

### FPS
- **Type**: `float`
- **Description**: Current frames per second rate, calculated as a moving average over the configured time window
- **Access**: Read-only property
- **Returns**: The average FPS over the last `FPSTimeRange` seconds, or 0.0 if fewer than 2 frames

## Methods

### __init__(options: StreamerOptions = None)
- **Parameters**:
  - `options`: Configuration options for error handling and recovery (default None, creates default StreamerOptions)
- **Description**: Initializes the Streamer instance with error handling configuration
- **Notes**: Sets the internal running flag to `True`, initializes timestamp deques for FPS (configured time window) and error tracking, and connects FPS update handler to OnFrame signal

### run()
- **Description**: Main thread execution method that runs the streaming loop with error handling and recovery
- **Behavior**:
  - Sets the running flag to `True`
  - Enters a continuous loop while `IsRunning` is `True`
  - Calls the `GetFrame()` method to retrieve frame data
  - Emits the `OnFrame` signal with the retrieved frame (FPS is updated automatically via signal connection)
  - Tracks consecutive successes and resets error counters when success threshold is reached
  - Catches and emits any exceptions via `OnError` signal
  - Tracks errors within time windows and counts consecutive errors
  - Exits the loop if `ExitOnError` is enabled and error thresholds are exceeded
- **Error Handling Logic**:
  - Consecutive errors are counted and compared against `ErrorThreshold`
  - Errors within the `ErrorTimeWindow` are tracked and compared against `ErrorTimeThreshold`
  - If either threshold is exceeded and `ExitOnError` is `True`, the streamer stops
  - Consecutive successes reset the error counters when `SuccessThreshold` is reached
- **Notes**: Subclasses must override the `GetFrame()` method to provide actual streaming logic

### Stop(timeout: float = -1)
- **Description**: Terminates the streaming loop, optionally with a timeout for force termination
- **Parameters**:
  - `timeout`: Timeout in seconds before force termination (-1 for no force termination)
- **Behavior**:
  - Sets the internal running flag to `False`
  - If timeout >= 0 and thread is alive, waits for timeout then raises `SystemExit` to force termination
- **Notes**: Uses low-level thread interruption for guaranteed immediate stopping when timeout is specified

## Subclassing Example

Since `Streamer` must be subclassed, here's an example of creating a custom streamer:

```python
from streamer import Streamer, StreamerOptions
from numpy import ndarray
import cv2  # Example for video streaming
from time import sleep

class VideoStreamer(Streamer):
    def __init__(self, video_path: str, options: StreamerOptions = None):
        super().__init__(options)
        self._video_path = video_path
        self._cap = cv2.VideoCapture(video_path)

    def GetFrame(self) -> ndarray:
        ret, frame = self._cap.read()
        if not ret:
            return None  # End of video
        return frame

    def run(self) -> None:
        with self._runningLock:
            self._isrunning = True

        while self.IsRunning:
            try:
                frame = self.GetFrame()
                if frame is not None:
                    self.OnFrame.emit(frame)
                    sleep(1/30.0)  # Example: limit to 30 FPS
                else:
                    break  # End of stream
            except Exception as ex:
                self.OnError.emit(ex)

# Usage with custom options
options = StreamerOptions()
options.ExitOnError = True
options.ErrorThreshold = 5
options.SuccessThreshold = 10
options.FPSTimeRange = 30.0  # 30-second FPS window

streamer = VideoStreamer(video_path="video.mp4", options=options)

# Connect to signals
def handle_frame(frame: ndarray):
    print(f"Received frame: {frame.shape}")

def handle_error(error: Exception):
    print(f"Streaming error: {error}")

streamer.OnFrame.connect(handle_frame)
streamer.OnError.connect(handle_error)

# Start streaming
streamer.start()

# Check FPS
print(f"Current FPS: {streamer.FPS}")

# Stop streaming
streamer.Stop()
```

## Dependencies

- `threading.Thread`: Base threading functionality
- `collections.deque`: Efficient timestamp storage for FPS and error tracking
- `numpy.ndarray`: Frame data type
- `jAGFx.signal.Signal`: Signal-slot communication system
- `jAGFx.configuration.Configuration`: Base configuration class for StreamerOptions
- `ctypes`, `inspect`: For thread interruption functionality
- `time`: For timestamping, FPS calculation, and error time windows

## Thread Safety

The Streamer uses signals for communication, which provide thread-safe emission. The `Stop()` method uses low-level thread interruption, which should be used carefully to avoid resource leaks or inconsistent states.

## Implementation Notes

- The base implementation includes placeholder code (`GetFrame()` raises `NotImplementedError`)
- FPS is calculated as a moving average over the configured time window using efficient deque operations
- Error handling captures all exceptions during frame processing with configurable thresholds
- Success threshold mechanism allows automatic error counter reset after successful recovery
- Time-windowed error tracking prevents false positives from sporadic errors
- Force termination uses `SystemExit` exception injection for immediate thread stopping when timeout is specified
- Thread-safe access to `_isrunning` using RLock
- FPS calculation is O(1) amortized per frame for optimal performance
- Error tracking uses efficient deque operations for time-windowed counting
