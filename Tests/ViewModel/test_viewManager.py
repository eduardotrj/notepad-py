from unittest.mock import Mock, patch
from Main.View.viewManager import ViewManager


class TestViewManager:
    """Test suite for ViewManager class."""

    def test_init(self, mock_view):
        """Test ViewManager initialization."""
        manager = ViewManager(mock_view)
        
        assert manager.view is mock_view

    def test_zoom_in_normal_case(self, mock_view):
        """Test zoom_in with normal font size."""
        mock_view.n_font = 12
        manager = ViewManager(mock_view)
        
        manager.zoom_in()
        
        assert mock_view.n_font == 13
        mock_view.set_font.assert_called_once_with(13)
        mock_view.set_zoom.assert_called_once_with(13)

    def test_zoom_in_with_event_parameter(self, mock_view):
        """Test zoom_in with event parameter."""
        mock_view.n_font = 10
        manager = ViewManager(mock_view)
        
        event = Mock()
        manager.zoom_in(event)
        
        assert mock_view.n_font == 11
        mock_view.set_font.assert_called_once_with(11)
        mock_view.set_zoom.assert_called_once_with(11)

    def test_zoom_in_at_maximum(self, mock_view):
        """Test zoom_in when already at maximum font size."""
        mock_view.n_font = 32  # Maximum size
        manager = ViewManager(mock_view)
        
        manager.zoom_in()
        
        # Should not increase beyond 32
        assert mock_view.n_font == 32
        mock_view.set_font.assert_called_once_with(32)
        mock_view.set_zoom.assert_called_once_with(32)

    def test_zoom_in_near_maximum(self, mock_view):
        """Test zoom_in when one step away from maximum."""
        mock_view.n_font = 31
        manager = ViewManager(mock_view)
        
        manager.zoom_in()
        
        assert mock_view.n_font == 32
        mock_view.set_font.assert_called_once_with(32)
        mock_view.set_zoom.assert_called_once_with(32)

    def test_zoom_out_normal_case(self, mock_view):
        """Test zoom_out with normal font size."""
        mock_view.n_font = 12
        manager = ViewManager(mock_view)
        
        manager.zoom_out()
        
        assert mock_view.n_font == 11
        mock_view.set_font.assert_called_once_with(11)
        mock_view.set_zoom.assert_called_once_with(11)

    def test_zoom_out_with_event_parameter(self, mock_view):
        """Test zoom_out with event parameter."""
        mock_view.n_font = 15
        manager = ViewManager(mock_view)
        
        event = Mock()
        manager.zoom_out(event)
        
        assert mock_view.n_font == 14
        mock_view.set_font.assert_called_once_with(14)
        mock_view.set_zoom.assert_called_once_with(14)

    def test_zoom_out_at_minimum(self, mock_view):
        """Test zoom_out when already at minimum font size."""
        mock_view.n_font = 0  # Minimum size
        manager = ViewManager(mock_view)
        
        manager.zoom_out()
        
        # Should not decrease below 0
        assert mock_view.n_font == 0
        mock_view.set_font.assert_called_once_with(0)
        mock_view.set_zoom.assert_called_once_with(0)

    def test_zoom_out_near_minimum(self, mock_view):
        """Test zoom_out when one step away from minimum."""
        mock_view.n_font = 1
        manager = ViewManager(mock_view)
        
        manager.zoom_out()
        
        assert mock_view.n_font == 0
        mock_view.set_font.assert_called_once_with(0)
        mock_view.set_zoom.assert_called_once_with(0)

    def test_zoom_reset_normal_case(self, mock_view):
        """Test zoom_reset with normal scenario."""
        mock_view.n_font = 20
        mock_view.default_size = 12
        manager = ViewManager(mock_view)
        
        manager.zoom_reset()
        
        assert mock_view.n_font == 12
        mock_view.set_font.assert_called_once_with(12)
        mock_view.set_zoom.assert_called_once_with(12)

    def test_zoom_reset_with_event_parameter(self, mock_view):
        """Test zoom_reset with event parameter."""
        mock_view.n_font = 8
        mock_view.default_size = 14
        manager = ViewManager(mock_view)
        
        event = Mock()
        manager.zoom_reset(event)
        
        assert mock_view.n_font == 14
        mock_view.set_font.assert_called_once_with(14)
        mock_view.set_zoom.assert_called_once_with(14)

    def test_zoom_reset_already_at_default(self, mock_view):
        """Test zoom_reset when already at default size."""
        mock_view.n_font = 12
        mock_view.default_size = 12
        manager = ViewManager(mock_view)
        
        manager.zoom_reset()
        
        assert mock_view.n_font == 12
        mock_view.set_font.assert_called_once_with(12)
        mock_view.set_zoom.assert_called_once_with(12)

    def test_switch_mode_from_night_to_day(self, mock_view):
        """Test switch_mode from night mode to day mode."""
        mock_view.day_mode = "🌙"  # Night mode
        mock_view.text_area = Mock()
        mock_view.menu_bar = Mock()
        
        manager = ViewManager(mock_view)
        
        manager.switch_mode()
        
        # Should switch to day mode
        mock_view.text_area.configure.assert_called_once_with(
            bg="#2A2F2D", fg="white"
        )
        assert mock_view.day_mode == "🌞"
        mock_view.menu_bar.entryconfig.assert_called_once_with(7, label="🌞")

    def test_switch_mode_from_day_to_night(self, mock_view):
        """Test switch_mode from day mode to night mode."""
        mock_view.day_mode = "🌞"  # Day mode
        mock_view.text_area = Mock()
        mock_view.menu_bar = Mock()
        
        manager = ViewManager(mock_view)
        
        manager.switch_mode()
        
        # Should switch to night mode
        mock_view.text_area.configure.assert_called_once_with(
            bg="white", fg="black"
        )
        assert mock_view.day_mode == "🌙"
        mock_view.menu_bar.entryconfig.assert_called_once_with(7, label="🌙")

    def test_switch_mode_with_event_parameter(self, mock_view):
        """Test switch_mode with event parameter."""
        mock_view.day_mode = "🌙"
        mock_view.text_area = Mock()
        mock_view.menu_bar = Mock()
        
        manager = ViewManager(mock_view)
        
        event = Mock()
        manager.switch_mode(event)
        
        mock_view.text_area.configure.assert_called_once_with(
            bg="#2A2F2D", fg="white"
        )
        assert mock_view.day_mode == "🌞"

    def test_select_type_plaintext(self, mock_view):
        """Test select_type_plaintext method."""
        manager = ViewManager(mock_view)
        
        with patch.object(manager, 'change_menu_type') as mock_change:
            manager.select_type_plaintext()
            
            assert mock_view.type_doc_selected == 0
            mock_change.assert_called_once()

    def test_select_type_plaintext_with_event(self, mock_view):
        """Test select_type_plaintext with event parameter."""
        manager = ViewManager(mock_view)
        
        event = Mock()
        
        with patch.object(manager, 'change_menu_type') as mock_change:
            manager.select_type_plaintext(event)
            
            assert mock_view.type_doc_selected == 0
            mock_change.assert_called_once()

    def test_select_type_markdown(self, mock_view):
        """Test select_type_markdown method."""
        manager = ViewManager(mock_view)
        
        with patch.object(manager, 'change_menu_type') as mock_change:
            manager.select_type_markdown()
            
            assert mock_view.type_doc_selected == 1
            mock_change.assert_called_once()

    def test_select_type_markdown_with_event(self, mock_view):
        """Test select_type_markdown with event parameter."""
        manager = ViewManager(mock_view)
        
        event = Mock()
        
        with patch.object(manager, 'change_menu_type') as mock_change:
            manager.select_type_markdown(event)
            
            assert mock_view.type_doc_selected == 1
            mock_change.assert_called_once()

    def test_select_type_html(self, mock_view):
        """Test select_type_html method."""
        manager = ViewManager(mock_view)
        
        with patch.object(manager, 'change_menu_type') as mock_change:
            manager.select_type_html()
            
            assert mock_view.type_doc_selected == 2
            mock_change.assert_called_once()

    def test_select_type_html_with_event(self, mock_view):
        """Test select_type_html with event parameter."""
        manager = ViewManager(mock_view)
        
        event = Mock()
        
        with patch.object(manager, 'change_menu_type') as mock_change:
            manager.select_type_html(event)
            
            assert mock_view.type_doc_selected == 2
            mock_change.assert_called_once()

    def test_change_menu_type(self, mock_view):
        """Test change_menu_type method."""
        mock_view.type_doc_selected = 1
        mock_view.TYPE_DOC = ["Plain Text", "Markdown", "HTML"]
        mock_view.menu_bar = Mock()
        
        manager = ViewManager(mock_view)
        
        manager.change_menu_type()
        
        mock_view.menu_bar.entryconfig.assert_called_once_with(
            2, label="Markdown"
        )

    def test_change_menu_type_different_selections(self, mock_view):
        """Test change_menu_type with different document types."""
        mock_view.TYPE_DOC = ["Plain Text", "Markdown", "HTML"]
        mock_view.menu_bar = Mock()
        
        manager = ViewManager(mock_view)
        
        # Test each document type
        for i, doc_type in enumerate(mock_view.TYPE_DOC):
            mock_view.type_doc_selected = i
            manager.change_menu_type()
            
            mock_view.menu_bar.entryconfig.assert_called_with(2, label=doc_type)

    def test_document_type_workflow(self, mock_view):
        """Test complete workflow of changing document types."""
        mock_view.TYPE_DOC = ["Plain Text", "Markdown", "HTML"]
        mock_view.menu_bar = Mock()
        
        manager = ViewManager(mock_view)
        
        # Start with plaintext
        manager.select_type_plaintext()
        assert mock_view.type_doc_selected == 0
        
        # Switch to markdown
        manager.select_type_markdown()
        assert mock_view.type_doc_selected == 1
        
        # Switch to HTML
        manager.select_type_html()
        assert mock_view.type_doc_selected == 2
        
        # Verify menu was updated for the last change
        mock_view.menu_bar.entryconfig.assert_called_with(2, label="HTML")

    def test_zoom_workflow(self, mock_view):
        """Test complete zoom workflow."""
        mock_view.n_font = 12
        mock_view.default_size = 12
        
        manager = ViewManager(mock_view)
        
        # Zoom in twice
        manager.zoom_in()
        assert mock_view.n_font == 13
        
        manager.zoom_in()
        assert mock_view.n_font == 14
        
        # Zoom out once
        manager.zoom_out()
        assert mock_view.n_font == 13
        
        # Reset zoom
        manager.zoom_reset()
        assert mock_view.n_font == 12

    def test_mode_switching_workflow(self, mock_view):
        """Test complete mode switching workflow."""
        mock_view.day_mode = "🌙"
        mock_view.text_area = Mock()
        mock_view.menu_bar = Mock()
        
        manager = ViewManager(mock_view)
        
        # Switch to day mode
        manager.switch_mode()
        assert mock_view.day_mode == "🌞"
        
        # Switch back to night mode
        manager.switch_mode()
        assert mock_view.day_mode == "🌙"
