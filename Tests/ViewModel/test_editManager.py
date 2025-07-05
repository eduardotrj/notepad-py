import tkinter as tk
from unittest.mock import Mock
from Main.ViewModel.editManager import EditManager


class TestEditManager:
    """Test suite for EditManager class."""

    def test_init(self, mock_view):
        """Test EditManager initialization."""
        manager = EditManager(mock_view)
        
        assert manager.view is mock_view

    def test_cut(self, mock_view):
        """Test cut method."""
        manager = EditManager(mock_view)
        
        manager.cut()
        
        mock_view.text_area.event_generate.assert_called_once_with("<<Cut>>")

    def test_copy(self, mock_view):
        """Test copy method."""
        manager = EditManager(mock_view)
        
        manager.copy()
        
        mock_view.text_area.event_generate.assert_called_once_with("<<Copy>>")

    def test_paste(self, mock_view):
        """Test paste method."""
        manager = EditManager(mock_view)
        
        manager.paste()
        
        mock_view.text_area.event_generate.assert_called_once_with("<<Paste>>")

    def test_select_all_default_event(self, mock_view):
        """Test select_all with default event parameter."""
        manager = EditManager(mock_view)
        
        manager.select_all()
        
        mock_view.text_area.tag_add.assert_called_once_with(
            'sel', '1.0', 'end')

    def test_select_all_with_event_parameter(self, mock_view):
        """Test select_all with explicit event parameter."""
        manager = EditManager(mock_view)
        
        event = Mock()
        manager.select_all(event)
        
        mock_view.text_area.tag_add.assert_called_once_with(
            'sel', '1.0', 'end')

    def test_delete_with_selection(self, mock_view):
        """Test delete method with text selected."""
        manager = EditManager(mock_view)
        
        # Mock successful selection
        mock_view.text_area.selection_get.return_value = "selected text"
        mock_view.text_area.index.return_value = "2.5"
        
        manager.delete()
        
        mock_view.text_area.selection_get.assert_called_once()
        mock_view.text_area.index.assert_called_once_with('sel.first')
        mock_view.text_area.delete.assert_called_once_with(
            'sel.first', 'sel.last'
        )

    def test_delete_with_complex_selection_index(self, mock_view):
        """Test delete method with complex selection index."""
        manager = EditManager(mock_view)
        
        # Mock selection with multi-digit line and column
        mock_view.text_area.selection_get.return_value = "selected text"
        mock_view.text_area.index.return_value = "15.23"
        
        manager.delete()
        
        mock_view.text_area.selection_get.assert_called_once()
        mock_view.text_area.index.assert_called_once_with('sel.first')
        mock_view.text_area.delete.assert_called_once_with(
            'sel.first', 'sel.last'
        )

    def test_delete_without_selection(self, mock_view):
        """Test delete method with no text selected."""
        manager = EditManager(mock_view)
        
        # Mock TclError when no selection
        mock_view.text_area.selection_get.side_effect = tk.TclError(
            "No selection"
        )
        
        # Should not raise exception
        manager.delete()
        
        mock_view.text_area.selection_get.assert_called_once()
        mock_view.text_area.index.assert_not_called()
        mock_view.text_area.delete.assert_not_called()

    def test_delete_empty_selection(self, mock_view):
        """Test delete method with empty selection."""
        manager = EditManager(mock_view)
        
        # Mock empty selection (empty string is falsy)
        mock_view.text_area.selection_get.return_value = ""
        
        manager.delete()
        
        # Should call selection_get but not proceed to delete
        mock_view.text_area.selection_get.assert_called_once()
        # Index and delete should NOT be called since empty string is falsy
        mock_view.text_area.index.assert_not_called()
        mock_view.text_area.delete.assert_not_called()

    def test_auto_save_placeholder(self, mock_view):
        """Test auto_save method (currently a placeholder)."""
        manager = EditManager(mock_view)
        
        time_interval = 300  # 5 minutes
        
        # Should not raise any exception
        result = manager.auto_save(time_interval)
        
        assert result is None

    def test_edit_operations_sequence(self, mock_view):
        """Test sequence of edit operations."""
        manager = EditManager(mock_view)
        
        # Perform a sequence of operations
        manager.copy()
        manager.cut()
        manager.paste()
        manager.select_all()
        
        # Verify all operations were called
        expected_calls = ["<<Copy>>", "<<Cut>>", "<<Paste>>"]
        actual_calls = [
            call[0][0] for call in
            mock_view.text_area.event_generate.call_args_list
        ]
        
        assert actual_calls == expected_calls
        mock_view.text_area.tag_add.assert_called_once_with(
            'sel', '1.0', 'end')

    def test_copy_paste_workflow(self, mock_view):
        """Test typical copy-paste workflow."""
        manager = EditManager(mock_view)
        
        # First select all text
        manager.select_all()
        
        # Then copy
        manager.copy()
        
        # Move cursor and paste
        manager.paste()
        
        # Verify the sequence
        mock_view.text_area.tag_add.assert_called_once_with(
            'sel', '1.0', 'end')
        
        event_calls = mock_view.text_area.event_generate.call_args_list
        assert len(event_calls) == 2
        assert event_calls[0][0][0] == "<<Copy>>"
        assert event_calls[1][0][0] == "<<Paste>>"

    def test_cut_workflow(self, mock_view):
        """Test typical cut workflow."""
        manager = EditManager(mock_view)
        
        # Select text and cut
        manager.select_all()
        manager.cut()
        
        # Verify operations
        mock_view.text_area.tag_add.assert_called_once_with(
            'sel', '1.0', 'end')
        mock_view.text_area.event_generate.assert_called_once_with("<<Cut>>")

    def test_delete_with_different_tcl_errors(self, mock_view):
        """Test delete method with different TclError scenarios."""
        manager = EditManager(mock_view)
        
        # Test different TclError messages
        error_messages = [
            "No selection",
            "Invalid selection",
            "Text widget error"
        ]
        
        for error_msg in error_messages:
            mock_view.text_area.selection_get.side_effect = tk.TclError(
                error_msg
            )
            
            # Should handle all TclErrors gracefully
            manager.delete()
            
            mock_view.text_area.delete.assert_not_called()
            mock_view.text_area.reset_mock()

    def test_multiple_delete_attempts(self, mock_view):
        """Test multiple delete attempts in sequence."""
        manager = EditManager(mock_view)
        
        # First delete - successful
        mock_view.text_area.selection_get.return_value = "text"
        mock_view.text_area.index.return_value = "1.0"
        manager.delete()
        
        # Second delete - no selection
        mock_view.text_area.selection_get.side_effect = tk.TclError()
        manager.delete()
        
        # Third delete - successful again
        mock_view.text_area.selection_get.side_effect = None
        mock_view.text_area.selection_get.return_value = "more text"
        manager.delete()
        
        # Verify delete was called twice (first and third attempts)
        assert mock_view.text_area.delete.call_count == 2

    def test_all_event_generation_methods(self, mock_view):
        """Test all methods that generate events."""
        manager = EditManager(mock_view)
        
        # Test all event-generating methods
        manager.cut()
        manager.copy()
        manager.paste()
        
        # Verify all events were generated
        event_calls = mock_view.text_area.event_generate.call_args_list
        generated_events = [call[0][0] for call in event_calls]
        
        expected_events = ["<<Cut>>", "<<Copy>>", "<<Paste>>"]
        assert generated_events == expected_events

    def test_select_all_multiple_calls(self, mock_view):
        """Test multiple calls to select_all."""
        manager = EditManager(mock_view)
        
        # Call select_all multiple times
        for i in range(3):
            manager.select_all()
        
        # Should be called 3 times with same parameters
        assert mock_view.text_area.tag_add.call_count == 3
        
        for call in mock_view.text_area.tag_add.call_args_list:
            assert call[0] == ('sel', '1.0', 'end')

    def test_error_resilience(self, mock_view):
        """Test that manager is resilient to various errors."""
        manager = EditManager(mock_view)
        
        # Test resilience when text_area methods raise exceptions
        mock_view.text_area.event_generate.side_effect = [
            None,  # First call succeeds
            Exception("Event error"),  # Second call fails
            None   # Third call succeeds
        ]
        
        # First operation should succeed
        manager.cut()
        
        # Second operation should raise exception
        try:
            manager.copy()
            assert False, "Expected exception"
        except Exception as e:
            assert str(e) == "Event error"
        
        # Reset side effect for third operation
        mock_view.text_area.event_generate.side_effect = None
        manager.paste()
        
        # Verify calls were made
        assert mock_view.text_area.event_generate.call_count == 3
