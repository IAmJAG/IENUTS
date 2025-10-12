# eNuts
evolving Neural user training system

## Overview
eNuts - evolving Neural user training system is an AI driven aims to emitate a person gaming habit(bot). This is not simply a bot. This aims to understand a persons behavior and mannerism through understanding how a person reacts to the ingame situations.

## Libraries/Modules

- **eNuts**: Main application
- **dashboard**: Landing applications, this will be a laucher of the applications and tools.
- **jAGFx**: A multi-purpos library aims to contain all the basic and PnP
- **jAGUI**: A UI wrapper. Currently only supports PySide6. This contains custom components/widgets as well as tools to help the UI components
- **utilities**: This contains application local/specific modules/functions. And all modules and functions that does not fit, or caused issue(circular issues for example) from other libraries.
- **vannon**: A video annotator tools to help enuts gather data for AI training

## Project Structure

```
eNuts/
├── .kilocode/          # Custom tooling and project rules
├── .vscode/            # VS Code configuration
├── assets/             # Static assets
│   ├── fonts/          # Font files (.ttf)
│   ├── icons/          # Icon files (.png)
│   └── styles/         # Stylesheets (.qss)
├── config/             # Configuration files
│   ├── appconfig.json
│   ├── logger.cfg
│   └── vannon/
├── documents/          # Documentation
│   ├── enuts.md        # Main project overview
│   ├── dashboard/
│   ├── jAGUI/
│   └── jAGUI/components/
├── src/                # Source code
│   ├── main.py         # Main entry point
│   ├── dashboard/      # Dashboard application
│   ├── jAGFx/          # Framework library
│   ├── jAGUI/          # UI library
│   ├── poc/            # Proof of concept
│   └── utilities/      # Utility modules
└── README.md (if exists)
```
