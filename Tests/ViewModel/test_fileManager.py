"""
Tests for FileManager class.
"""
import pytest
from unittest.mock import Mock, patch, mock_open
import os

from Main.ViewModel.fileManager import FileManager


class TestFileManager:
    """Test cases for FileManager class."""
    
    def test_init(self, mock_view):
        """Test FileManager initialization."""
        callback = Mock()
        file_manager = FileManager(mock_view, callback)
        
        assert file_manager.view == mock_view
        assert file_manager.file is None
        assert file_manager.on_file_change_callback == callback
    
    def test_new_file(self, mock_view):
        """Test creating a new file."""
        callback = Mock()
        file_manager = FileManager(mock_view, callback)
        
        file_manager.new_file()
        
        mock_view.set_title.assert_called_once()
        mock_view.text_area.delete.assert_called_once_with(1.0, "end")
        assert file_manager.file is None
        callback.assert_called_once()
    
    def test_new_file_without_callback(self, mock_view):
        """Test creating a new file without callback."""
        file_manager = FileManager(mock_view)
        
        file_manager.new_file()
        
        mock_view.set_title.assert_called_once()
        mock_view.text_area.delete.assert_called_once_with(1.0, "end")
        assert file_manager.file is None
    
    @patch('Main.ViewModel.fileManager.askopenfilename')
    @patch('builtins.open', new_callable=mock_open, read_data="file content")
    @patch('os.path.basename', return_value="test.txt")
    def test_open_file_success(self, mock_basename, mock_file, mock_dialog, mock_view):
        """Test successfully opening a file."""
        mock_dialog.return_value = "test_file.txt"
        callback = Mock()
        file_manager = FileManager(mock_view, callback)
        
        file_manager.open_file()
        
        assert file_manager.file == "test_file.txt"
        mock_view.set_title.assert_called_once_with("test.txt")
        mock_view.text_area.delete.assert_called_once_with(1.0, "end")
        mock_view.text_area.insert.assert_called_once_with(1.0, "file content")
        callback.assert_called_once()
    
    @patch('Main.ViewModel.fileManager.askopenfilename')
    def test_open_file_cancelled(self, mock_dialog, mock_view):
        """Test cancelling file open dialog."""
        mock_dialog.return_value = ""
        file_manager = FileManager(mock_view)
        
        file_manager.open_file()
        
        assert file_manager.file is None
    
    @patch('Main.ViewModel.fileManager.askopenfilename')
    @patch('builtins.open', side_effect=Exception("File error"))
    def test_open_file_error(self, mock_file, mock_dialog, mock_view, capsys):
        """Test handling file open error."""
        mock_dialog.return_value = "test_file.txt"
        file_manager = FileManager(mock_view)
        
        file_manager.open_file()
        
        captured = capsys.readouterr()
        assert "Error opening file" in captured.out
    
    @patch('builtins.open', new_callable=mock_open)
    def test_save_file_existing(self, mock_file, mock_view):
        """Test saving to existing file."""
        file_manager = FileManager(mock_view)
        file_manager.file = "existing_file.txt"
        mock_view.text_area.get.return_value = "content to save"
        
        file_manager.save_file()
        
        mock_file.assert_called_once_with("existing_file.txt", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with("content to save")
    
    @patch('Main.ViewModel.fileManager.FileManager.save_as')
    def test_save_file_new(self, mock_save_as, mock_view):
        """Test saving new file (should call save_as)."""
        file_manager = FileManager(mock_view)
        
        file_manager.save_file()
        
        mock_save_as.assert_called_once()
    
    @patch('builtins.open', side_effect=Exception("Save error"))
    def test_save_file_error(self, mock_file, mock_view, capsys):
        """Test handling save file error."""
        file_manager = FileManager(mock_view)
        file_manager.file = "test_file.txt"
        
        file_manager.save_file()
        
        captured = capsys.readouterr()
        assert "Error saving file" in captured.out
    
    @patch('Main.ViewModel.fileManager.asksaveasfilename')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.basename', return_value="saved_file.txt")
    def test_save_as_success(self, mock_basename, mock_file, mock_dialog, mock_view):
        """Test successfully saving file with new name."""
        mock_dialog.return_value = "new_file.txt"
        mock_view.type_doc_selected = 0
        mock_view.text_area.get.return_value = "content to save"
        file_manager = FileManager(mock_view)
        
        file_manager.save_as()
        
        assert file_manager.file == "new_file.txt"
        mock_file.assert_called_once_with("new_file.txt", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with("content to save")
        mock_view.set_title.assert_called_once_with("saved_file.txt")
    
    @patch('Main.ViewModel.fileManager.asksaveasfilename')
    def test_save_as_cancelled(self, mock_dialog, mock_view):
        """Test cancelling save as dialog."""
        mock_dialog.return_value = ""
        file_manager = FileManager(mock_view)
        
        file_manager.save_as()
        
        assert file_manager.file is None
    
    @patch('Main.ViewModel.fileManager.asksaveasfilename')
    @patch('builtins.open', side_effect=Exception("Save error"))
    def test_save_as_error(self, mock_file, mock_dialog, mock_view, capsys):
        """Test handling save as error."""
        mock_dialog.return_value = "test_file.txt"
        mock_view.type_doc_selected = 0
        file_manager = FileManager(mock_view)
        
        file_manager.save_as()
        
        captured = capsys.readouterr()
        assert "Error saving file" in captured.out
    
    def test_open_recents(self, mock_view):
        """Test open_recents placeholder method."""
        file_manager = FileManager(mock_view)
        
        # Should not raise any exception
        file_manager.open_recents()
    
    def test_get_current_file(self, mock_view):
        """Test getting current file path."""
        file_manager = FileManager(mock_view)
        file_manager.file = "test_file.txt"
        
        assert file_manager.get_current_file() == "test_file.txt"
    
    def test_has_file(self, mock_view):
        """Test checking if file is open."""
        file_manager = FileManager(mock_view)
        
        assert file_manager.has_file() is False
        
        file_manager.file = "test_file.txt"
        assert file_manager.has_file() is True
