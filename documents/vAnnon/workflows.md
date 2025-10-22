# vAnnon Workflows and Data Flow

## Core Workflows

### 1. Application Startup

```mermaid
flowchart TD
    A[main.py] --> B[loadConfig()]
    B --> C[Set Windows taskbar icon]
    C --> D[Create QApplication]
    D --> E[Load fonts and QSS]
    E --> F[Create MainWindow]
    F --> G[Show window]
    G --> H[Start event loop]
```

**Key Steps**:
1. Load configuration from JSON
2. Configure platform-specific settings (Windows taskbar)
3. Initialize Qt application
4. Load UI resources (fonts, stylesheets)
5. Create and display main window
6. Enter Qt event loop

### 2. Video Loading Workflow

```mermaid
sequenceDiagram
    participant User
    participant MainWindow
    participant VideoThread
    participant MediaView

    User->>MainWindow: Select video file
    MainWindow->>VideoThread: setVideoFile(filePath)
    VideoThread->>VideoThread: VideoCapture(filePath)
    VideoThread->>VideoThread: Extract media info
    VideoThread->>VideoThread: Load first frame
    VideoThread->>MediaView: OnFrame.emit(frame, 0)
    MediaView->>MediaView: Display frame
    VideoThread->>MainWindow: OnMediaLoaded.emit(MediaInfo)
    MainWindow->>User: Update UI with video info
```

**Error Handling**:
- File not found → Exception with descriptive message
- Unsupported format → VideoCapture fails gracefully
- Corrupted file → OpenCV error handling

### 3. Annotation Creation Workflow

```mermaid
flowchart TD
    A[User clicks and drags] --> B[GraphicsView mouse events]
    B --> C[Create temporary rectangle]
    C --> D[Update rectangle on mouse move]
    D --> E[Mouse release]
    E --> F{Valid size?}
    F -->|Yes| G[Emit OnBoxCreated]
    F -->|No| H[Discard rectangle]
    G --> I[MediaView receives signal]
    I --> J[Create BoundingBox]
    I --> K[Add to graphics scene]
    I --> L[Emit OnItemAdded]
```

**Validation Rules**:
- Minimum size: 5x5 pixels
- Must be within frame boundaries
- Snapping to content (future enhancement)

### 4. Playback Control Workflow

```mermaid
stateDiagram-v2
    [*] --> Stopped
    Stopped --> Playing: play()
    Playing --> Paused: pause()
    Paused --> Playing: play()
    Playing --> Stopped: stop()
    Paused --> Stopped: stop()

    Playing --> Seeking: seek()
    Seeking --> Playing: seek complete
```

**State Transitions**:
- **Stopped → Playing**: Start from beginning or current position
- **Playing → Paused**: Freeze current frame
- **Paused → Playing**: Resume from current position
- **Any → Stopped**: Reset to beginning
- **Seeking**: Asynchronous seek operation

## Data Flow Patterns

### Frame Processing Pipeline

```mermaid
graph LR
    A[Video File] --> B[VideoCapture]
    B --> C[Frame Buffer]
    C --> D{Cache Hit?}
    D -->|Yes| E[Cached Frame]
    D -->|No| F[Decode Frame]
    F --> G[Cache Frame]
    E --> H[Display]
    G --> H
    H --> I[Annotation Overlay]
    I --> J[UI Update]
```

### Annotation Data Flow

```mermaid
graph TD
    A[User Input] --> B[GraphicsView]
    B --> C[BoundingBox Creation]
    C --> D[Scene Addition]
    D --> E[Signal Emission]
    E --> F[Annotation Manager]
    F --> G[Data Validation]
    G --> H[Storage/Update]
    H --> I[UI Feedback]
    I --> J[Persistence Layer]
```

## Detailed Component Interactions

### VideoThread Internal Flow

1. **Initialization**:
   - Create VideoCapture instance
   - Extract MediaInfo (FPS, frame count, resolution)
   - Initialize caching system
   - Start background thread

2. **Frame Serving Loop**:
    ```python
    while running:
        if seeking:
            frame = getFrame(seekPosition)
            emit OnFrame(frame, position)
            seeking = False
        elif playing:
            frame = getFrame(nextPosition)
            emit OnFrame(frame, position)
            updateNextPosition()

            # Precise timing with target timestamps
            if targetFrameTime == 0.0:
                targetFrameTime = monotonic()
            frameInterval = mediaInfo.getEstimatedDelay(playbackSpeed)
            targetFrameTime += frameInterval
            sleepDuration = max(0.0, targetFrameTime - monotonic())
            sleep(sleepDuration)
    ```

3. **Caching Logic**:
   - Monitor playback direction
   - Cache frames in priority order
   - Clean up distant frames
   - Track performance metrics

### MediaView Event Handling

1. **Frame Reception**:
   - Clear existing annotations
   - Update current frame index
   - Convert frame to QPixmap
   - Fit view to maintain aspect ratio

2. **Annotation Management**:
   - Track annotations per frame
   - Handle selection and editing
   - Coordinate with graphics scene

3. **User Interaction**:
   - Mouse events for drawing
   - Keyboard shortcuts for operations
   - Context menu for advanced actions

### Tag System Data Flow

```mermaid
graph TD
    A[TagCollection] --> B[Load from JSON]
    B --> C[Validate Tags]
    C --> D[Build Indexes]
    D --> E[Ready for Use]

    F[User Action] --> G{Operation Type}
    G -->|Add| H[Validate Uniqueness]
    G -->|Remove| I[Update Indexes]
    G -->|Search| J[Query Indexes]

    H --> K[Add to Collection]
    I --> L[Remove from Collection]
    J --> M[Return Results]

    K --> N[Save to JSON]
    L --> N
    N --> O[Persist Changes]
```

