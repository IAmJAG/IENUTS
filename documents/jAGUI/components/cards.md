# Card Components

## Overview

Card components provide clickable, icon-based UI elements commonly used for navigation and launching applications.

## cardBase

A clickable card component with icon and title.

**Location**: `src/jAGUI/components/cards/__cardBase.py`

**Features**:
- Displays an icon and title
- Clickable with signal emission
- Hand cursor on hover
- Minimum size constraints (160x220)
- Icon scaling and smoothing

**Properties**:
- `Title`: Get/set the card title
- `clicked`: Signal emitted on mouse click

**Usage**:
```python
from jAGUI.components.cards import cardBase

card = cardBase("Video Annotator", "path/to/logo.png")
card.clicked.connect(lambda: launch_app())
```

**Implementation Details**:
- Uses QVBoxLayout for vertical arrangement
- Icon displayed at 160x160, scaled with aspect ratio preservation
- Title centered below icon
- Mouse release event triggers click signal
