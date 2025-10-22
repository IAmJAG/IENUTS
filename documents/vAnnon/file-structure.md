# vAnnon File Structure and Organization

## Project Root Structure

```
d:/WS/nutsLAB/eNuts/
├── requirements.txt
├── .kilocode/
│   └── rules/
│       ├── CodingStyle.md
│       └── NamingConventions.md
├── .vscode/
├── assets/
│   ├── icons/
│   │   ├── logo.png
│   │   ├── arrowDown.png
│   │   ├── plus.png
│   │   ├── SaveAnnon.png
│   │   └── verify.png
│   │   └── basicOL/
│   │       └── minus.png
│   │   └── controlbox/
│   │       └── aesthetic.png
│   ├── images/
│   └── names.json
├── config/
│   ├── appconfig.json
│   ├── logger.cfg
│   ├── db/
│   │   └── appconfig.json
│   ├── enuts/
│   │   └── appconfig.json
│   └── vannon/
│       └── appconfig.json
├── documents/
│   ├── summary.md
│   ├── todo.md
│   └── vAnnon/
│       ├── README.md
│       ├── architecture.md
│       ├── components.md
│       ├── workflows.md
│       ├── api.md
│       ├── diagrams.md
│       ├── dependencies.md
│       └── file-structure.md
└── src/
    ├── main.py
    ├── dashboard/
    ├── eNuts/
    ├── jAGFx/
    ├── jAGUI/
    ├── poc/
    ├── streamer/
    ├── test/
    ├── utilities/
    └── vannon/
```

## vAnnon Module Structure

```
src/vannon/
├── main.py                          # Application entry point
├── boundingbox/
│   └── __boundingBox.py            # Bounding box implementation
├── configuration/
│   ├── __init__.py
│   └── __vAnnonConfiguration.py    # App-specific configuration
├── contracts/
│   ├── __init__.py
│   ├── __tag.py                    # Tag interface contract
│   └── __videoThread.py            # Video thread interface contract
├── tags/
│   ├── __init__.py
│   ├── __tag.py                    # Tag implementation
│   └── __tagCollection.py          # Tag collection management
├── videoThread/
│   ├── __init__.py
│   ├── __cacheOptions.py           # Frame caching configuration
│   ├── __mediaInfo.py              # Video metadata
│   ├── __mediaState.py             # Media loading states
│   ├── __playbackState.py          # Playback control states
│   └── __videoThread.py            # Video processing thread
└── UI/
    ├── __init__.py
    ├── __mainWindow.py             # Main application window
    └── components/
        ├── __graphicsView.py       # Video display canvas
        └── __mediaView.py          # Annotation-enabled media view
```

## File Naming Conventions

### Module Files
- **Double Underscore Prefix**: `__moduleName.py`
  - Example: `__tag.py`, `__boundingBox.py`
  - Purpose: Private module implementation
  - Convention: Lowercase with underscores

### Package Structure
- **Directory Names**: Lowercase, no underscores
  - Example: `boundingbox/`, `configuration/`, `videoThread/`
- **Package Init**: `__init__.py` in each directory

### Configuration Files
- **JSON Configs**: `appconfig.json`
- **Logger Config**: `logger.cfg`
- **Tag Storage**: `tags.json`

## Code Organization Principles

### Separation of Concerns

#### 1. Entry Point (`main.py`)
**Responsibilities**:
- Application initialization
- Dependency injection setup
- Qt application lifecycle
- Platform-specific configuration

**Dependencies**:
- Qt widgets and core
- Framework configuration
- Dependency injection
- Logging utilities

#### 2. Configuration Layer (`configuration/`)
**Responsibilities**:
- Application settings management
- Tag path configuration
- JSON serialization/deserialization

**Key Classes**:
- `vAnnonConfiguration`: Extends `ApplicationConfiguration`

#### 3. Data Models (`tags/`, `boundingbox/`)
**Responsibilities**:
- Domain object definitions
- Business logic validation
- Serialization support

**Key Classes**:
- `Tag`: Annotation classification
- `TagCollection`: Tag management
- `BoundingBox`: Spatial annotation

#### 4. Business Logic (`videoThread/`)
**Responsibilities**:
- Video file processing
- Frame caching and seeking
- Playback state management
- Performance optimization

**Key Classes**:
- `VideoThread`: Video processing engine
- `MediaInfo`: Video metadata
- `CacheOptions`: Caching configuration

#### 5. User Interface (`UI/`)
**Responsibilities**:
- Visual component management
- User interaction handling
- Graphics rendering
- Event processing

**Key Classes**:
- `MainWindow`: Application window
- `MediaView`: Video display with annotations
- `GraphicsView`: Interactive canvas

#### 6. Contracts (`contracts/`)
**Responsibilities**:
- Interface definitions
- Type safety enforcement
- API contracts

**Key Protocols**:
- `iTag`: Tag interface
- `iVideoThread`: Video thread interface

### Dependency Flow

```
main.py
├── configuration (loads settings)
├── UI (creates window)
│   └── components
│       └── MediaView
│           └── VideoThread (video processing)
│               └── boundingbox (annotations)
└── tags (loads tag definitions)
    └── TagCollection
        └── Tag (individual tags)
```

## Asset Organization

### Icons (`assets/icons/`)
- **logo.png**: Application icon
- **arrowDown.png**: UI navigation
- **plus.png**: Add operations
- **SaveAnnon.png**: Save annotations
- **verify.png**: Validation/checking
- **basicOL/minus.png**: Remove operations
- **controlbox/aesthetic.png**: UI styling