## Configuration Workflow

### Application Configuration Loading

```mermaid
flowchart TD
    A[Application Start] --> B[LoadCFG()]
    B --> C[Read JSON file]
    C --> D[Parse configuration]
    D --> E[Create vAnnonConfiguration]
    E --> F[Register with Provider]
    F --> G[Available for injection]
```

### Runtime Configuration Updates

```mermaid
flowchart TD
    A[Configuration Change] --> B[Validate new values]
    B --> C[Update in-memory config]
    C --> D[Notify dependent components]
    D --> E[Save to JSON]
    E --> F[Persist changes]
```

## Error Handling and Recovery

### Video Loading Errors

```mermaid
flowchart TD
    A[Load Video] --> B{File exists?}
    B -->|No| C[FileNotFoundError]
    B -->|Yes| D{Valid format?}
    D -->|No| E[UnsupportedFormatError]
    D -->|Yes| F{Readable?}
    F -->|No| G[CorruptionError]
    F -->|Yes| H[Success]
```

### Annotation Errors

```mermaid
flowchart TD
    A[Create Annotation] --> B{Valid position?}
    B -->|No| C[PositionError]
    B -->|Yes| D{Valid size?}
    D -->|No| E[SizeError]
    D -->|Yes| F{Unique ID?}
    F -->|No| G[DuplicateError]
    F -->|Yes| H[Success]
```

## Performance Optimization Workflows

### Frame Caching Strategy

1. **Cache Window Calculation**:
   - Current position ± (cache_duration × FPS / 2)
   - Adjust for playback direction
   - Respect memory limits

2. **Cache Maintenance**:
   - Remove frames outside window
   - Prioritize frequently accessed frames
   - Monitor cache hit rates

3. **Adaptive Caching**:
   - Track seek patterns
   - Adjust cache size based on usage
   - Balance memory vs performance

### UI Responsiveness

1. **Thread Separation**:
   - Video processing in background thread
   - UI updates on main thread
   - Signal-based communication

2. **Lazy Loading**:
   - Load components on demand
   - Cache UI elements
   - Minimize redraws

3. **Efficient Rendering**:
   - Use QPixmap for frame display
   - Minimize graphics item updates
   - Batch UI operations

## Data Export Workflows

### Annotation Export

```mermaid
flowchart TD
    A[Export Request] --> B[Gather all annotations]
    B --> C[Group by frame]
    C --> D[Convert to export format]
    D --> E{Format type}
    E -->|JSON| F[Serialize to JSON]
    E -->|CSV| G[Convert to CSV]
    E -->|Custom| H[Apply custom format]
    F --> I[Write to file]
    G --> I
    H --> I
```

### Tag Export

```mermaid
flowchart TD
    A[Export Tags] --> B[Get TagCollection]
    B --> C[Sort by code]
    C --> D[Format as JSON]
    D --> E[Include metadata]
    E --> F[Write to file]
```

## Integration Workflows

### With eNuts Ecosystem

```mermaid
graph TD
    A[vAnnon] --> B[Shared Configuration]
    A --> C[Common UI Components]
    A --> D[Logging Framework]
    A --> E[Dependency Injection]

    B --> F[eNuts Main App]
    C --> F
    D --> F
    E --> F

    F --> G[Data Exchange]
    G --> H[Annotation Import/Export]
    G --> I[Video Processing]
```

### External Tool Integration

```mermaid
graph TD
    A[vAnnon] --> B[Export Annotations]
    B --> C[Training Pipeline]
    C --> D[ML Model Training]
    D --> E[Model Validation]
    E --> F[Deployed Model]
    F --> G[Automated Annotation]
    G --> A
```

## Lifecycle Management

### Component Initialization

```mermaid
flowchart TD
    A[Application Start] --> B[Initialize DI Container]
    B --> C[Load Configuration]
    C --> D[Create Core Services]
    D --> E[Initialize UI Components]
    E --> F[Connect Signals]
    F --> G[Ready for User Input]
```

### Component Shutdown

```mermaid
flowchart TD
    A[Application Close] --> B[Stop Video Thread]
    B --> C[Save Configuration]
    C --> D[Save Annotations]
    D --> E[Clean Up Resources]
    E --> F[Exit Application]
```

### Memory Management

```mermaid
flowchart TD
    A[Component Creation] --> B[Allocate Resources]
    B --> C[Track References]
    C --> D[Monitor Usage]
    D --> E{Need Cleanup?}
    E -->|Yes| F[Release Resources]
    E -->|No| D
    F --> G[Update Tracking]
```

## Future Workflow Extensions

### Batch Processing

```mermaid
flowchart TD
    A[Batch Request] --> B[Load Video List]
    B --> C[Process Each Video]
    C --> D[Auto-annotate if model available]
    D --> E[Manual review/correction]
    E --> F[Export annotations]
    F --> G[Next video]
    G --> H{Batch complete?}
    H -->|No| C
    H -->|Yes| I[Generate summary report]
```

### Collaborative Annotation

```mermaid
flowchart TD
    A[Multi-user session] --> B[Load shared project]
    B --> C[Lock annotation regions]
    C --> D[Real-time sync]
    D --> E[Conflict resolution]
    E --> F[Save merged annotations]
    F --> G[Session complete]
```

### Automated Assistance

```mermaid
flowchart TD
    A[Frame loaded] --> B[Run detection model]
    B --> C[Generate proposals]
    C --> D[Present to user]
    D --> E[User accepts/rejects/edits]
    E --> F[Update training data]
    F --> G[Model improvement]
