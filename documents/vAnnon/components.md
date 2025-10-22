# vAnnon Core Components

## Tag System

### Tag Class
**Location**: `src/vannon/tags/__tag.py`

**Purpose**: Represents a single annotation tag with hierarchical classification capabilities.

**Key Properties**:
- `Code`: Integer (must be power of 2 for bitwise operations)
- `Text`: String identifier
- `Description`: Optional detailed description

**Validation Rules**:
- Code must be positive integer and power of 2
- Text must be non-empty string
- Unique code and text within collection

**Example**:
```python
tag = Tag(1, "person", "Human being in frame")
tag = Tag(2, "vehicle", "Any type of vehicle")
tag = Tag(4, "animal", "Living creature")
```

### TagCollection Class
**Location**: `src/vannon/tags/__tagCollection.py`

**Purpose**: Manages a collection of tags with persistence and search capabilities.

**Key Features**:
- **Persistence**: JSON-based save/load to `assets/tags/tags.json`
- **Uniqueness**: Enforces unique codes and texts
- **Search**: Find by code, text (partial match), or description
- **Serialization**: Full collection encoding/decoding

**Methods**:
- `Append(tag)`: Add new tag to collection
- `Remove(tag)`: Remove tag from collection
- `FindByCode(code)`: Exact code lookup
- `FindByText(text, caseSensitive=False)`: Text-based search
- `FilterByDescription(keyword)`: Description search
- `GetTagsWithCodes(codes)`: Bulk code lookup

## Bounding Box System

### BoundingBox Class
**Location**: `src/vannon/boundingbox/__boundingBox.py`

**Purpose**: Represents a rectangular annotation region on a video frame.

**Inheritance**: `QRectF` (Qt rectangle) + `Serialisable`

**Key Properties**:
- `Id`: UUID-based unique identifier
- `Class`: String label/classification
- `X, Y`: Top-left coordinates
- `W, H`: Width and height
- `Origin`: Boolean flag for origin tracking
- `Center`: Calculated center point
- `Area`: Calculated area

**Serialization**: JSON-compatible with type metadata.

**Example**:
```python
bbox = BoundingBox("person", QRectF(100, 50, 80, 120))
bbox.Id  # UUID string
bbox.Class  # "person"
bbox.Center  # (140.0, 110.0)
```

## Video Processing System

### VideoThread Class
**Location**: `src/vannon/videoThread/__videoThread.py`

**Purpose**: Handles video file loading, playback, and frame management.

**Inheritance**: `Streamer` (base streaming functionality)

**Key Features**:
- **Video Loading**: OpenCV-based video capture
- **Playback Control**: Play, pause, stop, seek operations
- **Frame Caching**: Performance optimization for seeking
- **State Management**: Complex playback state system
- **Speed Control**: Adjustable playback speed (0.1x to unlimited)
- **Precise Timing**: Timestamp-based frame scheduling for accurate playback

### Playback States
**Location**: `src/vannon/videoThread/__playbackState.py`

**State Flags**:
- `STOPPED`: Video is stopped
- `PLAYING`: Video is playing
- `PAUSED`: Video is paused
- `FAST`: Fast playback mode
- `FORWARD`: Forward direction (combined with PLAYING)
- `BACKWARD`: Backward direction (combined with PLAYING)

**Validation**: Ensures valid state combinations.

### Media States
**Location**: `src/vannon/videoThread/__mediaState.py`

**States**:
- `LOADED`: Media file successfully loaded
- `UNLOADED`: No media file loaded

## User Interface Components

### MainWindow Class
**Location**: `src/vannon/UI/__mainWindow.py`

**Purpose**: Main application window container.

**Inheritance**: `ModernWindow` (jAGUI base)

**Features**:
- Vertical layout with stretch
- Close event handling
- UI setup hooks

### GraphicsView Class
**Location**: `src/vannon/UI/components/__graphicsView.py`

**Purpose**: Custom graphics view for video display and interaction.

**Inheritance**: `QGraphicsView`

**Key Features**:
- **Interactive Drawing**: Mouse-based rectangle creation
- **Canvas Management**: QGraphicsPixmapItem for video frames
- **Pen Customization**: Configurable drawing appearance
- **Event Handling**: Mouse press/move/release for drawing

**Signals**:
- `OnBoxCreated(QRectF)`: Emitted when user draws a rectangle

### MediaView Class
**Location**: `src/vannon/UI/components/__mediaView.py`

**Purpose**: Extends GraphicsView with annotation capabilities.

**Key Features**:
- **Frame Management**: Tracks current frame index
- **Annotation Integration**: Bounding box creation and editing
- **Keyboard Shortcuts**:
  - `Delete`: Remove selected bounding boxes
  - `Ctrl+C`: Copy selected boxes
  - `Ctrl+V`: Paste boxes at cursor
