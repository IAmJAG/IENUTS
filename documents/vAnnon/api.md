# vAnnon API Reference

## Core Classes

### Tag

**Location**: `src/vannon/tags/__tag.py`

#### Constructor Overloads

```python
Tag()  # Empty tag
Tag(code: int, text: str)  # With code and text
Tag(code: int, text: str, description: str)  # Full initialization
Tag(dct: dict)  # From dictionary (deserialization)
```

#### Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `Code` | `int` | Read-only | Unique power-of-2 identifier |
| `Text` | `str` | Read-only | Human-readable identifier |
| `Description` | `str` | Read/Write | Detailed description |

#### Validation Rules

- **Code**: Must be positive integer and power of 2 (1, 2, 4, 8, 16, etc.)
- **Text**: Non-empty string, unique within collection
- **Description**: Optional string

#### Example

```python
# Create tags
person_tag = Tag(1, "person", "Human being")
vehicle_tag = Tag(2, "vehicle", "Any motorized vehicle")

# Access properties
print(person_tag.Code)  # 1
print(person_tag.Text)  # "person"
person_tag.Description = "A human individual"
```

### TagCollection

**Location**: `src/vannon/tags/__tagCollection.py`

#### Constructor Overloads

```python
TagCollection()  # Empty collection
TagCollection(dct: dict)  # From dictionary
TagCollection(tags: list)  # From list of tags
TagCollection(tags: tuple)  # From tuple of tags
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `Append` | `tag: iTag` | `None` | Add tag to collection |
| `Remove` | `tag: iTag` | `None` | Remove tag from collection |
| `Clear` | - | `None` | Remove all tags |
| `Save` | - | `None` | Save to configured path |
| `Load` | - | `None` | Load from configured path |
| `FindByCode` | `code: int` | `Optional[iTag]` | Find tag by exact code |
| `FindByText` | `text: str, caseSensitive: bool = False` | `list[iTag]` | Find tags containing text |
| `FilterByDescription` | `keyword: str, caseSensitive: bool = False` | `list[iTag]` | Find tags by description |
| `GetTagsWithCodes` | `codes: list[int]` | `list[iTag]` | Get tags matching codes |

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| Length | `int` | Number of tags in collection |

#### Example

```python
collection = TagCollection()

# Add tags
person = Tag(1, "person")
vehicle = Tag(2, "vehicle")
collection.Append(person)
collection.Append(vehicle)

# Search
found = collection.FindByText("person")  # [person]
by_codes = collection.GetTagsWithCodes([1, 2])  # [person, vehicle]

# Persistence
collection.Save()  # Saves to config.TagsPath
collection.Load()  # Loads from config.TagsPath
```

### BoundingBox

**Location**: `src/vannon/boundingbox/__boundingBox.py`

#### Constructor Overloads

```python
BoundingBox(klass: str, rect: QRectF, id: str = None)  # Standard
BoundingBox(dct: dict)  # From dictionary
```

#### Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `Id` | `str` | Read-only | UUID-based unique identifier |
| `Class` | `str` | Read/Write | Classification label |
| `Origin` | `bool` | Read/Write | Origin tracking flag |
| `X` | `float` | Read-only | Left coordinate |
| `Y` | `float` | Read-only | Top coordinate |
| `W` | `float` | Read-only | Width |
| `H` | `float` | Read-only | Height |
| `Center` | `tuple[float, float]` | Read-only | Center coordinates |
| `Area` | `int` | Read-only | Area in pixels |

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `toTuple` | - | `tuple[int, int, int, int]` | Convert to (x, y, w, h) |

#### Example

```python
from PySide6.QtCore import QRectF

# Create bounding box
bbox = BoundingBox("person", QRectF(100, 50, 80, 120))
print(bbox.Id)  # UUID string
print(bbox.Class)  # "person"
print(bbox.Center)  # (140.0, 110.0)
print(bbox.Area)  # 9600

