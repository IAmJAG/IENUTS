# VideoThread Documentation

## Overview

The `VideoThread` class is a specialized implementation of the `Streamer` base class designed specifically for video playback operations. It extends the streaming capabilities with video-specific features such as playback control, seeking, media state management, and frame-accurate positioning. The class provides a thread-safe interface for loading, playing, pausing, and seeking through video files using OpenCV's VideoCapture functionality.

**Important**: `VideoThread` inherits from `Streamer` and must be used in conjunction with its base class functionality. It provides additional signals and methods for video playback control beyond the basic streaming operations.

Key features:
- Video file loading and media information extraction
- Playback state management (play, pause, stop, forward, backward)
- Frame-accurate seeking capabilities
- Real-time FPS synchronization with video timing
- Intelligent frame caching for improved performance
- Thread-safe access to video capture operations
- Signal-based communication for playback state changes and media events
- Automatic loop handling and end-of-video detection
- Integration with the base `Streamer` error handling and FPS monitoring

## Class Description

```python
class VideoThread(Streamer):
    # Additional Signals
    OnPlaybackStateChanged: Signal = Signal(ePlaybackState)
    OnMediaLoaded: Signal = Signal(MediaInfo)
    OnMediaStateChanged: Signal = Signal(eMediaState)

    # Properties
    NextFrame: int
    MediaInfo: MediaInfo
    IsSeeking: bool
    SeekRequest: int
    PlaybackState: ePlaybackState
    MediaState: eMediaState

    # Methods
    def __init__(self, options: StreamerOptions = None, cacheOptions: CacheOptions = None)
    def play(self)
    def pause(self)
    def stop(self)
    def setVideoFile(self, filePath: str)
    def seek(self, frameIndex: int)
    def run(self) -> None
    def Stop(self, timeout: float = -1) -> bool

    # Cache Methods
    def EnableCache(self)
    def DisableCache(self)
    def GetCachedFrame(self, frameIndex: int) -> ndarray | None
    def AddToCache(self, frameIndex: int, frame: ndarray)
    def ClearCache(self)
    def UpdateCache(self)
```

## Related Classes and Enums

### ePlaybackState

An `IntFlag` enum representing the various playback states of the video thread.

```python
class ePlaybackState(IntFlag):
    STOPPED = 0x00
    PLAYING = 0x01
    PAUSED = 0x02
    FAST = 0x04
    FORWARD = PLAYING | 0x08
    BACKWARD = PLAYING | 0x10
```

#### States
- **STOPPED**: Video is stopped and positioned at the beginning
- **PLAYING**: Video is currently playing (normal speed)
- **PAUSED**: Video is paused at current position
- **FAST**: Fast playback mode (can be combined with PLAYING)
- **FORWARD**: Forward playback (PLAYING with forward direction)
- **BACKWARD**: Backward playback (PLAYING with backward direction)

### MediaInfo

A serializable class containing information about the loaded media file.

```python
class MediaInfo(Serialisable):
    # Properties
    FPS: float
    FrameCount: int
    Filepath: str

    # Methods
    def getEstimatedDelay(self) -> float
    def resetFPS(self)
```

#### Properties
- **FPS**: Current frames per second rate
- **FrameCount**: Total number of frames in the video
- **Filepath**: Path to the video file

#### Methods
- **getEstimatedDelay()**: Returns the estimated delay between frames (1/FPS)
- **resetFPS()**: Resets FPS to original video FPS

### CacheOptions

A configuration class for VideoThread caching behavior.

```python
class CacheOptions(Serialisable):
    # Properties
    CacheDuration: int  # Total milliseconds to cache around current frame
    TimerInterval: int  # Milliseconds between cache updates
    AverageSeekReadTimeWindow: int  # Milliseconds to keep seek time entries
    TimeSeekDuration: int  # Milliseconds to keep entries in _timeSeeks
```

