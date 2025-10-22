# Layout Components

## Overview

Layout components provide custom layout management beyond standard Qt layouts.

## FlowLayout

A custom flow layout that arranges widgets in rows or columns with automatic wrapping.

**Location**: `src/jAGUI/components/layouts/__flowLayout.py`

**Features**:
- Horizontal flow: left to right, wrap down
- Vertical flow: top to bottom, wrap right
- Configurable expansion direction
- Dynamic item management
- Size hint calculation with wrapping

**Key Methods**:
- `setExpandingDirections(orientation)`: Set expansion direction (Vertical/Horizontal)
- `addItem(item)`: Add layout item
- `count()`: Get item count
- `itemAt(index)`: Get item at index
- `takeAt(index)`: Remove and return item

**Properties**:
- `expandingDirections`: Current expansion orientation

**Implementation Details**:
- Uses QRect for positioning calculations
- Supports both test mode (for size calculation) and actual layout
- Handles margins and spacing
- Calculates height for width in vertical expansion mode

**Usage**:
```python
from jAGUI.components.layouts import FlowLayout

layout = FlowLayout()
layout.setExpandingDirections(Qt.Orientation.Vertical)
layout.addWidget(widget1)
layout.addWidget(widget2)
