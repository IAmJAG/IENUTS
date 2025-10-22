# Status Bar Components

## Overview

Status bar components provide information display and window resizing functionality.

## StatusBar

A singleton status bar with message display and resize grip.

**Location**: `src/jAGUI/components/statusBar/__statusBar.py`

**Features**:
- Singleton pattern (one instance per application)
- Message display with timeout
- Integrated resize grip
- Thread-safe message updates
- Fixed height (25px)

**Key Methods**:
- `showMessage(text, timeout)`: Display message, 0 = permanent
- `clearMessage()`: Clear current message

**Signals/Properties**:
- Timer-based automatic clearing
- Expandable status label
- Resize grip in bottom-right

**Usage**:
```python
from jAGUI.components.statusBar import StatusBar, Status

# Direct function call (thread-safe)
Status("Operation completed", 3000)

# Or get instance
status_bar = StatusBar()
status_bar.showMessage("Loading...", 0)
```

**Implementation Details**:
- Uses QMetaObject.invokeMethod for thread safety
- QLabel for status text with expanding policy
- QTimer for message timeouts
- ResizeGrip for window resizing
