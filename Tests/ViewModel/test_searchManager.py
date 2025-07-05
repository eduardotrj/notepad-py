"""
Tests for SearchManager class.
"""
from unittest.mock import Mock, patch

from Main.ViewModel.searchManager import SearchManager


class TestSearchManager:
    """Test cases for SearchManager class."""
    
    def test_init(self, mock_view, mock_instances):
        """Test SearchManager initialization."""
        search_manager = SearchManager(mock_view, mock_instances)
        
        assert search_manager.view == mock_view
        assert search_manager.instances == mock_instances
        assert search_manager.search_view is None
        assert search_manager.search_word == ""
        assert search_manager.replace_word == ""
        assert search_manager.total_matches == 0
        assert search_manager.tag_position == 0
    
    def test_search_new_window_simple(self, mock_view, mock_instances):
        """Test creating new search window (simplified test)."""
        search_manager = SearchManager(mock_view, mock_instances)
        
        # Patch all the dependencies
        with patch('Main.ViewModel.searchManager.tk.StringVar') as mock_sv:
            with patch('Main.ViewModel.searchManager.ExtraWindow') as mock_ew:
                with patch('builtins.isinstance', return_value=False):
                    mock_extra_instance = Mock()
                    mock_ew.return_value = mock_extra_instance
                    
                    search_manager.search()
                    
                    # Should create StringVar instances
                    assert mock_sv.call_count == 3
                    
                    # Should create new ExtraWindow
                    mock_ew.assert_called_once_with(search_manager, "Search")
                    # Should add to instances
                    assert mock_extra_instance in search_manager.instances
    
    def test_search_existing_window_simple(self, mock_view, mock_instances):
        """Test focusing existing search window (simplified test)."""
        search_manager = SearchManager(mock_view, mock_instances)
        
        # Mock existing search view
        mock_search_view = Mock()
        search_manager.search_view = mock_search_view
        
        with patch('Main.ViewModel.searchManager.tk.StringVar'):
            with patch('builtins.isinstance', return_value=True):
                search_manager.search()
                
                mock_search_view.focus_search.assert_called_once()
    
    def test_search_text_with_replace(self, mock_view, mock_instances):
        """Test searching text with replace enabled."""
        search_manager = SearchManager(mock_view, mock_instances)
        
        # Setup mocks
        search_manager.input_search = Mock()
        search_manager.input_search.get.return_value = "test"
        search_manager.input_replace = Mock()
        search_manager.input_replace.get.return_value = "replace"
        search_manager.enable_replace = Mock()
        search_manager.enable_replace.get.return_value = 'true'
        search_manager.total_matches = 1
        search_manager.replace_text = Mock()
        search_manager.search_all = Mock(return_value=1)
        search_manager.select_tag = Mock()
        
        search_manager.search_text()
        
        search_manager.replace_text.assert_called_once()
        search_manager.search_all.assert_called_once()
        search_manager.select_tag.assert_called_once()
    
    def test_search_text_no_results(self, mock_view, mock_instances):
        """Test searching text with no results."""
        with patch('Main.ViewModel.searchManager.MessageWindow') as mock_msg:
            search_manager = SearchManager(mock_view, mock_instances)
            
            search_manager.input_search = Mock()
            search_manager.input_search.get.return_value = "test"
            search_manager.input_replace = Mock()
            search_manager.input_replace.get.return_value = ""
            search_manager.search_all = Mock(return_value=0)
            
            search_manager.search_text()
            
            mock_msg.show_message.assert_called_once_with(
                "Not results found", "warning"
            )
    
    def test_search_all_success(self, mock_view, mock_instances):
        """Test searching all occurrences successfully."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.search_word = "test"
        
        # Mock text area search to return positions
        mock_view.text_area.search.side_effect = ["1.0", "2.0", None]
        
        result = search_manager.search_all()
        
        assert result == 2
        assert len(search_manager.search_list) == 2
        assert len(search_manager.search_list_idx) == 2
    
    def test_search_all_no_matches(self, mock_view, mock_instances):
        """Test searching all with no matches."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.search_word = "notfound"
        
        mock_view.text_area.search.return_value = None
        
        result = search_manager.search_all()
        
        assert result == 0
        assert len(search_manager.search_list) == 0
    
    def test_select_tag_with_results(self, mock_view, mock_instances):
        """Test selecting tag with search results."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.search_list = ["1.4", "2.4"]
        search_manager.search_list_idx = ["1.0", "2.0"]
        search_manager.tag_position = 0
        search_manager.search_view = Mock()
        
        search_manager.select_tag()
        
        mock_view.text_area.tag_remove.assert_called_once()
        mock_view.text_area.tag_add.assert_called_once_with(
            "sel", "1.0", "1.4")
        mock_view.text_area.mark_set.assert_called_once()
        mock_view.text_area.see.assert_called_once()
    
    def test_select_tag_no_results(self, mock_view, mock_instances):
        """Test selecting tag with no search results."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.search_list = []
        search_manager.search_view = Mock()
        
        search_manager.select_tag()
        
        assert search_manager.total_matches == 0
        assert search_manager.tag_position == 0
    
    def test_replace_text(self, mock_view, mock_instances):
        """Test replacing current search result."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.search_list = ["1.4"]
        search_manager.search_list_idx = ["1.0"]
        search_manager.tag_position = 0
        search_manager.replace_word = "replacement"
        
        search_manager.replace_text()
        
        mock_view.text_area.delete.assert_called_once_with("1.0", "1.4")
        mock_view.text_area.insert.assert_called_once_with(
            "1.0", "replacement")
    
    def test_next_tag_with_results(self, mock_view, mock_instances):
        """Test moving to next tag."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.search_list = ["1.4", "2.4"]
        search_manager.total_matches = 2
        search_manager.tag_position = 0
        search_manager.select_tag = Mock()
        
        search_manager.next_tag()
        
        assert search_manager.tag_position == 1
        search_manager.select_tag.assert_called_once()
    
    def test_next_tag_wrap_around(self, mock_view, mock_instances):
        """Test next tag wrapping around to beginning."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.search_list = ["1.4", "2.4"]
        search_manager.total_matches = 2
        search_manager.tag_position = 1  # Last position
        search_manager.select_tag = Mock()
        
        search_manager.next_tag()
        
        assert search_manager.tag_position == 0  # Should wrap to beginning
        search_manager.select_tag.assert_called_once()
    
    def test_last_tag_with_results(self, mock_view, mock_instances):
        """Test moving to previous tag."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.search_list = ["1.4", "2.4"]
        search_manager.total_matches = 2
        search_manager.tag_position = 1
        search_manager.select_tag = Mock()
        
        search_manager.last_tag()
        
        assert search_manager.tag_position == 0
        search_manager.select_tag.assert_called_once()
    
    def test_last_tag_wrap_around(self, mock_view, mock_instances):
        """Test previous tag wrapping around to end."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.search_list = ["1.4", "2.4"]
        search_manager.total_matches = 2
        search_manager.tag_position = 0  # First position
        search_manager.select_tag = Mock()
        
        search_manager.last_tag()
        
        assert search_manager.tag_position == 1  # Should wrap to end
        search_manager.select_tag.assert_called_once()
    
    def test_show_replace_enable(self, mock_view, mock_instances):
        """Test showing replace option."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.enable_replace = Mock()
        search_manager.enable_replace.get.return_value = 'true'
        search_manager.search_view = Mock()
        
        search_manager.show_replace()
        
        search_manager.search_view.add_replace_option.assert_called_once()
    
    def test_show_replace_disable(self, mock_view, mock_instances):
        """Test hiding replace option."""
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.enable_replace = Mock()
        search_manager.enable_replace.get.return_value = 'false'
        search_manager.search_view = Mock()
        
        search_manager.show_replace()
        
        search_manager.search_view.remove_replace_option.assert_called_once()
    
    @patch('Main.ViewModel.searchManager.gc.collect')
    def test_delete_instance(self, mock_gc, mock_view, mock_instances):
        """Test deleting search instance."""
        from Main.View.extraView import ExtraWindow
        
        search_manager = SearchManager(mock_view, mock_instances)
        search_manager.search_view = Mock(spec=ExtraWindow)
        
        search_manager.delete_instance(search_manager.search_view)
        
        assert search_manager.search_view is None
        mock_gc.assert_called_once()
