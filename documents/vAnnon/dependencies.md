# vAnnon Dependencies and Libraries

## Core Dependencies

### PySide6 (Qt for Python)
**Purpose**: GUI framework and application foundation
**Version**: 6.x
**Key Components Used**:
- `QApplication`: Main application loop
- `QWidget`: Base UI components
- `QGraphicsView/QGraphicsScene`: Canvas for video display
- `QRectF/QRect`: Rectangle geometry
- `QPixmap`: Image display
- `Signal`: Event system
- `QBoxLayout`: Layout management

**Integration Points**:
- Main window and UI components
- Graphics rendering
- Event handling
- Threading (QThread base classes)

### OpenCV (cv2)
**Purpose**: Video processing and computer vision
**Version**: 4.x
**Key Components Used**:
- `VideoCapture`: Video file reading
- `CAP_PROP_*`: Video properties (FPS, frame count, etc.)
- `ndarray`: Frame data structure
- Image processing functions

**Integration Points**:
- Video file loading and frame extraction
- Frame buffering and caching
- Raw image data handling

### NumPy
**Purpose**: Numerical computing for image data
**Version**: 1.x
**Key Components Used**:
- `ndarray`: Multi-dimensional arrays for frame data
- Array operations and manipulations

**Integration Points**:
- Frame data storage and processing
- Image format conversions

## Framework Dependencies

### jAGFx Framework
**Purpose**: Custom application framework
**Components Used**:

#### Configuration System
- `ApplicationConfiguration`: Base config class
- `LoggerConfig`: Logging configuration
- `iConfiguration`: Configuration interface

#### Dependency Injection
- `Provider`: Service locator pattern
- `iDependent`: Dependency interface

#### Logging
- `debug()`, `info()`, `warning()`, `error()`: Logging functions
- Centralized logging with configurable levels

#### Serialization
- `Serialisable`: Base serialization class
- `jsonDecode()`: JSON deserialization
- Automatic property encoding/decoding

#### Overload System
- `OverloadDispatcher`: Method overloading
- Multiple constructor support

#### Signal System
- `Signal`: Custom signal implementation
- Event-driven communication

#### Property System
- `TSProperty`: Thread-safe properties
- Property decorators

### jAGUI Framework
**Purpose**: Custom UI component library
**Components Used**:
- `ModernWindow`: Base window class
- `processMarker`: UI processing decorators
- Layout and component utilities

## Standard Library Dependencies

### Python Standard Library
- `sys`: System-specific parameters
- `os`: Operating system interface
- `json`: JSON encoding/decoding
- `typing`: Type hints
- `threading`: Threading support
- `time`: Time functions
- `uuid`: Unique identifier generation

### Windows-Specific
- `ctypes`: Foreign function library (Windows API calls)
- `ctypes.wintypes`: Windows type definitions

## Project Structure Dependencies

### Internal Module Dependencies

```
src/vannon/
├── main.py
│   ├── PySide6.QtWidgets
│   ├── jAGFx.configuration
│   ├── jAGFx.dependencyInjection
│   ├── jAGFx.logger
│   └── utilities
├── configuration/
│   └── __vAnnonConfiguration.py
│       ├── json
│       ├── jAGFx.configuration
│       └── jAGFx.dependencyInjection
├── contracts/
│   ├── __tag.py
│   │   └── typing
│   └── __videoThread.py
│       └── jAGFx.signal
├── tags/
│   ├── __tag.py
│   │   ├── typing
│   │   ├── jAGFx.overload
│   │   └── jAGFx.serializer
│   └── __tagCollection.py
│       ├── json
│       ├── os
│       ├── typing
│       ├── jAGFx.contracts.configuration
│       ├── jAGFx.dependencyInjection
│       ├── jAGFx.logger
│       ├── jAGFx.overload
│       ├── jAGFx.serializer
│       └── ..configuration
├── boundingbox/
│   └── __boundingBox.py
│       ├── typing
│       ├── uuid
│       ├── PySide6.QtCore
│       └── jAGFx.overload
│       └── jAGFx.serializer
├── videoThread/
│   ├── __videoThread.py
│   │   ├── threading
│   │   ├── time
│   │   ├── cv2
│   │   ├── numpy
│   │   ├── jAGFx.logger
│   │   ├── jAGFx.serializer
│   │   ├── jAGFx.signal
│   │   └── streamer
│   ├── __playbackState.py
│   │   └── enum
│   ├── __mediaState.py
│   │   ├── enum
│   │   └── auto
│   ├── __cacheOptions.py
│   ├── __mediaInfo.py
│   └── __init__.py
└── UI/
    ├── __mainWindow.py
    │   ├── PySide6.QtGui
    │   ├── PySide6.QtWidgets
    │   └── jAGUI.components.forms
    │   └── jAGUI.components.utilities
    │   └── utilities.mwHelper
    └── components/
        ├── __graphicsView.py
        │   ├── PySide6.QtCore
        │   ├── PySide6.QtGui
        │   ├── PySide6.QtWidgets
        │   └── jAGFx.property
        └── __mediaView.py
            ├── cv2
            ├── numpy
            ├── PySide6.QtCore
            ├── PySide6.QtGui
            ├── PySide6.QtWidgets
            ├── jAGFx.logger
            ├── jAGFx.property
            ├── jAGUI.components.utilities
            └── ...videoThread
```