### Images (`assets/images/`)
- General image assets
- UI backgrounds
- Visual elements

### Configuration (`config/vannon/`)
- **appconfig.json**: Application settings
  ```json
  {
    "Title": "jAG's Video Annotator",
    "Company": "jAG",
    "AppId": "vAnnon",
    "TagsPath": ".\\assets\\tags\\tags.json",
    "Style": "base"
  }
  ```

### Tag Storage (`assets/tags/`)
- **tags.json**: Persistent tag definitions
- Auto-created if missing
- JSON format with type metadata

## Import Structure

### Internal Imports
```python
# Relative imports within vannon
from .configuration import vAnnonConfiguration
from .tags import Tag, TagCollection
from .boundingbox import BoundingBox
from .videoThread import VideoThread, ePlaybackState
from .UI import MainWindow
from .contracts import iTag, iVideoThread
```

### External Framework Imports
```python
# jAGFx framework
from jAGFx.configuration import ApplicationConfiguration, iConfiguration
from jAGFx.dependencyInjection import Provider
from jAGFx.logger import debug, info, warning, error
from jAGFx.serializer import Serialisable, jsonDecode
from jAGFx.signal import Signal
from jAGFx.overload import OverloadDispatcher

# jAGUI framework
from jAGUI.components.forms import ModernWindow
from jAGUI.components.utilities import processMarker

# Qt/PySide6
from PySide6.QtWidgets import QApplication, QBoxLayout
from PySide6.QtCore import QRectF, Signal as QtSignal
from PySide6.QtGui import QPixmap, QMouseEvent

# Third-party
import cv2 as cv
import numpy as np
```

## File Dependencies Map

### main.py Dependencies
```
main.py
├── PySide6.QtWidgets (QApplication)
├── jAGFx.configuration (iConfiguration)
├── jAGFx.dependencyInjection (Provider)
├── jAGFx.logger (debug)
├── utilities (LoadFonts, LoadQSS, loadConfig)
├── vannon.configuration (vAnnonConfiguration)
└── vannon.UI (MainWindow)
```

### VideoThread Dependencies
```
__videoThread.py
├── threading (RLock, Thread)
├── time (monotonic, sleep, time)
├── cv2 (VideoCapture, CAP_PROP_*)
├── numpy (ndarray)
├── jAGFx.logger (debug)
├── jAGFx.serializer (Serialisable)
├── jAGFx.signal (Signal)
├── streamer (Streamer, StreamerOptions)
├── .__cacheOptions (CacheOptions)
├── .__mediaInfo (MediaInfo)
├── .__mediaState (eMediaState)
└── .__playbackState (ePlaybackState)
```

### MediaView Dependencies
```
__mediaView.py
├── cv2 (cv)
├── numpy (ndarray)
├── PySide6.QtCore (QEvent, QPointF, QRectF, Signal)
├── PySide6.QtGui (QCursor, QPen, QPixmap)
├── PySide6.QtWidgets (QBoxLayout, QGraphicsItem)
├── jAGFx.logger (debug)
├── jAGFx.property (TSProperty)
├── jAGUI.components.utilities (processMarker)
├── ...videoThread (VideoThread, ePlaybackState)
└── .__graphicsView (GraphicsView)
```

## Build and Deployment Structure

### Development Structure
- **Source**: `src/vannon/` - All Python modules
- **Assets**: `assets/` - Icons, images, tag definitions
- **Config**: `config/vannon/` - Application settings
- **Docs**: `documents/vAnnon/` - Documentation

### Runtime Structure
- **Executable**: `src/vannon/main.py`
- **Libraries**: PySide6, OpenCV, NumPy
- **Assets**: Relative paths from executable
- **Config**: JSON files loaded at runtime

### Packaging Considerations
- **Dependencies**: Listed in `requirements.txt`
- **Data Files**: Assets and config included
- **Entry Point**: `main.py` with proper imports

## Version Control Organization

### Git Structure
```
.gitignore
├── *.pyc
├── __pycache__/
├── *.log
├── config/local/  # Local configs not committed
└── assets/tags/   # Generated tag files
```

### Documentation Structure
```
documents/vAnnon/
├── README.md          # Overview and getting started
├── architecture.md    # System design and patterns
├── components.md      # Detailed component descriptions
├── workflows.md       # Process flows and data movement
├── api.md            # API reference and usage examples
├── diagrams.md       # Visual architecture diagrams
├── dependencies.md   # Library and dependency information
└── file-structure.md # This file
```

## Extensibility Points

### Adding New Components
1. **Create Module**: Add `__newComponent.py` in appropriate directory
2. **Update Imports**: Add to `__init__.py` if public
3. **Register Dependencies**: Add to DI container if needed
4. **Update Documentation**: Add to relevant docs

### Configuration Extensions
1. **Add Properties**: Extend `vAnnonConfiguration`
2. **Update JSON Schema**: Modify `appconfig.json`
3. **Handle Defaults**: Provide fallback values

### UI Extensions
1. **Create Component**: Extend existing UI classes
2. **Add to Layout**: Integrate into `MainWindow` or `MediaView`
3. **Connect Signals**: Wire up event handling

This file structure provides a solid foundation for the vAnnon video annotation system, with clear separation of concerns, consistent naming, and room for future extensions.
