# Base Components

## Overview

The base components provide the foundation for all jAGUI components, implementing common functionality like layout management, UI setup, and lifecycle handling.

## Component

Base class for all UI components.

**Location**: `src/jAGUI/components/bases/__component.py`

**Features**:
- Layout management with QBoxLayout
- SetupUI method for initialization
- Property-based configuration
- Process marker decorator

**Key Methods**:
- `setupUI(layout)`: Initialize component UI
- `Load()`: Lifecycle loading
- Properties for margins, spacing, etc.

## ComponentBase

Extends Component with QWidget integration.

**Location**: `src/jAGUI/components/bases/__componentBase.py`

**Features**:
- Inherits from Component and QWidget
- Direct Qt widget functionality
- UI setup with layout parameter

## ContainerBase

Provides container functionality for grouping components.

**Location**: `src/jAGUI/components/bases/__containerBase.py`

**Features**:
- Container for multiple child components
- Layout management for children
- Content margins and spacing configuration

## ScrollableFlowWidget

A scrollable container with flow layout capabilities.

**Location**: `src/jAGUI/components/bases/__scrollableFlowWidget.py`

**Features**:
- Scrollable area
- Flow layout for dynamic content
- Vertical scrolling support
