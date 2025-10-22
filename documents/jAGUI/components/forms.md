# Form Components

## Overview

Form components provide window and dialog functionality with integrated title bars, status bars, and navigation.

## ModernWindow

A modern window with title bar and status bar.

**Location**: `src/jAGUI/components/forms/__modernWindow.py`

**Features**:
- Inherits from FormBasic
- Integrated TitleBar and StatusBar
- Content layout for adding components
- Process marker decorator

**Structure**:
- TitleBar at top
- Content layout (QBoxLayout) in middle
- StatusBar at bottom

**Usage**:
```python
from jAGUI.components.forms import ModernWindow

class MyWindow(ModernWindow):
    def setupUI(self):
        super().setupUI()
        # Add components to self._layout
        self._layout.addWidget(my_component)
```

**Key Properties**:
- `_layout`: Content layout for adding widgets

## FormBasic

Basic form implementation.

**Location**: `src/jAGUI/components/forms/__basic.py`

**Features**:
- Base form functionality
- Layout management
- Component addition methods

## CustomTitleBar

Customizable title bar component.

**Location**: `src/jAGUI/components/forms/__customTitleBar.py`

## FormWithSideNavigation

Form with integrated side navigation.

**Location**: `src/jAGUI/components/forms/__sideNavigation.py`

**Features**:
- Side navigation panel
- Main content area
- Navigation state management

## FormBase

Base class for all forms.

**Location**: `src/jAGUI/components/forms/base/__formBase.py`

**Features**:
- Fundamental form functionality
- Component management
- Layout setup