#### Properties
- **CacheDuration**: Total time in milliseconds to cache frames around current position
- **TimerInterval**: Interval in milliseconds between cache update checks
- **AverageSeekReadTimeWindow**: Time window in milliseconds for averaging seek+read times
- **TimeSeekDuration**: Duration in milliseconds to retain seek time measurements
- **Enabled**: Boolean flag to enable/disable caching functionality (default: True)

### eMediaState

An enum representing the loading state of media.

```python
class eMediaState(Enum):
    LOADED = auto()
    UNLOADED = auto()
```

## Signals

### OnPlaybackStateChanged
- **Type**: `Signal(ePlaybackState)`
- **Description**: Emitted when the playback state changes
- **Parameters**:
  - `state`: The new playback state
- **Usage**: Connect slots to monitor playback state transitions

### OnMediaLoaded
- **Type**: `Signal(MediaInfo)`
- **Description**: Emitted when a video file is successfully loaded
- **Parameters**:
  - `mediaInfo`: Information about the loaded media
- **Usage**: Connect slots to handle media loading completion

### OnMediaStateChanged
- **Type**: `Signal(eMediaState)`
- **Description**: Emitted when the media state changes
- **Parameters**:
  - `state`: The new media state
- **Usage**: Connect slots to monitor media loading/unloading

## Properties

### NextFrame
- **Type**: `int`
- **Description**: The frame index that will be retrieved on the next iteration
- **Access**: Read/write property
- **Thread Safety**: Protected by internal lock

### MediaInfo
- **Type**: `MediaInfo`
- **Description**: Information about the currently loaded media file
- **Access**: Read-only property
- **Returns**: `MediaInfo` object or `None` if no media is loaded

### IsSeeking
- **Type**: `bool`
- **Description**: Indicates whether a seek operation is pending
- **Access**: Read-only property
- **Returns**: `True` if a seek request is active, `False` otherwise

### SeekRequest
- **Type**: `int`
- **Description**: The target frame index for seeking operations
- **Access**: Read/write property
- **Thread Safety**: Protected by internal lock

### PlaybackState
- **Type**: `ePlaybackState`
- **Description**: Current playback state of the video thread
- **Access**: Read/write property
- **Thread Safety**: Protected by internal lock
- **Emits**: `OnPlaybackStateChanged` when value changes

### MediaState
- **Type**: `eMediaState`
- **Description**: Current loading state of the media
- **Access**: Read/write property
- **Thread Safety**: Protected by internal lock
- **Emits**: `OnMediaStateChanged` when value changes

## Methods

### __init__(options: StreamerOptions = None, cacheOptions: CacheOptions = None)
- **Parameters**:
  - `options`: Configuration options for streaming behavior (default None, uses default StreamerOptions)
  - `cacheOptions`: Configuration options for caching behavior (default None, uses default CacheOptions)
- **Description**: Initializes the VideoThread instance with default state and caching
- **Notes**: Sets up internal locks, initializes state variables, cache storage, performance tracking, and timer thread

### play()
- **Description**: Starts or resumes video playback
- **Behavior**: Sets `PlaybackState` to `ePlaybackState.PLAYING`

### pause()
- **Description**: Pauses video playback at current position
- **Behavior**: Sets `PlaybackState` to `ePlaybackState.PAUSED`

### stop()
- **Description**: Stops video playback and resets to beginning
- **Behavior**: Sets `PlaybackState` to `ePlaybackState.STOPPED`

### setVideoFile(filePath: str)
- **Parameters**:
  - `filePath`: Path to the video file to load
- **Description**: Loads a video file for playback
- **Behavior**:
  - Stops current playback and unloads existing media
  - Opens the video file using OpenCV VideoCapture
  - Extracts media information and emits `OnMediaLoaded`
  - Retrieves the first frame and emits it via `OnFrame`
  - Sets media state to `LOADED`
  - Starts the thread if not already running
  - Starts the cache timer thread for background caching
- **Raises**: `Exception` if the video file cannot be opened

