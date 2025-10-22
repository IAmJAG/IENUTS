# Dashboard Module Documentation

This document describes the implementation of the dashboard module in the eNuts project, a modern flat launcher dashboard using PySide6.

## Overview

The dashboard serves as a launcher for applications within the eNuts suite. It displays launchable items (e.g., eNuts, Video Annotator) and hides itself when an application is launched, remaining accessible via a system tray icon.

## Architecture

### Main Components

- **MainWindow**: The primary window class inheriting from `ModernWindow`.
- **Layout**: Uses `FlowLayout` for arranging launch tiles.
- **Launch Tiles**: Implemented using `cardBase` components.
- **Tray Icon**: `QSystemTrayIcon` for restoring the dashboard.
- **Configuration**: `DashboardConfiguration` for app settings.

### Key Files

- `src/dashboard/main.py`: Main entry point for the dashboard application.
- `src/dashboard/UI/__init__.py`: Exports the `MainWindow` class.
- `src/dashboard/UI/__mainWindow.py`: Contains the `MainWindow` implementation.
- `src/dashboard/configuration/__dashboardConfiguration.py`: Configuration class.
- `config/db/appconfig.json`: Configuration file.

## Implementation Details

### MainWindow Class

The `MainWindow` class extends `ModernWindow` and sets up the UI with a flow layout containing launch cards.

#### Setup Process

1. Initializes the layout as a `FlowLayout` with vertical expansion.
2. Adds `cardBase` components for "eNuts" and "Video Annotator" with icons.
3. Connects the card's click event to launch the respective application.
4. Sets margins, spacing, and alignment.
5. Sets up the system tray icon.

#### Launch Mechanism

Applications are launched using `subprocess.Popen` to run the same executable with `--launch <appName>` arguments. After launching, the dashboard hides itself.

```python
def _launchApp(self, appName):
    lCmd = [sys.executable, sys.argv[0], "--launch", appName]
    try:
        subprocess.Popen(lCmd)
    except OSError as e:
        debug(f"Error launching application as separate process: {e}")
        return
    self.hide()
```

#### Tray Icon

The tray icon provides a context menu with "Show Dashboard" and "Exit" options. It uses the configuration for icon and tooltip.

### Dependencies

- `jAGFx.configuration.iConfiguration`
- `jAGFx.dependencyInjection.Provider`
- `jAGFx.logger.debug`
- `jAGFx.utilities.io.getICONPath`
- `jAGUI.components.cards.cardBase`
- `jAGUI.components.forms.ModernWindow`
- `jAGUI.components.layouts.FlowLayout`
- `jAGUI.components.utilities.processMarker`
- `..configuration.DashboardConfiguration`

## Design Principles

The dashboard follows flat and minimalist design principles using Qt Style Sheets (QSS) for styling.

### Visual Elements

- **Background**: Light background color.
- **Cards**: White background with subtle borders and rounded corners.
- **Icons**: Large, centered icons on cards.
- **Interactivity**: Hover and pressed states for visual feedback.

### Layout

- Uses `FlowLayout` for flexible arrangement of cards.
- Cards are centered and have minimal margins/spacing.

## Configuration

The dashboard uses `DashboardConfiguration` loaded from `config/db/appconfig.json` for settings like icon, title, company, and app ID.

## Future Extensions

To add more launchable applications:

1. Create additional `cardBase` instances in `setupUI`.
2. Connect their `clicked` signals to new `_launchApp` calls with different app names.
3. Ensure the launched applications handle the `--launch` argument appropriately.

## Qt Style Sheets (QSS)

The styling is handled by the underlying `ModernWindow` and `cardBase` components, which apply flat design principles.

## Related Documentation

- [eNuts Dashboard Page](enuts-dashboard.md) - The dashboard page within the eNuts application
- [POC Dashboard](poc-dashboard.md) - Proof of concept implementation
