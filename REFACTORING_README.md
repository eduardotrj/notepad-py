# ViewModel Refactoring

This document describes the refactoring of the large `ViewModel` class into smaller, more focused classes following the Single Responsibility Principle.

## Overview

The original `ViewModel` class was a monolithic class with over 900 lines of code that handled multiple responsibilities including file management, keyboard input, text formatting, search functionality, indexing, view management, and editing operations. This made it difficult to maintain, test, and extend.

## Refactored Architecture

The `ViewModel` class has been refactored into the following specialized manager classes:

### 1. FileManager (`fileManager.py`)
**Responsibility**: Handle all file operations
- File creation, opening, saving, and saving as
- File path management
- File encoding handling
- Error handling for file operations

### 2. KeyboardHandler (`keyboardHandler.py`)
**Responsibility**: Handle keyboard events and shortcuts
- Key press and release events
- Keyboard shortcuts for various operations
- Special key combinations (Alt+R for symbols, Ctrl combinations)
- Delegation to appropriate managers based on key combinations

### 3. TextFormatter (`textFormatter.py`)
**Responsibility**: Handle text formatting and styling
- Text style application
- Title formatting (multiple styles)
- Line decorations
- Date/time insertion
- Mathematical operations on text

### 4. SearchManager (`searchManager.py`)
**Responsibility**: Handle search and replace functionality
- Text searching with case-insensitive options
- Replace functionality
- Navigation between search results
- Search window management
- Search state management

### 5. IndexManager (`indexManager.py`)
**Responsibility**: Handle document indexing and navigation
- Document title detection and indexing
- Index tree management
- Navigation to specific titles
- Index updates when content changes

### 6. ViewManager (`viewManager.py`)
**Responsibility**: Handle view-related operations
- Zoom in/out/reset functionality
- Day/night mode switching
- Document type selection (plain text, markdown, HTML)
- Menu updates

### 7. EditManager (`editManager.py`)
**Responsibility**: Handle basic text editing operations
- Cut, copy, paste operations
- Text selection
- Text deletion
- Auto-save functionality (placeholder)

### 8. ViewModel (refactored)
**Responsibility**: Coordinate between all managers and maintain backward compatibility
- Initialize and coordinate all manager classes
- Provide delegation methods for backward compatibility
- Handle cross-cutting concerns like callbacks
- Manage the overall application lifecycle

## Benefits of the Refactoring

### 1. **Single Responsibility Principle (SRP)**
Each class now has a single, well-defined responsibility, making the code more focused and easier to understand.

### 2. **Improved Maintainability**
- Smaller classes are easier to understand and modify
- Changes to one functionality (e.g., file operations) don't affect other parts
- Easier to locate and fix bugs

### 3. **Better Testability**
- Each manager can be unit tested independently
- Mock dependencies can be easily injected
- Isolated testing of specific functionality

### 4. **Enhanced Extensibility**
- New features can be added to specific managers without affecting others
- New managers can be added for additional functionality
- Easier to implement new file formats, search algorithms, etc.

### 5. **Improved Code Organization**
- Related functionality is grouped together
- Clear separation of concerns
- Better code structure and navigation

### 6. **Backward Compatibility**
- The refactored `ViewModel` maintains all public methods as delegation points
- Existing code that uses `ViewModel` continues to work without changes
- Properties are preserved using Python's `@property` decorator

## Usage

### Before Refactoring
```python
# All functionality was accessed through ViewModel
viewmodel = ViewModel()
viewmodel.open_file()  # File operation
viewmodel.search()     # Search operation
viewmodel.zoom_in()    # View operation
```

### After Refactoring
```python
# Direct access to managers (for new code)
viewmodel = ViewModel()
viewmodel.file_manager.open_file()      # Direct access
viewmodel.search_manager.search()       # Direct access
viewmodel.view_manager.zoom_in()        # Direct access

# Or still use the delegation methods (for compatibility)
viewmodel.open_file()  # Still works via delegation
viewmodel.search()     # Still works via delegation
viewmodel.zoom_in()    # Still works via delegation
```

## File Structure

```
Main/
├── viewmodel.py          # Refactored coordinator class
├── fileManager.py        # File operations
├── keyboardHandler.py    # Keyboard event handling
├── textFormatter.py      # Text formatting and styling
├── searchManager.py      # Search and replace functionality
├── indexManager.py       # Document indexing
├── viewManager.py        # View-related operations
├── editManager.py        # Text editing operations
└── ...                   # Other existing files
```

## Migration Guide

For existing code that uses the `ViewModel` class:

1. **No immediate changes required** - All existing method calls continue to work through delegation
2. **For new development** - Consider using the specific managers directly for better code organization
3. **For testing** - Use individual managers for focused unit testing

## Future Improvements

1. **Dependency Injection**: Consider using a dependency injection framework for better decoupling
2. **Event System**: Implement an event-driven architecture for better communication between managers
3. **Plugin Architecture**: Allow for easy extension through plugin-based managers
4. **Configuration Management**: Add a configuration manager for application settings

## Implementation Notes

- All managers maintain references to the `view` object for UI interactions
- Callbacks are used to notify other managers of state changes (e.g., file changes trigger index updates)
- The keyboard handler delegates to appropriate managers based on key combinations
- Properties in the main `ViewModel` provide access to manager state for backward compatibility

This refactoring significantly improves the codebase structure while maintaining full backward compatibility and providing a foundation for future enhancements.
