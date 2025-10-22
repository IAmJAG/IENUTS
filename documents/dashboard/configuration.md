# Dashboard Configuration Documentation

This document describes the configuration system for the dashboard module in the eNuts project.

## Overview

The dashboard configuration manages application settings, logging, and UI customization for the dashboard launcher.

## Architecture

### Main Components

- **DashboardConfiguration**: Main configuration class extending ApplicationConfiguration.
- **LoadCFG Function**: Factory function for loading configuration from JSON.
- **Configuration File**: JSON file containing all settings.

### Key Files

- `src/dashboard/configuration/__dashboardConfiguration.py`: Configuration class implementation.
- `config/db/appconfig.json`: Configuration data file.

## Implementation Details

### DashboardConfiguration Class

Extends `ApplicationConfiguration` with dashboard-specific properties.

#### Properties

- **TagsPath**: Path to tags directory (default: `".\\assets\\tags"`).
- Inherited properties from ApplicationConfiguration:
  - Title, Company, AppId, Icon
  - StyleDefaults, Style
  - ImagesPaths, ImagesExtensions

#### Path Handling

The `TagsPath` property includes normalization:
- Converts forward slashes to backslashes (Windows compatibility).
- Removes trailing backslashes.

### LoadCFG Function

Loads configuration from JSON file and decodes it into a DashboardConfiguration instance.

#### Process

1. Creates a new DashboardConfiguration instance.
2. Opens and parses the JSON file.
3. Calls `cfg.decode(cfgdict)` to populate properties.
4. Returns the configured instance.

### Dependency Injection

The configuration is registered with the Provider system:

```python
Provider.RegisterFactory(iConfiguration, LoadCFG, DashboardConfiguration, True)
```

This allows other components to resolve `iConfiguration` and receive a `DashboardConfiguration` instance.

## Configuration File Structure

The configuration is stored in `config/db/appconfig.json`:

```json
{
  "Sections": {
    "LOGGER": {
      "DefaultLogLevel": "DEBUG",
      "Filters": {
        "NOTMINE": {
          ".ALL": "DEBUG"
        },
        "jAGUI": {
          ".components.utilities": "ERROR"
        }
      },
      "__type__": "jAGFx.configuration.LoggerConfig"
    }
  },
  "Title": "eNuts Dashboard",
  "Company": "jAG",
  "AppId": "dashboard",
  "Icon": "logo",
  "StyleDefaults": "cooldark",
  "Style": "base",
  "ImagesPaths": [
    "",
    "./assets/icons/",
    "./assets/images/"
  ],
  "ImagesExtensions": [
    ".png",
    ".jpg",
    ".bmp"
  ],
  "__type__": "dashboard.configuration.DashboardConfiguration"
}
```

## Dependencies

- `jAGFx.configuration.ApplicationConfiguration, LoggerConfig, iConfiguration`
- `jAGFx.dependencyInjection.Provider`

## Usage

The configuration is used throughout the dashboard application:

### MainWindow Setup

```python
cfg: DashboardConfiguration = Provider.Resolve(iConfiguration)
main = MainWindow()
# Configuration properties used for window title, icon, etc.
```

### Tray Icon Configuration

```python
self._trayIcon: QSystemTrayIcon = QIcon(getICONPath(cfg.Icon)), self)
self._trayIcon.setToolTip(cfg.Title)
```

## Design Principles

The configuration system follows the project's dependency injection and configuration patterns.

### Extensibility

- Easy to add new properties by extending the class.
- JSON-based configuration allows runtime changes.
- Type hints and validation through the base ApplicationConfiguration.

### Separation of Concerns

- Configuration loading separated from usage.
- Factory pattern allows different loading strategies.
- Interface-based design enables testing and mocking.

## Future Extensions

Potential enhancements to the configuration system:

1. **Validation**: Add schema validation for configuration files.
2. **Environment Overrides**: Support environment variable overrides.
3. **Hot Reloading**: Allow configuration changes without restart.
4. **Multiple Profiles**: Support different configuration profiles.
5. **Encrypted Values**: Support encrypted sensitive configuration values.

## Related Documentation

- [Dashboard Module](readme.md) - Main dashboard documentation
- [jAGFx Configuration](../../jAGFx/configuration/readme.md) - Base configuration system
