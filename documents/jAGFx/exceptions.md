# jAGFx Exceptions Documentation

This document provides detailed information about the exception classes in the jAGFx framework used within the eNuts project. These exceptions follow the project's coding style rules, including type hints, consistent naming conventions, and object-oriented design principles.

## Overview

The jAGFx exceptions module provides a hierarchy of custom exception classes designed to provide detailed error information, including file names, line numbers, and contextual data. All exceptions inherit from the base `jAGException` class and are exported through the `__init__.py` file.

## Exception Hierarchy

```
jAGException (base)
├── ModuleException
├── invalidParameterTypeException
└── parameterRequiredException
```

## Base Exception Class: jAGException

The `jAGException` class serves as the foundation for all custom exceptions in the framework. It automatically captures contextual information about where the exception occurred.

### Properties

- **Message**: The error message (string or list of strings)
- **Filename**: The source file where the exception occurred (string)
- **Attribute**: The function/method name where the exception occurred (string)
- **LineNumber**: The line number where the exception occurred (integer)
- **InnerException**: Any wrapped inner exception (Exception or None)

### Constructor Parameters

- `message`: Error message (str, list[str], or None)
- `inner`: Inner exception to wrap (Exception or None)
- `frame`: Frame object for context (FrameType or None)
- `*args`: Additional positional arguments
- `**kwargs`: Additional keyword arguments

### Usage Example

```python
from jAGFx.exceptions import jAGException

try:
    # Some operation that might fail
    risky_operation()
except Exception as e:
    raise jAGException("Operation failed", inner=e)
```

## ModuleException

The `ModuleException` class extends `jAGException` to provide module-specific error information, including fully qualified names (FQN) for classes and methods.

### Additional Properties

- **FQN**: Fully Qualified Name in format "module.class.method" (string)
- **Message**: The error message (string or list of strings)
- **Filename**: The source file where the exception occurred (string)
- **Attribute**: The function/method name where the exception occurred (string)
- **LineNumber**: The line number where the exception occurred (integer)
- **InnerException**: Any wrapped inner exception (Exception or None)

### Constructor Parameters

- `message`: Error message (str, list[str], or None)
- `inner`: Inner exception to wrap (Exception or None)
- `frame`: Frame object for context (FrameType or None)
- `module`: Module name override (str or None)
- `klass`: Class name override (str or None)
- `member`: Member name override (str or None)
- `*args`: Additional positional arguments
- `**kwargs`: Additional keyword arguments

### Usage Example

```python
from jAGFx.exceptions import ModuleException

class MyClass:
    def my_method(self):
        try:
            # Risky operation
            pass
        except Exception as e:
            raise ModuleException("Method execution failed", inner=e)
```

## Parameter Exceptions

### invalidParameterTypeException

Raised when a parameter has an incorrect type.

#### Constructor Parameters

- `expected`: The expected type (type)
- `provided`: The actual type provided (type)
- `message`: Additional error message (str or None)
- `inner`: Inner exception to wrap (Exception or None)
- `*args`: Additional positional arguments
- `**kwargs`: Additional keyword arguments

#### Properties

- **Message**: The error message (string or list of strings)
- **Filename**: The source file where the exception occurred (string)
- **Attribute**: The function/method name where the exception occurred (string)
- **LineNumber**: The line number where the exception occurred (integer)
- **InnerException**: Any wrapped inner exception (Exception or None)

#### Usage Example

```python
from jAGFx.exceptions import invalidParameterTypeException

def validate_parameter(param):
    if not isinstance(param, int):
        raise invalidParameterTypeException(int, type(param), "Parameter must be an integer")
```

### parameterRequiredException

Raised when a required parameter is missing or None.

#### Constructor Parameters

- `name`: Name of the required parameter (str)
- `message`: Additional error message (str or None)
- `inner`: Inner exception to wrap (Exception or None)
- `*args`: Additional positional arguments
- `**kwargs`: Additional keyword arguments

#### Properties

- **Message**: The error message (string or list of strings)
- **Filename**: The source file where the exception occurred (string)
- **Attribute**: The function/method name where the exception occurred (string)
- **LineNumber**: The line number where the exception occurred (integer)
- **InnerException**: Any wrapped inner exception (Exception or None)

#### Usage Example

```python
from jAGFx.exceptions import parameterRequiredException

def process_data(data):
    if data is None:
        raise parameterRequiredException("data", "Data parameter is required for processing")
```

## Error Handling Best Practices

### Try-Except Blocks

```python
from jAGFx.exceptions import jAGException

try:
    # Code that might raise exceptions
    pass
except jAGException as e:
    # Handle custom exceptions
    logger.error(f"Custom error: {e.Message} in {e.Filename}:{e.LineNumber}")
except Exception as e:
    # Wrap unexpected exceptions
    raise jAGException("Unexpected error", inner=e)
```

### Logging Integration

All exceptions integrate with the project's logging system. The base `jAGException` automatically logs errors using the custom logger. Use the custom logger to record additional exception details:

```python
from utilities import logger

try:
    # Risky operation
    pass
except jAGException as e:
    logger.error(f"Exception occurred: {e.Message}", exc_info=True)
```

## Module Structure

The exceptions are organized in the following files:

- `__exceptionBase.py`: Contains the base `jAGException` class
- `__classError.py`: Contains the `ModuleException` class
- `__parameterExceptions.py`: Contains parameter-specific exceptions
- `__init__.py`: Exports all exception classes

## Dependencies

- `inspect`: For frame inspection and context capture
- `types`: For FrameType annotations
- `typing`: For type hints
- `jAGFx.logger`: For automatic error logging

## Design Principles

- **Inheritance**: All exceptions inherit from `jAGException` for consistency
- **Type Safety**: Extensive use of type hints
- **Context Preservation**: Automatic capture of file, line, and method information
- **Wrapping**: Support for inner exceptions to maintain error chains
- **Flexibility**: Optional parameters allow customization of error messages and context

## Rule Compliance

The exceptions module follows most project coding style rules and naming conventions:

### Compliant Aspects
- **Imports**: Properly grouped with standard library imports first, followed by local imports
- **Type Hints**: Extensive use of type annotations throughout all classes
- **Naming Conventions**:
  - Classes: PascalCase (e.g., `jAGException`, `ModuleException`)
  - Properties: TitleCase (e.g., `Message`, `Filename`)
  - Parameters: camelCase (e.g., `inner`, `frame`)
  - Local Variables: lTitleCase (e.g., `lFrame`, `lMessage`)
  - Private Attributes: _camelCase (e.g., `_filename`, `_inner`)
- **Object-Oriented Design**: Inheritance hierarchy with base exception class
- **Error Handling**: Proper exception chaining with inner exceptions
- **Code Structure**: Clean separation of concerns across multiple files

### Issues Identified

No issues were found in the current codebase. All classes have proper docstrings, correct variable names, and consistent message formatting. The code follows all project coding style rules and naming conventions.
