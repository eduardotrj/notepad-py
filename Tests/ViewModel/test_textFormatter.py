"""
Tests for TextFormatter class.
"""
from unittest.mock import Mock, patch
from datetime import datetime

from Main.ViewModel.textFormatter import TextFormatter


class TestTextFormatter:
    """Test cases for TextFormatter class."""
    
    def test_init(self, mock_view, mock_model):
        """Test TextFormatter initialization."""
        callback = Mock()
        formatter = TextFormatter(mock_view, mock_model, callback)
        
        assert formatter.view == mock_view
        assert formatter.model == mock_model
        assert formatter.on_text_change_callback == callback
        assert formatter.select_text == ""
    
    def test_take_text_success(self, mock_view, mock_model):
        """Test applying style to selected text."""
        callback = Mock()
        formatter = TextFormatter(mock_view, mock_model, callback)
        
        mock_view.text_area.selection_get.return_value = "hello"
        mock_view.text_area.index.return_value = "1.5"
        
        formatter.take_text("fb")
        
        mock_view.text_area.delete.assert_called_once_with('sel.first', 'sel.last')
        mock_view.text_area.insert.assert_called_once_with("1.5", "h_fbe_fbl_fbl_fbo_fb")
        callback.assert_called_once()
    
    def test_take_text_no_selection(self, mock_view, mock_model):
        """Test applying style when no text is selected."""
        from tkinter import TclError
        formatter = TextFormatter(mock_view, mock_model)
        
        mock_view.text_area.selection_get.side_effect = TclError("No selection")
        
        # Should not raise exception
        formatter.take_text("fb")
    
    def test_print_line_styles(self, mock_view, mock_model):
        """Test printing different line styles."""
        formatter = TextFormatter(mock_view, mock_model)
        mock_view.text_area.index.return_value = "1.0"
        
        # Test different line styles
        for style in range(1, 8):
            formatter.print_line(style)
            mock_view.text_area.insert.assert_called()
        
        # Test invalid style
        formatter.print_line(999)
        # Should not insert anything for invalid style
    
    def test_print_title_big_title(self, mock_view, mock_model):
        """Test creating big title (style 1)."""
        formatter = TextFormatter(mock_view, mock_model)
        
        mock_view.text_area.selection_get.return_value = "Title"
        mock_view.text_area.index.return_value = "1.0"
        
        formatter.print_title(1)
        
        mock_view.text_area.delete.assert_called_once_with('sel.first', 'sel.last')
        mock_view.text_area.insert.assert_called_once()
        # Check that the inserted text contains the title formatting
        call_args = mock_view.text_area.insert.call_args[0]
        assert "Title" in call_args[1]
        assert "▀" in call_args[1]  # Top border
        assert "▄" in call_args[1]  # Bottom border
    
    def test_print_title_bullet_styles(self, mock_view, mock_model):
        """Test creating bullet-style titles (styles 2-7)."""
        callback = Mock()
        formatter = TextFormatter(mock_view, mock_model, callback)
        
        mock_view.text_area.selection_get.return_value = "subtitle"
        mock_view.text_area.index.return_value = "1.0"
        
        # Test each bullet style
        for style in range(2, 8):
            formatter.print_title(style)
            mock_view.text_area.delete.assert_called_with('sel.first', 'sel.last')
            mock_view.text_area.insert.assert_called()
            callback.assert_called()
    
    def test_print_title_delete_style(self, mock_view, mock_model):
        """Test delete style (style 8)."""
        formatter = TextFormatter(mock_view, mock_model)
        
        mock_view.text_area.selection_get.return_value = "■▪●text▄▀░"
        mock_view.text_area.index.return_value = "1.0"
        
        formatter.print_title(8)
        
        # Should remove special characters and convert to lowercase
        call_args = mock_view.text_area.insert.call_args[0]
        assert call_args[1] == "text"
    
    def test_print_title_no_selection(self, mock_view, mock_model):
        """Test print_title when no text is selected."""
        from tkinter import TclError
        formatter = TextFormatter(mock_view, mock_model)
        
        mock_view.text_area.selection_get.side_effect = TclError("No selection")
        
        # Should not raise exception
        formatter.print_title(1)
    
    @patch('Main.ViewModel.textFormatter.datetime')
    def test_print_time(self, mock_datetime, mock_view, mock_model):
        """Test inserting current time."""
        formatter = TextFormatter(mock_view, mock_model)
        
        # Mock datetime
        mock_now = Mock()
        mock_now.strftime.return_value = "12:34 01/01/2024"
        mock_datetime.now.return_value = mock_now
        
        mock_view.text_area.index.return_value = "1.0"
        
        formatter.print_time()
        
        mock_view.text_area.insert.assert_called_once_with("1.0", "12:34 01/01/2024")
    
    def test_do_operations_with_selection(self, mock_view, mock_model):
        """Test do_operations with selected text."""
        formatter = TextFormatter(mock_view, mock_model)
        
        mock_view.text_area.selection_get.return_value = "2+2"
        mock_view.text_area.index.return_value = "1.0"
        
        formatter.do_operations()
        
        mock_view.text_area.delete.assert_called_once_with('sel.first', 'sel.last')
        mock_view.text_area.insert.assert_called_once_with("1.0", "")  # Empty solution for now
    
    def test_do_operations_no_selection(self, mock_view, mock_model):
        """Test do_operations when no text is selected."""
        from tkinter import TclError
        formatter = TextFormatter(mock_view, mock_model)
        
        mock_view.text_area.selection_get.side_effect = TclError("No selection")
        
        # Should not raise exception
        formatter.do_operations()
    
    def test_format_title_style_constants(self, mock_view, mock_model):
        """Test that constants are properly defined."""
        formatter = TextFormatter(mock_view, mock_model)
        
        assert hasattr(formatter, 'INDEX_START')
        assert hasattr(formatter, 'SUB_INDEX')
        assert hasattr(formatter, 'EMPTY_SYMBOL')
        
        assert len(formatter.INDEX_START) > 100  # Should be a long line
        assert formatter.SUB_INDEX == "■ "
        assert formatter.EMPTY_SYMBOL == 'ㅤ'
