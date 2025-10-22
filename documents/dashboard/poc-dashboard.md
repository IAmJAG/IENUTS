# POC Dashboard Documentation

This document describes the proof-of-concept (POC) dashboard implementation in the eNuts project.

## Overview

The POC dashboard is a standalone demonstration of dashboard functionality, showcasing a modern flat launcher interface using PySide6. It serves as a reference implementation for the main dashboard module.

## Architecture

### Main Components

- **LaunchCard**: Custom widget for individual application launch tiles.
- **LaunchTile**: Wrapper widget containing a LaunchCard with launch callback.
- **IndependentApp**: Separate application window launched by the dashboard.
- **Dashboard**: Main launcher window with grid layout and tray icon.

### Key Files

- `src/poc/dashboard.py`: Complete POC implementation in a single file.

## Implementation Details

### LaunchCard Class

A custom QWidget that displays an application name with an icon and emits a clicked signal.

#### Features

- Cursor changes to pointing hand on hover.
- Minimum width constraint for consistent sizing.
- Icon display using standard Qt icons.
- Click event handling with signal emission.

### LaunchTile Class

A wrapper that combines a LaunchCard with a launch callback function.

### IndependentApp Class

A QMainWindow that represents a launched application, running in a separate process.

#### Features

- Displays application name and process ID.
- Custom styling with light blue background.
- Serves as a placeholder for actual application functionality.

### Dashboard Class

The main launcher window that displays launch tiles and manages application launching.

#### Setup Process

1. Creates main window with title and geometry.
2. Initializes active apps tracking.
3. Sets up UI with grid layout containing launch tiles.
4. Configures system tray icon with context menu.

#### Launch Mechanism

Applications are launched using `subprocess.Popen` with command line arguments:

```python
command = [sys.executable, sys.argv[0], "--launch-app", app_name]
subprocess.Popen(command)
```

After launching, the dashboard hides itself.

#### Tray Icon

Provides system tray functionality with:
- Custom icon and tooltip.
- Context menu with "Show Dashboard" and "Exit" options.

### Execution Model

The script determines whether to run as dashboard or launched app based on command line arguments:

- Default: Runs the Dashboard
- `--launch-app <name>`: Runs IndependentApp with specified name

## Design Principles

The POC follows flat design principles with custom QSS styling.

### Visual Elements

- **Background**: Light gray background (`#D8E0E5`).
- **Cards**: White background with subtle borders and rounded corners.
- **Icons**: Standard Qt icons for demonstration.
- **Interactivity**: Hover effects with blue accent colors.

### Layout

- Grid layout for organizing launch tiles.
- Centered content with padding.
- Section headers with high contrast bands.

## Configuration

The POC uses hardcoded values for demonstration purposes. In production implementations, this would be replaced with configuration files.

## Dependencies

- `PySide6.QtCore, QtGui, QtWidgets`
- `subprocess, sys`

## Purpose and Usage

The POC serves as:

1. **Reference Implementation**: Demonstrates core dashboard concepts.
2. **Testing Ground**: Allows experimentation with UI layouts and interactions.
3. **Educational Tool**: Shows how to implement launcher-style applications in PySide6.

## Limitations

- Uses standard Qt icons instead of custom icons.
- Hardcoded application names and styling.
- No actual application functionality beyond placeholder windows.
- Single-file implementation (not modular).

## Future Extensions

To evolve the POC into a production dashboard:

1. Extract components into separate modules.
2. Implement proper configuration system.
3. Add custom icon support.
4. Integrate with actual applications.
5. Add error handling and logging.
6. Implement application state management.

## Qt Style Sheets (QSS)

The POC includes comprehensive QSS styling for all components:

```python
style_sheet = """
/* GLOBAL STYLES */
QMainWindow { background-color: #D8E0E5; }

/* LAUNCH CARDS */
QWidget#LaunchCard {
    background-color: #FFFFFF;
    color: #333333;
    border: 1px solid #CCCCCC;
    border-radius: 8px;
}

/* TEXT */
QLabel#LaunchCardText {
    font-size: 11pt;
    font-weight: 500;
    background-color: transparent;
}

/* INTERACTIVITY */
QWidget#LaunchCard:hover {
    background-color: #EAF2FF;
    border: 1px solid #4A90E2;
}
QWidget#LaunchCard:pressed {
    background-color: #DDEEFC;
}

/* SECTION HEADERS */
QLabel {
    font-size: 16pt;
    font-weight: bold;
    color: #444444;
    padding: 10px 30px;
    margin-top: 0;
    background-color: #FFFFFF;
    border-bottom: 1px solid #CCCCCC;
}
"""
```

## Related Documentation

- [Dashboard Module](readme.md) - Production dashboard implementation
- [eNuts Dashboard Page](enuts-dashboard.md) - In-app dashboard page