### seek(frameIndex: int)
- **Parameters**:
  - `frameIndex`: Target frame index to seek to (0-based)
- **Description**: Requests a seek operation to the specified frame
- **Behavior**: Sets the seek request if the frame index is valid (within bounds)
- **Notes**: The actual seeking occurs in the main loop during the next iteration

### run()
- **Description**: Main thread execution method that handles video playback loop
- **Behavior**:
  - Overrides the base `Streamer.run()` method
  - Defines an internal `_xGetFrame()` function for frame retrieval
  - Handles seeking, playback, and timing synchronization
  - Manages end-of-video looping and state transitions
  - Starts cache timer thread for background caching
  - Calls the base class `run()` method with the custom frame getter
- **Frame Retrieval Logic**:
  - Checks cache first before VideoCapture operations
  - If seeking: Retrieves frame at seek position and clears seek request
  - If playing: Retrieves next frame and advances position
  - Handles end-of-video by looping back to frame 0 and stopping playback
  - Synchronizes playback timing with video FPS using monotonic time
  - Tracks seek and read performance for cache optimization (only non-zero times)
  - Updates _frameTimeTimeLeft for cache timer coordination
- **Notes**: Uses monotonic time for precise timing control, includes intelligent caching, and properly handles exceptions by re-raising them for base class error handling

### GetCachedFrame(frameIndex: int)
- **Parameters**:
  - `frameIndex`: The frame index to retrieve from cache
- **Returns**: `ndarray | None` - The cached frame or None if not cached
- **Description**: Retrieves a frame from the cache if available

### AddToCache(frameIndex: int, frame: ndarray)
- **Parameters**:
  - `frameIndex`: The frame index to cache
  - `frame`: The frame data to cache
- **Description**: Stores a frame in the cache for future retrieval

### ClearCache()
- **Description**: Clears all cached frames and performance tracking data
- **Behavior**: Called automatically when unloading media

### EnableCache()
- **Description**: Enables the caching system at runtime
- **Behavior**: Starts the cache timer thread and enables cache operations if not already enabled

### DisableCache()
- **Description**: Disables the caching system at runtime
- **Behavior**: Stops the cache timer thread and disables cache operations if currently enabled

### UpdateCache()
- **Description**: Caches one frame per call, prioritized by playback direction
- **Behavior**:
  - Calculates cache range around current frame position based on CacheDuration and FPS
  - Prioritizes caching based on BACKWARD/FORWARD playback state
  - Finds next uncached frame in priority direction
  - Caches exactly one frame to avoid blocking
  - Returns early if caching is disabled or no MediaInfo/VideoCapture is available

### Stop(timeout: float = -1) -> bool
- **Parameters**:
  - `timeout`: Timeout value for stopping the thread (default -1, uses base class default)
- **Returns**: `bool` - Success status of stopping operation
- **Description**: Stops the VideoThread and its cache timer thread
- **Behavior**:
  - Stops the cache timer thread if running
  - Calls the base Streamer.Stop() method
  - Returns the result from the base class

## Usage Example

```python
from streamer import StreamerOptions
from vannon.videoThread import VideoThread, ePlaybackState, CacheOptions

# Create VideoThread with custom options
options = StreamerOptions()
options.ExitOnError = True
options.ErrorThreshold = 5

# Configure caching (optional)
cacheOptions = CacheOptions()
cacheOptions.CacheDuration = 15000  # 15 seconds of frames
cacheOptions.TimerInterval = 20     # Check every 20ms
cacheOptions.Enabled = True         # Enable caching (default: True)

videoThread = VideoThread(options, cacheOptions)

# Runtime cache control
videoThread.EnableCache()   # Enable caching
videoThread.DisableCache()  # Disable caching

videoThread = VideoThread(options, cacheOptions)

# Connect to signals
def handle_frame(frame: ndarray, frameId: int):
    print(f"Frame {frameId}: {frame.shape}")

def handle_playback_state(state: ePlaybackState):
    print(f"Playback state: {state}")

def handle_media_loaded(mediaInfo: MediaInfo):
    print(f"Media loaded: {mediaInfo.Filepath}, {mediaInfo.FrameCount} frames at {mediaInfo.FPS} FPS")

videoThread.OnFrame.connect(handle_frame)
videoThread.OnPlaybackStateChanged.connect(handle_playback_state)
videoThread.OnMediaLoaded.connect(handle_media_loaded)

# Load and play video
videoThread.setVideoFile("path/to/video.mp4")
videoThread.play()

# Control playback
videoThread.pause()
videoThread.seek(100)  # Seek to frame 100
videoThread.play()

# Stop and cleanup
videoThread.stop()
videoThread.Stop()  # Stop the streaming thread and cache timer
```

