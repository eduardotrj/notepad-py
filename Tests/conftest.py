"""
Test configuration and shared fixtures for ViewModel tests.
"""
import pytest
import tkinter as tk
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


@pytest.fixture
def mock_view():
    """Create a mock view object for testing."""
    view = Mock()
    view.text_area = Mock()
    view.index_tree = Mock()
    view.menu_bar = Mock()
    view.bind = Mock()
    view.set_title = Mock()
    view.set_font = Mock()
    view.set_zoom = Mock()
    view.run = Mock()
    view.destroy = Mock()
    view.configure = Mock()
    
    # Mock text area methods
    view.text_area.get = Mock(return_value="sample text")
    view.text_area.delete = Mock()
    view.text_area.insert = Mock()
    view.text_area.index = Mock(return_value="1.0")
    view.text_area.selection_get = Mock(return_value="selected text")
    view.text_area.tag_add = Mock()
    view.text_area.tag_remove = Mock()
    view.text_area.mark_set = Mock()
    view.text_area.see = Mock()
    view.text_area.search = Mock(return_value="1.5")
    view.text_area.event_generate = Mock()
    view.text_area.configure = Mock()
    
    # Mock index tree methods
    view.index_tree.get_children = Mock(return_value=[])
    view.index_tree.delete = Mock()
    view.index_tree.insert = Mock(return_value="item1")
    
    # Mock menu bar methods
    view.menu_bar.entryconfig = Mock()
    
    # View properties
    view.n_font = 12
    view.default_size = 12
    view.day_mode = "🌙"
    view.type_doc_selected = 0
    view.TYPE_DOC = ["Plain Text", "Markdown", "HTML"]
    view._open_file = "Test File"
    
    return view


@pytest.fixture
def mock_model():
    """Create a mock model object for testing."""
    model = Mock()
    model.apply_style = Mock(side_effect=lambda char, style: f"{char}_{style}")
    return model


@pytest.fixture
def mock_instances():
    """Create a mock instances list for testing."""
    return []


@pytest.fixture
def sample_file_path():
    """Sample file path for testing."""
    return "test_file.txt"


@pytest.fixture
def sample_text():
    """Sample text content for testing."""
    return "This is a sample text for testing purposes."


class MockTkinter:
    """Mock tkinter classes and functions."""
    
    class StringVar:
        def __init__(self, value=""):
            self._value = value
        
        def get(self):
            return self._value
        
        def set(self, value):
            self._value = value
    
    INSERT = "insert"
    END = "end"
    SEL = "sel"


# Patch tkinter imports for testing
@pytest.fixture(autouse=True)
def mock_tkinter():
    """Mock tkinter module for all tests."""
    with patch('tkinter.StringVar', MockTkinter.StringVar):
        with patch('tkinter.INSERT', MockTkinter.INSERT):
            with patch('tkinter.END', MockTkinter.END):
                with patch('tkinter.SEL', MockTkinter.SEL):
                    yield


@pytest.fixture
def mock_file_operations():
    """Mock file operations for testing."""
    with patch('builtins.open', create=True) as mock_open:
        with patch('os.path.basename', return_value="test.txt"):
            mock_file = MagicMock()
            mock_file.read.return_value = "file content"
            mock_file.write = Mock()
            mock_file.__enter__.return_value = mock_file
            mock_file.__exit__.return_value = None
            mock_open.return_value = mock_file
            yield mock_open
