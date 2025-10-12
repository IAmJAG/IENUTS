# Coding Style Rules

This document defines the coding style rules used throughout the vAnnon project codebase.

## General Rules

All code in this project must follow these coding style rules to ensure consistency, readability, and maintainability.

---

## Specific Conventions

### Imports
- Group imports with section separators: `# ==================================================================================`
- Order: Standard library imports first, then third-party (e.g., PySide6), then local imports.
- Separate groups with the separator comment.
- Import grouping with separators is enforced in most files; ensure all new code follows this pattern.

### Code Structure
- Use object-oriented design with inheritance, decorators, and design patterns (e.g., Dependency Injection, Singleton, Factory).
- Employ decorators extensively for functionality like `@processMarker(True, True)`, `@OverloadDispatcher`, `@benchmark`.
- Use properties for encapsulation of class attributes.
- Implement interfaces/contracts (e.g., `iConfiguration`, `iProvider`) for modularity.

### Type Hints
- Use type hints extensively for function parameters, return types, and variables (e.g., `def main(args: list = sys.argv)`, `lLayout: QBoxLayout`).
- Ensure type annotations are accurate and up-to-date.

### Error Handling
- Use try-except blocks with specific exception types.
- Log errors using the custom logger (debug, info, warning, error, critical, fatal).
- Handle platform-specific code appropriately (e.g., Windows-specific calls).

### Indentation and Spacing
- Use 4 spaces for indentation.
- Maintain consistent spacing around operators and after commas.

### Comments and Docstrings
- Use minimal comments; rely on self-documenting code.
- Include docstrings for decorators and key functions where necessary.
- Use section separators for logical code blocks.
- Do not include the LOGS directory in project documentation structures.

### Constants and Variables
- Adhere strictly to naming conventions for prefixes (e.g., `l` for locals, `C_` for constants).
- Avoid global variables; use dependency injection instead.

### GUI and Framework Usage
- Use PySide6 (Qt) for UI components with custom jAGUI wrappers.
- Implement layouts, events, and icons consistently.
- Process QSS (Qt Style Sheets) with regex for variables and placeholders.

### Patterns and Best Practices
- Implement overloading via decorators.
- Use lifecycle management for dependencies (Singleton, Transient, Factory).
- Benchmark performance-critical functions with decorators.
- Load configurations from JSON files.
- Ensure cross-platform compatibility where applicable.

---

## Enforcement

- All new code must follow these style rules.
- Code reviews will check for style compliance.
- Import grouping with separators is not yet universally enforced but will be addressed moving forward.
- Automated tools may be used to validate style in the future.

## Rationale

These rules promote:
- **Consistency**: Uniform style across the codebase.
- **Readability**: Clear, maintainable code structure.
- **Maintainability**: Easier to understand, modify, and extend.
- **Quality**: Robust error handling and type safety.