## External Dependencies

### Streamer Framework
**Location**: `src/streamer/`
**Purpose**: Base streaming functionality
**Components Used**:
- `Streamer`: Base streaming class
- `StreamerOptions`: Streaming configuration

### Utility Modules
**Location**: `src/utilities/`
**Purpose**: Shared utility functions
**Components Used**:
- Font loading
- QSS loading
- Configuration loading

## Runtime Dependencies

### Platform-Specific Dependencies

#### Windows
- Windows API (shell32.dll for taskbar icons)
- Windows-specific path handling

#### Cross-Platform
- Qt platform plugins
- OpenCV codecs
- Python runtime

### Configuration File Dependencies

#### JSON Configuration Files
- `config/vannon/appconfig.json`: Application settings
- `assets/tags/tags.json`: Tag definitions

#### Logger Configuration
- `config/logger.cfg`: Logging configuration

## Build and Development Dependencies

### Development Tools
- **Python**: 3.8+
- **Qt Creator**: UI development (optional)
- **VS Code**: Primary IDE
- **Git**: Version control

### Testing Dependencies
- **pytest**: Testing framework
- **unittest**: Standard testing

### Documentation Dependencies
- **Markdown**: Documentation format
- **Mermaid**: Diagram generation

## Dependency Management

### Requirements File
**Location**: `requirements.txt`
**Purpose**: Python package dependencies
**Contents**:
```
PySide6>=6.0.0
opencv-python>=4.5.0
numpy>=1.21.0
```

### Internal Dependency Resolution

#### Dependency Injection Container
- **Provider Pattern**: Service registration and resolution
- **Factory Functions**: Object creation
- **Singleton Management**: Shared instance management

#### Import Structure
- **Relative Imports**: Within vannon package
- **Absolute Imports**: External dependencies
- **Conditional Imports**: Platform-specific code

## Version Compatibility

### Python Version Support
- **Minimum**: Python 3.8
- **Recommended**: Python 3.9+
- **Tested**: Python 3.8, 3.9, 3.10

### Qt/PySide6 Compatibility
- **Qt Version**: 6.0+
- **PySide6**: 6.0+
- **Platform Support**: Windows, Linux, macOS

### OpenCV Compatibility
- **Version**: 4.5+
- **Codecs**: Platform-dependent
- **Python Bindings**: opencv-python

## Performance Considerations

### Memory Dependencies
- **Qt Objects**: Managed by Qt's parent-child system
- **OpenCV Arrays**: Manual memory management
- **Python Objects**: Garbage collected

### Threading Dependencies
- **QThread**: Qt threading
- **threading.Thread**: Python threading
- **RLock**: Thread synchronization

### Caching Dependencies
- **Frame Storage**: NumPy arrays
- **Metadata Storage**: Python dictionaries
- **File I/O**: JSON serialization

## Future Dependency Considerations

### Potential Additions
- **Machine Learning**: TensorFlow, PyTorch for automated annotation
- **Database**: SQLite for annotation storage
- **Network**: Requests for cloud synchronization
- **Image Processing**: Pillow, scikit-image for advanced processing

### Version Pinning Strategy
- **Major Versions**: Pinned for stability
- **Minor Versions**: Flexible for bug fixes
- **Patch Versions**: Automatic updates

### Dependency Updates
- **Automated Testing**: CI/CD pipeline
- **Compatibility Checks**: Version matrix testing
- **Migration Planning**: Breaking change handling
