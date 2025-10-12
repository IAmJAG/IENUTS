# jAGUI Components Documentation

This document provides an overview of the jAGUI component library used in the eNuts project. The components are organized into categories and follow object-oriented design principles with extensive use of decorators, inheritance, and design patterns.

## Overview

The jAGUI components are built on PySide6 (Qt) and provide reusable UI elements for building modern, flat-designed applications. Components follow the project's coding style rules, including type hints, dependency injection, and consistent naming conventions.

## Architecture

### Base Classes

All components inherit from base classes that provide common functionality:

- **Component**: Base class for all UI components, provides layout management and setup methods.
- **ComponentBase**: Extends Component with QWidget integration.
- **ContainerBase**: Provides container functionality for grouping components.
- **ScrollableFlowWidget**: A scrollable container with flow layout capabilities.

### Key Features

- **Process Markers**: All components use the `@processMarker` decorator for lifecycle management.
- **Dependency Injection**: Components use the Provider system for resolving dependencies.
- **Type Safety**: Extensive use of type hints throughout.
- **Logging**: Integrated logging using the custom logger.
- **Styling**: Components support QSS (Qt Style Sheets) for theming.

## Component Categories

Detailed documentation for each category is available in separate files:

### [Bases](components/bases.md)

Fundamental base classes for component development.

### [Cards](components/cards.md)

Card-based UI elements, including the `cardBase` used for launch tiles.

### [Forms](components/forms.md)

Window and form components, including `ModernWindow` used in the dashboard.

### [Layouts](components/layouts.md)

Layout management components, including `FlowLayout`.

### [Navigation](components/navigation.md)

Navigation components like `SideNavigationBar`.

### [Status Bar](components/statusBar.md)

Status display components including the singleton `StatusBar`.

### [Title Bar](components/titleBar.md)

Window title bar components with full control functionality.

### Other Categories

- **Buttons**: Interactive button components (Button, ScaleButton).
- **Central**: Central widget components.
- **CommandBar**: Command bar interfaces.
- **Logger**: Logging view components.
- **Pages**: Page-based navigation.
- **ResizeGrip**: Window resize handles.
- **Spinbox**: Custom spin box controls.
- **Utilities**: Various utility components and helpers.

## Usage Examples

### Creating a Card Component

```python
from jAGUI.components.cards import cardBase

# Create a launch card
card = cardBase("Application Name", "path/to/icon.png")
card.clicked.connect(lambda: launch_app())
```

### Using FlowLayout

```python
from jAGUI.components.layouts import FlowLayout

layout = FlowLayout()
layout.setExpandingDirections(Qt.Orientation.Vertical)
layout.addWidget(card1)
layout.addWidget(card2)
```

### ModernWindow Setup

```python
from jAGUI.components.forms import ModernWindow

class MyWindow(ModernWindow):
    def setupUI(self):
        super().setupUI()
        # Add components to self._layout
        self._layout.addWidget(my_component)
```

## Styling

Components support Qt Style Sheets (QSS) for theming. The title bar includes QSS preprocessing for variables and placeholders.

## Dependencies

Components rely on:

- PySide6 for Qt functionality
- jAGFx framework for configuration, logging, dependency injection
- Custom utilities for icons, styles, and helpers

## Best Practices

- Always call `super().setupUI()` in overridden setupUI methods
- Use the Provider system for dependency resolution
- Follow naming conventions (TitleCase for public methods, camelCase for parameters)
- Use type hints extensively
- Log important events using the custom logger
- Handle exceptions appropriately with try-except blocks