# Modify
bbox.Class = "adult"
bbox.Origin = True
```

### VideoThread

**Location**: `src/vannon/videoThread/__videoThread.py`

#### Constructor

```python
VideoThread(options: StreamerOptions = None, cacheOptions: CacheOptions = None)
```

#### Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `NextFrame` | `int` | Read/Write | Next frame to process |
| `MediaInfo` | `MediaInfo` | Read-only | Video metadata |
| `IsSeeking` | `bool` | Read-only | Whether seek operation in progress |
| `SeekRequest` | `int` | Read/Write | Requested seek position |
| `PlaybackState` | `ePlaybackState` | Read/Write | Current playback state |
| `MediaState` | `eMediaState` | Read/Write | Current media state |

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `play` | - | `None` | Start/resume playback |
| `pause` | - | `None` | Pause playback |
| `stop` | - | `None` | Stop playback |
| `setVideoFile` | `filePath: str` | `None` | Load video file |
| `seek` | `frameIndex: int` | `None` | Seek to frame |
| `EnableCache` | - | `None` | Enable frame caching |
| `DisableCache` | - | `None` | Disable frame caching |
| `GetCachedFrame` | `frameIndex: int` | `ndarray \| None` | Get cached frame |
| `AddToCache` | `frameIndex: int, frame: ndarray` | `None` | Cache frame |
| `ClearCache` | - | `None` | Clear all cached frames |

#### Signals

| Signal | Parameters | Description |
|--------|------------|-------------|
| `OnPlaybackStateChanged` | `ePlaybackState` | Playback state changed |
| `OnMediaLoaded` | `MediaInfo` | Media file loaded |
| `OnMediaStateChanged` | `eMediaState` | Media state changed |

#### Example

```python
video_thread = VideoThread()

# Load video
video_thread.setVideoFile("path/to/video.mp4")

# Control playback
video_thread.play()
video_thread.pause()
video_thread.seek(100)  # Jump to frame 100

# Check state
if video_thread.PlaybackState & ePlaybackState.PLAYING:
    print("Video is playing")

# Cache management
video_thread.EnableCache()
frame = video_thread.GetCachedFrame(50)
```

### MediaView

**Location**: `src/vannon/UI/components/__mediaView.py`

#### Constructor

```python
MediaView(vt: VideoThread, parent=None)
```

#### Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `FrameIndex` | `int` | Read/Write | Current frame index |
| `RawImage` | `cv.Mat` | Read-only | Current frame as ndarray |
| `Clipboard` | `list[QRectF]` | Read-only | Copied bounding boxes |

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `Load` | - | `None` | Initialize view |
| `setupUI` | `layout: QBoxLayout = None` | `None` | Setup UI components |
| `ProcessImage` | `frame: ndarray` | `QPixmap` | Convert frame to pixmap |
| `AddGraphicItem` | `rect: QRectF` | `BoundingBox` | Add bounding box |
| `selectGraphicsItemById` | `bboxId: str` | `None` | Select bounding box by ID |

#### Signals

| Signal | Parameters | Description |
|--------|------------|-------------|
| `OnFrameIndexChanged` | `int` | Current frame changed |
| `OnItemAdded` | `int, object` | Annotation added (frame_index, bbox) |
| `OnItemUpdate` | `int, object` | Annotation updated (frame_index, bbox) |
| `OnItemRemove` | `int, str` | Annotation removed (frame_index, bbox_id) |

#### Example

```python
media_view = MediaView(video_thread)

# Handle frame changes
def on_frame_changed(frame_idx):
    print(f"Current frame: {frame_idx}")

media_view.OnFrameIndexChanged.connect(on_frame_changed)

# Handle annotations
def on_annotation_added(frame_idx, bbox):
    print(f"Added bbox at frame {frame_idx}: {bbox.Class}")

media_view.OnItemAdded.connect(on_annotation_added)
```

### GraphicsView

**Location**: `src/vannon/UI/components/__graphicsView.py`

#### Constructor

```python
GraphicsView(parent=None)
```

#### Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `Canvas` | `QGraphicsPixmapItem` | Read-only | Video display canvas |
| `DrawingEnabled` | `bool` | Read/Write | Enable rectangle drawing |

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `setDrawingPen` | `color: QColor, lineWidth: int = 2, style: Qt.PenStyle = Qt.PenStyle.DotLine` | `None` | Configure drawing appearance |

#### Signals

| Signal | Parameters | Description |
|--------|------------|-------------|
| `OnBoxCreated` | `QRectF` | User created rectangle |

#### Example

```python
graphics_view = GraphicsView()

# Enable drawing
graphics_view.DrawingEnabled = True

# Configure pen
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
graphics_view.setDrawingPen(QColor("red"), 3, Qt.PenStyle.SolidLine)

# Handle drawing
def on_box_created(rect):
    print(f"Created box: {rect}")

graphics_view.OnBoxCreated.connect(on_box_created)
```

## Configuration Classes

### vAnnonConfiguration

**Location**: `src/vannon/configuration/__vAnnonConfiguration.py`

#### Properties

| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `TagsPath` | `str` | Read/Write | Path to tags JSON file |

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `LoadCFG` | `path: str = DB_CONFIG_PATH` | `vAnnonConfiguration` | Load from JSON |

#### Example

```python
from jAGFx.dependencyInjection import Provider
from jAGFx.configuration import iConfiguration

