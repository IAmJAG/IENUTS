# Title Bar Components

## Overview

Title bar components provide window control and branding functionality.

## TitleBar

Full-featured title bar with controls and window management.

**Location**: `src/jAGUI/components/titleBar/__titleBar.py`

**Features**:
- Application icon display
- Window title text
- Control buttons: minimize, maximize/restore, close, theme toggle
- Window dragging (when not maximized)
- Double-click to maximize
- QSS preprocessing for theming

**Control Buttons**:
- **Theme**: Reapplies QSS stylesheets
- **Minimize**: Minimizes window
- **Maximize/Restore**: Toggles window maximization
- **Close**: Closes window

**Key Properties**:
- `IconSize`: Size of application icon
- `MainWindow`: Reference to parent window

**Methods**:
- `ToggleMaximizeRestore()`: Toggle window maximization
- `mousePressEvent()`: Handle dragging and double-click
- `mouseMoveEvent()`: Perform window dragging

**QSS Processing**:
- Variable replacement (--var: value)
- Placeholder substitution (@var)
- Regex-based preprocessing

**Implementation Details**:
- Fixed height (40px)
- Horizontal layout with stretch for centering
- Icon loading with fallbacks
- Event filtering for drag operations

## FormTitleBar

Specialized title bar for forms.

**Location**: `src/jAGUI/components/titleBar/__formTitleBar.py`

## TitleBarx

Extended title bar functionality.

**Location**: `src/jAGUI/components/titleBar/__titleBarx.py`
