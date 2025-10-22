# vAnnon Documentation Index

## Overview

vAnnon is a specialized video annotation application designed for creating bounding box annotations on video frames. This documentation provides comprehensive information about the system's architecture, components, workflows, and usage.

## Documentation Structure

### Core Documentation

| Document | Description | Audience |
|----------|-------------|----------|
| [README.md](README.md) | System overview, purpose, and key features | All users |
| [architecture.md](architecture.md) | High-level system design and patterns | Architects, developers |
| [components.md](components.md) | Detailed component descriptions | Developers |
| [workflows.md](workflows.md) | Process flows and data movement | Developers, users |
| [api.md](api.md) | Complete API reference | Developers |
| [diagrams.md](diagrams.md) | Visual architecture diagrams | All technical users |
| [dependencies.md](dependencies.md) | Libraries and dependency information | Developers, deployers |
| [file-structure.md](file-structure.md) | Code organization and file layout | Developers |

## Quick Start

### For Users
1. **Getting Started**: Read [README.md](README.md) for system overview
2. **Basic Usage**: Refer to workflow examples in [workflows.md](workflows.md)
3. **UI Guide**: See component descriptions in [components.md](components.md)

### For Developers
1. **System Architecture**: Start with [architecture.md](architecture.md)
2. **API Reference**: Use [api.md](api.md) for implementation details
3. **Code Structure**: Review [file-structure.md](file-structure.md)
4. **Dependencies**: Check [dependencies.md](dependencies.md)

## Key Concepts

### Core Components

#### Data Models
- **Tag**: Classification system for annotations
- **BoundingBox**: Spatial annotation regions
- **TagCollection**: Tag management and persistence

#### Processing Engine
- **VideoThread**: Video loading, playback, and caching
- **MediaInfo**: Video metadata and properties
- **CacheOptions**: Performance optimization settings

#### User Interface
- **MainWindow**: Application container
- **MediaView**: Video display with annotation capabilities
- **GraphicsView**: Interactive drawing canvas

### Key Workflows

#### Video Processing
1. **Loading**: File selection → VideoCapture initialization → Metadata extraction
2. **Playback**: Frame serving → Caching → Display updates
3. **Seeking**: Position requests → Cache checking → Frame decoding

#### Annotation Process
1. **Creation**: User drawing → Rectangle validation → BoundingBox instantiation
2. **Management**: Scene addition → Event handling → Data persistence
3. **Editing**: Selection → Modification → Update propagation

### Architecture Patterns

#### Design Patterns Used
- **Dependency Injection**: Service resolution and configuration
- **Observer Pattern**: Signal/slot event system
- **Factory Pattern**: Object creation and initialization
- **Decorator Pattern**: Cross-cutting concerns (logging, benchmarking)

#### Threading Model
- **Main Thread**: UI updates and user interaction
- **Video Thread**: Frame processing and playback
- **Cache Thread**: Background frame prefetching

## Configuration

### Application Settings
- **Location**: `config/vannon/appconfig.json`
- **Managed by**: `vAnnonConfiguration` class
- **Key Settings**:
  - Application metadata (title, company, version)
  - UI styling and themes
  - Tag storage paths
  - Logging configuration

### Runtime Configuration
- **Dependency Injection**: Service registration and resolution
- **Environment Variables**: Platform-specific paths
- **Dynamic Settings**: User preferences and session state

## Development Guidelines

### Coding Standards
- **Naming**: Follow project conventions (see `.kilocode/rules/NamingConventions.md`)
- **Style**: Adhere to coding style rules (see `.kilocode/rules/CodingStyle.md`)
- **Documentation**: Inline comments and docstrings

### File Organization
- **Modules**: Double underscore prefix (`__moduleName.py`)
- **Packages**: Lowercase directory names
- **Imports**: Grouped by type (standard, third-party, local)

### Testing
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction validation
- **UI Tests**: User interaction workflows

## API Reference Summary

### Primary Classes

| Class | Purpose | Key Methods |
|-------|---------|--------------|
| `Tag` | Annotation classification | `Code`, `Text`, `Description` |
| `BoundingBox` | Spatial annotation | `X`, `Y`, `W`, `H`, `Class` |
| `VideoThread` | Video processing | `play()`, `pause()`, `seek()` |
| `MediaView` | UI video display | `AddGraphicItem()`, `ProcessImage()` |
| `TagCollection` | Tag management | `Append()`, `FindByCode()`, `Save()` |

### Key Signals

| Signal | Source | Purpose |
|--------|--------|---------|
| `OnFrame` | VideoThread | New frame available |
| `OnBoxCreated` | GraphicsView | User created rectangle |
| `OnItemAdded` | MediaView | Annotation added |
| `OnPlaybackStateChanged` | VideoThread | Playback state changed |

## Performance Considerations

### Optimization Areas
- **Frame Caching**: Reduces seek latency
- **Memory Management**: Efficient resource cleanup
- **UI Responsiveness**: Thread separation
- **Graphics Rendering**: Optimized drawing operations

### Monitoring Points
- **Cache Hit Rates**: Frame retrieval efficiency
- **Memory Usage**: Resource consumption tracking
- **Frame Rates**: Playback performance metrics
- **UI Latency**: Response time measurements

## Deployment and Packaging

### Runtime Requirements
- **Python**: 3.8+
- **PySide6**: 6.0+
- **OpenCV**: 4.5+
- **NumPy**: 1.21+

### Distribution
- **Source Distribution**: Python modules and assets
- **Binary Distribution**: Frozen executable with dependencies
- **Configuration**: JSON config files
- **Assets**: Icons, images, and tag definitions

## Integration Points

### eNuts Ecosystem
- **Shared Frameworks**: jAGFx, jAGUI
- **Configuration**: Common settings management
- **Logging**: Unified logging system
- **UI Components**: Consistent look and feel

### External Tools
- **Data Export**: Training data for ML pipelines
- **Video Formats**: OpenCV-supported codecs
- **Annotation Standards**: JSON-based interchange formats

## Future Extensions

### Planned Features
- **Automated Annotation**: ML model integration
- **Batch Processing**: Multiple video workflows
- **Collaborative Editing**: Multi-user annotation
- **Advanced Tools**: Polygon annotations, keypoint detection

### Extension Points
- **Plugin Architecture**: Modular component loading
- **Custom Tags**: Extensible classification systems
- **Alternative UIs**: Different interface implementations
- **Export Formats**: Additional data interchange options

## Support and Resources

### Documentation Navigation
- **Conceptual**: Start with README and architecture
- **Implementation**: Use components and API reference
- **Integration**: Review workflows and dependencies

### Development Resources
- **Code Examples**: API documentation
- **Diagrams**: Visual architecture understanding
- **Configuration**: Setup and customization
- **Performance**: Optimization guidelines

---

This documentation provides a comprehensive guide to the vAnnon video annotation system. For specific implementation details, refer to the individual documents linked above.