# Get configuration
config = Provider.Resolve(iConfiguration)
print(config.TagsPath)  # ".\\assets\\tags\\tags.json"
```

## Enums and Constants

### ePlaybackState

**Location**: `src/vannon/videoThread/__playbackState.py`

| Value | Description |
|-------|-------------|
| `STOPPED = 0x00` | Video stopped |
| `PLAYING = 0x01` | Video playing |
| `PAUSED = 0x02` | Video paused |
| `FAST = 0x04` | Fast playback |
| `FORWARD = PLAYING \| 0x08` | Forward playback |
| `BACKWARD = PLAYING \| 0x10` | Backward playback |

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `IsValid` | `state: ePlaybackState` | `bool` | Validate state combination |

### eMediaState

**Location**: `src/vannon/videoThread/__mediaState.py`

| Value | Description |
|-------|-------------|
| `LOADED` | Media file loaded |
| `UNLOADED` | No media loaded |

## Protocols/Interfaces

### iTag

**Location**: `src/vannon/contracts/__tag.py`

**Required Properties**:
- `Code: int`
- `Text: str`
- `Description: str` (getter/setter)

### iVideoThread

**Location**: `src/vannon/contracts/__videoThread.py`

**Required Signals**:
- `OnFrame`
- `OnError`
- `OnPlaybackStateChanged`
- `OnMediaLoaded`
- `OnMediaStateChanged`

**Required Properties**:
- `IsSeeking: bool`
- `SeekRequest: int`
- `PlaybackState: int`
- `MediaState: bool`

**Required Methods**:
- `play()`
- `pause()`
- `stop()`
- `setVideoFile(filePath: str)`
- `start()`
- `seek(frameIndex: int)`

## Utility Classes

### MediaInfo

**Location**: `src/vannon/videoThread/__mediaInfo.py`

**Properties**:
- `FilePath: str`
- `FPS: float`
- `FrameCount: int`
- `Duration: float`
- `Resolution: tuple[int, int]`

**Methods**:
- `getEstimatedDelay(): float`

### CacheOptions

**Location**: `src/vannon/videoThread/__cacheOptions.py`

**Properties**:
- `IsEnabled: bool`
- `CacheDuration: int` (milliseconds)
- `TimerInterval: float` (seconds)
- `TimeSeekDuration: int` (milliseconds)

## Usage Examples

### Complete Annotation Workflow

```python
from jAGFx.dependencyInjection import Provider
from jAGFx.configuration import iConfiguration
from vannon.tags import TagCollection
from vannon.videoThread import VideoThread
from vannon.UI.components import MediaView
from PySide6.QtCore import QRectF

# Setup
config = Provider.Resolve(iConfiguration)
tags = TagCollection()
tags.Load()

video_thread = VideoThread()
media_view = MediaView(video_thread)

# Load video
video_thread.setVideoFile("sample.mp4")

# Create annotation
rect = QRectF(100, 50, 80, 120)
bbox = media_view.AddGraphicItem(rect)
bbox.Class = "person"

# Save work
# (annotations would be saved through a manager class)
```

### Tag Management

```python
from vannon.tags import Tag, TagCollection

# Create collection
tags = TagCollection()

# Add tags
person = Tag(1, "person", "Human being")
car = Tag(2, "car", "Automobile")
bike = Tag(4, "bike", "Bicycle")

tags.Append(person)
tags.Append(car)
tags.Append(bike)

# Search
people = tags.FindByText("person")  # [person]
vehicles = tags.GetTagsWithCodes([2, 4])  # [car, bike]

# Persist
tags.Save()
```

### Video Playback Control

```python
from vannon.videoThread import VideoThread, ePlaybackState

video = VideoThread()

# Load and play
video.setVideoFile("video.mp4")
video.play()

# Control playback
video.pause()
video.seek(500)  # Jump to frame 500
video.play()

# Check state
if video.PlaybackState == ePlaybackState.PLAYING:
    print("Playing normally")
elif video.PlaybackState & ePlaybackState.FAST:
    print("Fast playback")
```

## Error Handling

### Common Exceptions

| Exception | Context | Handling |
|-----------|---------|----------|
| `ValueError` | Invalid tag parameters | Validate input before creation |
| `KeyError` | Missing deserialization data | Check JSON structure |
| `Exception` | Video loading failure | Check file path and format |
| `AttributeError` | Missing configuration | Ensure proper initialization |

### Best Practices

```python
try:
    # Tag operations
    tag = Tag(code, text, description)
    collection.Append(tag)
except ValueError as e:
    print(f"Invalid tag: {e}")

try:
    # Video operations
    video_thread.setVideoFile(file_path)
except Exception as e:
    print(f"Video load failed: {e}")

try:
    # Configuration
    config = Provider.Resolve(iConfiguration)
except Exception as e:
    print(f"Configuration error: {e}")
