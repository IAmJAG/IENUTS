# Navigation Components

## Overview

Navigation components provide menu systems and navigation panels for application interfaces.

## SideNavigationBar

A collapsible side navigation bar with smooth animations.

**Location**: `src/jAGUI/components/navigation/__sideNavigationBar.py`

**Features**:
- Expandable/collapsible with animation
- Toggle button with icon changes
- Menu container for navigation items
- Thread-safe state management
- Configurable animation duration and easing

**States**:
- COLLAPSED: Minimized state
- EXPANDED: Full size state
- COLLAPSING/EXPANDING: Transition states

**Key Properties**:
- `AnimationDuration`: Animation length in milliseconds
- `EasingCurve`: Animation easing function
- `State`: Current navigation state
- `OnStateChanged`: Signal emitted on state changes

**Methods**:
- `toggle()`: Toggle between expanded/collapsed
- `setupUI()`: Initialize UI components

**Implementation Details**:
- Uses QPropertyAnimation for smooth transitions
- Icon changes based on state (show/hide icons)
- ContainerBase for menu contents
- RLock for thread-safe state changes

**Usage**:
```python
from jAGUI.components.navigation import SideNavigationBar

nav = SideNavigationBar("Menu", "menu_icon.png")
nav.Layout.addWidget(menu_item1)
nav.Layout.addWidget(menu_item2)
```

## _navigationBar (Base)

Base class for navigation bars.

**Location**: `src/jAGUI/components/navigation/__base.py`

**Features**:
- Common navigation functionality
- State enumeration
- Orientation support
- Size management for expand/collapse
