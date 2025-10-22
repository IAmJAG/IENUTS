# eNuts Dashboard Page Documentation

This document describes the dashboard page implementation within the eNuts application.

## Overview

The eNuts dashboard page serves as the main landing page within the eNuts application, providing a welcome message and entry point for training functionality.

## Architecture

### Main Components

- **Dashboard Function**: A function that creates and configures the dashboard page.
- **Layout**: Uses vertical box layout for arranging UI elements.
- **Welcome Label**: Displays the application title and description.
- **Training Button**: Entry point for starting the training process.

### Key Files

- `src/eNuts/UI/pages/__dashboard.py`: Contains the `Dashboard()` function implementation.

## Implementation Details

### Dashboard Function

The `Dashboard()` function creates a page using the `CreatePage` helper and adds UI elements.

#### Setup Process

1. Creates a page with title "--DASHBOARD--" and object name "DASHBOARD".
2. Adds a welcome label with centered alignment and custom styling.
3. Adds a description label with centered alignment and lighter styling.
4. Adds a "Start Training" button with custom styling and centered alignment.
5. Adds stretch to push content to the top.

#### UI Elements

- **Welcome Label**: "Welcome to eNuts!" with large, bold font.
- **Description Label**: "Your evolving Neural user training system." with smaller font.
- **Training Button**: Blue button with hover and press effects.

### Styling

The page uses inline CSS styling for Qt widgets:

```python
lWelcomeLabel.setStyleSheet("font-size: 24px; font-weight: bold; color: #f0f0f0;")
lDescriptionLabel.setStyleSheet("font-size: 14px; color: #cccccc;")
lBtn.setStyleSheet("""
    QPushButton {
        background-color: #007acc;
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #005f99;
    }
    QPushButton:pressed {
        background-color: #003f66;
    }
""")
```

## Dependencies

- `PySide6.QtCore.Qt`
- `PySide6.QtWidgets.QLabel, QPushButton`
- `..mwHelper` (for `CreatePage` function)

## Design Principles

The dashboard page follows a clean, centered layout with a dark theme suitable for the eNuts application.

### Visual Elements

- **Background**: Inherits from parent container (typically dark).
- **Text**: Light colors for contrast against dark background.
- **Button**: Blue accent color with interactive states.

### Layout

- Vertical centering with stretch at bottom.
- Centered alignment for all elements.
- Minimal spacing and margins.

## Future Extensions

The dashboard page is designed to be extended with additional functionality:

1. Connect the training button to actual training workflows.
2. Add status indicators or recent activity.
3. Include quick access to common features.
4. Add navigation elements or shortcuts.

## Integration

The dashboard page is integrated into the main eNuts application through the navigation system in `src/eNuts/UI/__mainWindow.py`, where it's added as a menu item.
