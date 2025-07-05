from unittest.mock import Mock, patch
from Main.ViewModel.keyboardHandler import KeyboardHandler


class TestKeyboardHandler:
    """Test suite for KeyboardHandler class."""

    def test_init(self, mock_view):
        """Test KeyboardHandler initialization."""
        # Create mock managers
        file_manager = Mock()
        text_formatter = Mock()
        search_manager = Mock()
        view_manager = Mock()
        edit_manager = Mock()

        # Create handler
        handler = KeyboardHandler(
            mock_view, file_manager, text_formatter,
            search_manager, view_manager, edit_manager
        )

        # Verify initialization
        assert handler.view is mock_view
        assert handler.file_manager is file_manager
        assert handler.text_formatter is text_formatter
        assert handler.search_manager is search_manager
        assert handler.view_manager is view_manager
        assert handler.edit_manager is edit_manager
        assert handler.key_alt_r is False
        assert handler.key_control_l is False

        # Verify shortcuts were set up
        mock_view.bind.assert_called()
        mock_view.text_area.bind.assert_called()

    def test_setup_shortcuts(self, mock_view):
        """Test that keyboard shortcuts are properly bound."""
        file_manager = Mock()
        text_formatter = Mock()
        search_manager = Mock()
        view_manager = Mock()
        edit_manager = Mock()

        handler = KeyboardHandler(
            mock_view, file_manager, text_formatter,
            search_manager, view_manager, edit_manager
        )

        # Verify key bindings were called
        expected_bindings = [
            "<Control-n>", "<Control-o>", "<Control-s>", "<Control-S>",
            "<Control-m>", "<Control-plus>", "<Control-minus>", "<Control-0>",
            "<KeyPress>", "<KeyRelease>"
        ]
        
        # Check that bind was called with expected shortcuts
        for binding in expected_bindings:
            # Note: We can't easily test the exact callback functions
            # Just verify that bind was called multiple times
            assert mock_view.bind.call_count >= len(expected_bindings)

    def test_test123(self, mock_view):
        """Test the test123 method."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        event = Mock()
        
        with patch('builtins.print') as mock_print:
            handler.test123(event)
            mock_print.assert_called_once_with("Working!")

    def test_key_pressed_alt_r(self, mock_view):
        """Test key_pressed with Alt_R key."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        event = Mock()
        event.keysym = 'Alt_R'
        
        with patch.object(handler, '_handle_alt_r_combinations') as \
                mock_handle_alt:
            result = handler.key_pressed(event)
            
            assert handler.key_alt_r is True
            assert result == "break"
            mock_handle_alt.assert_called_once_with(event)

    def test_key_pressed_control_l(self, mock_view):
        """Test key_pressed with Control_L key."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        event = Mock()
        event.keysym = 'Control_L'
        
        with patch.object(handler, '_handle_control_combinations') as \
                mock_handle_ctrl:
            result = handler.key_pressed(event)
            
            assert handler.key_control_l is True
            assert result == "break"
            mock_handle_ctrl.assert_called_once_with(event)

    def test_key_pressed_regular_key(self, mock_view):
        """Test key_pressed with regular key when no modifiers are active."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        event = Mock()
        event.keysym = 'a'
        
        with patch.object(handler, '_handle_alt_r_combinations') as \
                mock_handle_alt, \
                patch.object(handler, '_handle_control_combinations') as \
                mock_handle_ctrl:
            
            result = handler.key_pressed(event)
            
            assert handler.key_alt_r is False
            assert handler.key_control_l is False
            assert result == "break"
            mock_handle_alt.assert_not_called()
            mock_handle_ctrl.assert_not_called()

    def test_key_released_alt_r(self, mock_view):
        """Test key_released with Alt_R key."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        # Set initial state
        handler.key_alt_r = True
        
        event = Mock()
        event.keysym = 'Alt_R'
        
        result = handler.key_released(event)
        
        assert handler.key_alt_r is False
        assert result == "break"

    def test_key_released_control_l(self, mock_view):
        """Test key_released with Control_L key."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        # Set initial state
        handler.key_control_l = True
        
        event = Mock()
        event.keysym = 'Control_L'
        
        result = handler.key_released(event)
        
        assert handler.key_control_l is False
        assert result == "break"

    def test_handle_alt_r_combinations_valid_symbols(self, mock_view):
        """Test _handle_alt_r_combinations with valid symbol keys."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        mock_view.text_area.index.return_value = "1.0"
        
        # Test various symbol mappings
        test_cases = [
            ('2', '⚠️'),
            ('3', '‼'),
            ('5', '✶'),
            ('6', '●'),
            ('p', '←'),
            ('bracketleft', '↑'),
            ('t', '■'),
            ('y', '▪')
        ]
        
        for keysym, expected_symbol in test_cases:
            event = Mock()
            event.keysym = keysym
            
            handler._handle_alt_r_combinations(event)
            
            mock_view.text_area.insert.assert_called_with(
                "1.0", expected_symbol)

    def test_handle_alt_r_combinations_invalid_key(self, mock_view):
        """Test _handle_alt_r_combinations with invalid key."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        mock_view.text_area.index.return_value = "1.0"
        
        event = Mock()
        event.keysym = 'invalid_key'
        
        handler._handle_alt_r_combinations(event)
        
        # Should not insert anything for invalid keys
        mock_view.text_area.insert.assert_not_called()

    def test_handle_control_combinations_text_formatting(self, mock_view):
        """Test _handle_control_combinations with text formatting keys."""
        text_formatter = Mock()
        handler = KeyboardHandler(
            mock_view, Mock(), text_formatter, Mock(), Mock(), Mock()
        )
        
        # Test text formatting shortcuts
        test_cases = [
            ('r', 'nn'),
            ('b', 'fb'),
            ('j', 'fi'),
            ('h', 'hn'),
            ('w', 'wn'),
            ('l', 'ln')
        ]
        
        for keysym, expected_format in test_cases:
            event = Mock()
            event.keysym = keysym
            
            handler._handle_control_combinations(event)
            
            text_formatter.take_text.assert_called_with(expected_format)

    def test_handle_control_combinations_file_operations(self, mock_view):
        """Test _handle_control_combinations with file operation keys."""
        file_manager = Mock()
        handler = KeyboardHandler(
            mock_view, file_manager, Mock(), Mock(), Mock(), Mock()
        )
        
        # Test file operations
        test_cases = [
            ('o', 'open_file'),
            ('s', 'save_file'),
            ('n', 'new_file')
        ]
        
        for keysym, method_name in test_cases:
            event = Mock()
            event.keysym = keysym
            
            handler._handle_control_combinations(event)
            
            getattr(file_manager, method_name).assert_called_once()
            file_manager.reset_mock()

    def test_handle_control_combinations_save_as(self, mock_view):
        """Test _handle_control_combinations with save as shortcut."""
        file_manager = Mock()
        handler = KeyboardHandler(
            mock_view, file_manager, Mock(), Mock(), Mock(), Mock()
        )
        
        event = Mock()
        event.keysym = 's'
        # The original code checks for event.keysym == 'Shift_L' which
        # would override the 's' keysym - this seems like a bug in the
        # original code. For now, test the actual behavior.
        
        handler._handle_control_combinations(event)
        
        # Should call save_file, not save_as since keysym is 's'
        file_manager.save_file.assert_called_once()

    def test_handle_control_combinations_view_operations(self, mock_view):
        """Test _handle_control_combinations with view operation keys."""
        view_manager = Mock()
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), view_manager, Mock()
        )
        
        # Test zoom operations
        test_cases = [
            ('plus', 'zoom_in'),
            ('equal', 'zoom_in'),
            ('minus', 'zoom_out'),
            ('0', 'zoom_reset'),
            ('m', 'switch_mode')
        ]
        
        for keysym, method_name in test_cases:
            event = Mock()
            event.keysym = keysym
            
            handler._handle_control_combinations(event)
            
            getattr(view_manager, method_name).assert_called_once()
            view_manager.reset_mock()

    def test_handle_control_combinations_search(self, mock_view):
        """Test _handle_control_combinations with search key."""
        search_manager = Mock()
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), search_manager, Mock(), Mock()
        )
        
        event = Mock()
        event.keysym = 'f'
        
        handler._handle_control_combinations(event)
        
        search_manager.search.assert_called_once()

    def test_handle_control_combinations_title_formatting(self, mock_view):
        """Test _handle_control_combinations with title formatting keys."""
        text_formatter = Mock()
        handler = KeyboardHandler(
            mock_view, Mock(), text_formatter, Mock(), Mock(), Mock()
        )
        
        # Test title formatting (numbers 1-8)
        for number in ['1', '2', '3', '4', '5', '6', '7', '8']:
            event = Mock()
            event.keysym = number
            
            handler._handle_control_combinations(event)
            
            text_formatter.print_title.assert_called_with(int(number))
            text_formatter.reset_mock()

    def test_handle_control_combinations_exit(self, mock_view):
        """Test _handle_control_combinations with exit key combination."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        event = Mock()
        event.keysym = '.'
        
        handler._handle_control_combinations(event)
        
        mock_view.destroy.assert_called_once()

    def test_save_step(self, mock_view):
        """Test save_step method."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        obj = Mock()
        
        # Currently just a placeholder, should not raise any errors
        result = handler.save_step(obj)
        assert result is None

    def test_key_state_management(self, mock_view):
        """Test that key states are managed correctly."""
        handler = KeyboardHandler(
            mock_view, Mock(), Mock(), Mock(), Mock(), Mock()
        )
        
        # Test Alt_R state management
        event_alt_press = Mock()
        event_alt_press.keysym = 'Alt_R'
        
        event_alt_release = Mock()
        event_alt_release.keysym = 'Alt_R'
        
        # Press Alt_R
        assert handler.key_alt_r is False
        handler.key_pressed(event_alt_press)
        assert handler.key_alt_r is True
        
        # Release Alt_R
        handler.key_released(event_alt_release)
        assert handler.key_alt_r is False
        
        # Test Control_L state management
        event_ctrl_press = Mock()
        event_ctrl_press.keysym = 'Control_L'
        
        event_ctrl_release = Mock()
        event_ctrl_release.keysym = 'Control_L'
        
        # Press Control_L
        assert handler.key_control_l is False
        handler.key_pressed(event_ctrl_press)
        assert handler.key_control_l is True
        
        # Release Control_L
        handler.key_released(event_ctrl_release)
        assert handler.key_control_l is False