- **Event Filtering**: Global keyboard event handling

**Signals**:
- `OnFrameIndexChanged(int)`: Current frame changed
- `OnItemAdded(int, object)`: New annotation added
- `OnItemUpdate(int, object)`: Annotation modified
- `OnItemRemove(int, str)`: Annotation removed

## Configuration System

### vAnnonConfiguration Class
**Location**: `src/vannon/configuration/__vAnnonConfiguration.py`

**Purpose**: Application-specific configuration management.

**Inheritance**: `ApplicationConfiguration`

**Key Properties**:
- `TagsPath`: Path to tags JSON file
- Standard app properties (Title, Company, AppId, etc.)

**Loading**: Factory function loads from `config/vannon/appconfig.json`

## Contracts and Interfaces

### iTag Protocol
**Location**: `src/vannon/contracts/__tag.py`

**Purpose**: Defines the interface for tag objects.

**Required Properties**:
- `Code: int`
- `Text: str`
- `Description: str` (getter/setter)

### iVideoThread Protocol
**Location**: `src/vannon/contracts/__videoThread.py`

**Purpose**: Defines the interface for video thread implementations.

**Signals**:
- `OnFrame`
- `OnError`
- `OnPlaybackStateChanged`
- `OnMediaLoaded`
- `OnMediaStateChanged`

**Properties**:
- `IsSeeking: bool`
- `SeekRequest: int`
- `PlaybackState: int`
- `MediaState: bool`
- `PlaybackSpeed: float`

**Methods**:
- `play()`, `pause()`, `stop()`, `setVideoFile()`, `start()`, `seek()`, `setPlaybackSpeed()`

## Data Flow Components

### Cache Options
**Location**: `src/vannon/videoThread/__cacheOptions.py`

**Purpose**: Configures frame caching behavior.

**Properties**:
- `IsEnabled`: Enable/disable caching
- `CacheDuration`: How long to cache (milliseconds)
- `TimerInterval`: Cache update frequency

### Media Info
**Location**: `src/vannon/videoThread/__mediaInfo.py`

**Purpose**: Metadata about loaded video file.

**Properties**:
- `FilePath`: Source file path
- `FPS`: Frames per second
- `FrameCount`: Total frames
- `Duration`: Video duration
- `Resolution`: Video dimensions

**Methods**:
- `getEstimatedDelay(speed=1.0)`: Calculate frame timing with optional speed multiplier

## Utility Components

### Streamer Base Class
**Location**: `src/streamer/__streamer.py`

**Purpose**: Base class for streaming operations.

**Features**:
- Thread management
- Frame processing pipeline
- Error handling
- Lifecycle management

### StreamerOptions
**Location**: `src/streamer/__streamerOptions.py`

**Purpose**: Configuration for streamer behavior.

**Properties**:
- Threading options
- Buffer sizes
- Processing parameters

## Integration Points

### Dependency Injection
- **Provider Registration**: Configuration and services registered with DI container
- **Service Resolution**: Components resolve dependencies through `Provider.Resolve()`

### Signal/Slot System
- **Event-driven**: Qt signals for UI updates and data flow
- **Loose Coupling**: Components communicate through signals rather than direct calls

### Serialization Framework
- **jAGFx.Serialisable**: Base class for JSON serialization
- **Type Metadata**: `__type__` field for proper deserialization
- **Property Reflection**: Automatic encoding/decoding of properties

## Error Handling

### Exception Types
- **ValueError**: Invalid tag or bounding box parameters
- **KeyError**: Missing required data during deserialization
- **Exception**: Video loading failures, file access errors

### Logging Integration
- **Centralized Logging**: All components use jAGFx logger
- **Debug Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Context Information**: Caller info and timestamps

## Performance Optimizations

### Frame Caching
- **Temporal Caching**: Cache frames around current position
- **Priority Direction**: Cache in playback direction first
- **Memory Management**: Automatic cleanup of old frames

### Playback Timing
- **Precise Scheduling**: Timestamp-based frame timing prevents drift
- **Speed Adjustment**: Real-time playback speed control without quality loss
- **Processing Compensation**: Timing accounts for frame processing overhead

### UI Responsiveness
- **Thread Separation**: Video processing off UI thread
- **Lazy Updates**: Only update visuals when necessary
- **Efficient Rendering**: Minimize graphics operations

### Memory Management
- **Reference Counting**: Proper cleanup of Qt objects
- **Resource Disposal**: Explicit cleanup in destructors
- **Cache Limits**: Prevent unbounded memory growth