## Dependencies

- `threading.RLock`: For thread-safe access to shared resources
- `threading.Thread`: For background cache timer thread
- `time.monotonic`: For high-precision timing in playback synchronization
- `time.time`: For timestamp tracking in performance measurements
- `time.sleep`: For precise timing control in frame synchronization
- `cv2.VideoCapture`: OpenCV video capture functionality
- `cv2.CAP_PROP_FPS`: For retrieving video FPS
- `cv2.CAP_PROP_FRAME_COUNT`: For retrieving total frame count
- `cv2.CAP_PROP_POS_FRAMES`: For setting/getting current frame position
- `numpy.ndarray`: Frame data type
- `jAGFx.logger.debug`: Logging functionality
- `jAGFx.serializer.Serialisable`: Base serialization class
- `jAGFx.signal.Signal`: Signal-slot communication system
- `streamer.Streamer`: Base streaming class
- `streamer.StreamerOptions`: Streaming configuration
- `vannon.videoThread.CacheOptions`: Cache configuration class
- `vannon.videoThread.MediaInfo`: Media information class
- `vannon.videoThread.eMediaState`: Media state enumeration
- `vannon.videoThread.ePlaybackState`: Playback state enumeration

## Thread Safety

The VideoThread uses multiple RLock objects to ensure thread-safe access to critical sections:
- `_vcapLock`: Protects VideoCapture operations
- `_nextLock`: Protects NextFrame property
- `_seekLock`: Protects seek request operations
- `_playLock`: Protects playback state
- `_mediLock`: Protects media state
- `_cacheLock`: Protects cache operations
- `_frameTimeLock`: Protects _frameTimeTimeLeft access

All property accessors use appropriate locks, and signal emissions are thread-safe through the base Signal implementation.

The class also uses a separate daemon thread for cache management (`_cacheTimer`) that runs in the background to pre-load frames during idle periods. This thread coordinates with the main playback thread using `_frameTimeTimeLeft` to determine when caching is beneficial. The thread is properly cleaned up in the `Stop()` method to prevent resource leaks.

## Implementation Notes

- VideoThread extends the base Streamer functionality with video-specific operations and intelligent caching
- Frame retrieval checks cache first, then falls back to VideoCapture operations with performance tracking
- Playback timing uses monotonic time to ensure consistent frame rates regardless of system load
- End-of-video handling automatically loops back to the beginning and stops playback
- Seek operations are asynchronous and processed in the main loop to avoid blocking
- Media loading emits the first frame immediately after loading for UI responsiveness
- Intelligent caching uses separate timer thread to pre-load frames during idle periods
- Cache prioritizes frames based on playback direction (BACKWARD/FORWARD)
- Performance tracking measures seek+read times (only non-zero values) to optimize cache timing
- Cache range dynamically adjusts based on current frame position
- Runtime enable/disable methods for cache control during operation
- Cache timer thread is properly stopped in Stop() method to prevent resource leaks
- FPS synchronization ensures smooth playback at the video's native frame rate
- Error handling delegates to the base Streamer class for consistent behavior
- The class integrates seamlessly with the existing signal-slot architecture
- Cache timer thread is properly stopped in the Stop() method to prevent resource leaks
