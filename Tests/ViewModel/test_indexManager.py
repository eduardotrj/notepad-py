from unittest.mock import Mock, patch
from Main.ViewModel.indexManager import IndexManager


class TestIndexManager:
    """Test suite for IndexManager class."""

    def test_init(self, mock_view):
        """Test IndexManager initialization."""
        text_formatter = Mock()
        
        manager = IndexManager(mock_view, text_formatter)
        
        assert manager.view is mock_view
        assert manager.text_formatter is text_formatter
        assert manager.titles_dict == {}
        assert manager.sub_titles_dict == {}

    def test_go_select_title_existing_title(self, mock_view):
        """Test go_select_title with existing title."""
        text_formatter = Mock()
        manager = IndexManager(mock_view, text_formatter)
        
        # Set up mock data
        manager.titles_dict = {"Test Title": 5.0}
        
        # Call method
        manager.go_select_title("Test Title")
        
        # Verify text area operations
        mock_view.text_area.mark_set.assert_called_once_with(
            "insert", "15.0"
        )
        mock_view.text_area.see.assert_called_once_with(15.0)

    def test_go_select_title_with_decimal_position(self, mock_view):
        """Test go_select_title with decimal position."""
        text_formatter = Mock()
        manager = IndexManager(mock_view, text_formatter)
        
        # Set up mock data with decimal position
        manager.titles_dict = {"Test Title": 5.5}
        
        # Call method
        manager.go_select_title("Test Title")
        
        # Verify calculations: 5.5 + 10.0 = 15.5
        mock_view.text_area.mark_set.assert_called_once_with(
            "insert", "15.5"
        )
        mock_view.text_area.see.assert_called_once_with(15.0)

    def test_find_index_empty_document(self, mock_view):
        """Test find_index with empty document."""
        text_formatter = Mock()
        text_formatter.INDEX_START = "# "
        
        manager = IndexManager(mock_view, text_formatter)
        mock_view._open_file = "test.txt"
        
        # Mock empty search result
        mock_view.text_area.search.return_value = ""
        
        with patch.object(manager, 'update_index') as mock_update:
            manager.find_index()
            
            # Should have at least the file entry
            assert "test.txt" in manager.titles_dict
            assert manager.titles_dict["test.txt"] == 1.0
            mock_update.assert_called_once()

    def test_find_index_with_titles(self, mock_view):
        """Test find_index with document containing titles."""
        text_formatter = Mock()
        text_formatter.INDEX_START = "# "
        
        manager = IndexManager(mock_view, text_formatter)
        mock_view._open_file = "test.txt"
        
        # Mock search results
        search_results = ["2.0", "5.0", ""]  # Two titles found, then empty
        mock_view.text_area.search.side_effect = search_results
        
        # Mock line content retrieval
        mock_view.text_area.get.side_effect = [
            "  First Title",
            "  Second Title"
        ]
        
        with patch.object(manager, 'update_index') as mock_update:
            manager.find_index()
            
            # Verify titles were found and processed
            expected_titles = {
                "test.txt": 1.0,
                "First Title": 3.0,
                "Second Title": 6.0
            }
            
            for title, position in expected_titles.items():
                assert title in manager.titles_dict
                assert manager.titles_dict[title] == position
            
            mock_update.assert_called_once()

    def test_find_index_cleans_deleted_titles(self, mock_view):
        """Test that find_index removes titles no longer in document."""
        text_formatter = Mock()
        text_formatter.INDEX_START = "# "
        
        manager = IndexManager(mock_view, text_formatter)
        mock_view._open_file = "test.txt"
        
        # Set up existing titles
        manager.titles_dict = {
            "test.txt": 1.0,
            "Old Title": 2.0,
            "Existing Title": 3.0
        }
        
        # Mock search to only find "Existing Title"
        search_results = ["3.0", ""]
        mock_view.text_area.search.side_effect = search_results
        mock_view.text_area.get.return_value = "  Existing Title"
        
        with patch.object(manager, 'update_index') as mock_update:
            manager.find_index()
            
            # "Old Title" should be removed
            assert "Old Title" not in manager.titles_dict
            assert "Existing Title" in manager.titles_dict
            assert "test.txt" in manager.titles_dict
            
            mock_update.assert_called_once()

    def test_find_index_sorts_titles_by_position(self, mock_view):
        """Test that find_index sorts titles by their position."""
        text_formatter = Mock()
        text_formatter.INDEX_START = "# "
        
        manager = IndexManager(mock_view, text_formatter)
        mock_view._open_file = "test.txt"
        
        # Mock search results in non-sequential order
        search_results = ["5.0", "2.0", "8.0", ""]
        mock_view.text_area.search.side_effect = search_results
        
        mock_view.text_area.get.side_effect = [
            "  Third Title",   # at position 6.0
            "  First Title",   # at position 3.0
            "  Fourth Title"   # at position 9.0
        ]
        
        with patch.object(manager, 'update_index') as mock_update:
            manager.find_index()
            
            # Get the keys in order they appear in the sorted dictionary
            sorted_titles = list(manager.titles_dict.keys())
            
            # Should be sorted by position (value)
            assert sorted_titles.index("test.txt") < sorted_titles.index(
                "First Title")
            assert sorted_titles.index("First Title") < sorted_titles.index(
                "Third Title")
            assert sorted_titles.index("Third Title") < sorted_titles.index(
                "Fourth Title")

    def test_update_index_empty_titles(self, mock_view):
        """Test update_index with no titles."""
        text_formatter = Mock()
        text_formatter.EMPTY_SYMBOL = "ㅤ"
        
        manager = IndexManager(mock_view, text_formatter)
        manager.titles_dict = {}
        
        # Mock empty tree
        mock_view.index_tree.get_children.return_value = []
        
        manager.update_index()
        
        # Should clear existing items and not insert any new ones
        mock_view.index_tree.get_children.assert_called_once()
        mock_view.index_tree.insert.assert_not_called()

    def test_update_index_with_titles(self, mock_view):
        """Test update_index with existing titles."""
        text_formatter = Mock()
        text_formatter.EMPTY_SYMBOL = "ㅤ"
        
        manager = IndexManager(mock_view, text_formatter)
        manager.titles_dict = {
            "test.txt": 1.0,
            "First Title": 2.0,
            "Second Title": 3.0
        }
        
        # Mock existing tree items
        existing_items = ["item1", "item2"]
        mock_view.index_tree.get_children.return_value = existing_items
        mock_view.index_tree.insert.return_value = "new_item"
        
        manager.update_index()
        
        # Should delete existing items
        for item in existing_items:
            mock_view.index_tree.delete.assert_any_call(item)
        
        # Should insert new items for each title
        assert mock_view.index_tree.insert.call_count == 3
        
        # Verify the format of inserted values
        insert_calls = mock_view.index_tree.insert.call_args_list
        
        # First call should be for "test.txt"
        first_call_value = insert_calls[0][1]['values']
        # The values parameter contains the full formatted string
        assert "1." in str(first_call_value)
        assert "test.txt" in first_call_value.replace("ㅤ", " ")

    def test_update_index_formats_titles_correctly(self, mock_view):
        """Test that update_index formats titles correctly."""
        text_formatter = Mock()
        text_formatter.EMPTY_SYMBOL = "ㅤ"
        
        manager = IndexManager(mock_view, text_formatter)
        manager.titles_dict = {
            "Title With Spaces": 1.0
        }
        
        mock_view.index_tree.get_children.return_value = []
        mock_view.index_tree.insert.return_value = "item1"
        
        manager.update_index()
        
        # Verify that spaces are replaced with EMPTY_SYMBOL
        insert_call = mock_view.index_tree.insert.call_args
        formatted_value = str(insert_call[1]['values'])
        
        # Should contain the EMPTY_SYMBOL replacement
        assert "ㅤ" in formatted_value

    def test_go_select_title_key_error(self, mock_view):
        """Test go_select_title with non-existent title."""
        text_formatter = Mock()
        manager = IndexManager(mock_view, text_formatter)
        
        # Empty titles dictionary
        manager.titles_dict = {}
        
        # Should raise KeyError for non-existent title
        try:
            manager.go_select_title("Non-existent Title")
            assert False, "Expected KeyError"
        except KeyError:
            pass  # Expected behavior

    def test_find_index_handles_complex_line_content(self, mock_view):
        """Test find_index with complex line content parsing."""
        text_formatter = Mock()
        text_formatter.INDEX_START = "# "
        
        manager = IndexManager(mock_view, text_formatter)
        mock_view._open_file = "test.txt"
        
        # Mock search result
        mock_view.text_area.search.side_effect = ["2.0", ""]
        
        # Mock line content with multiple spaces and formatting
        mock_view.text_area.get.return_value = "  Complex  Title  With  Spaces"
        
        with patch.object(manager, 'update_index') as mock_update:
            manager.find_index()
            
            # Should properly parse the title after the first two spaces
            # Line content "  Complex  Title  With  Spaces" split on "  "
            # gives ["", "Complex", "Title", "With", "Spaces"]
            # and [1] gives "Complex"
            assert "Complex" in manager.titles_dict
            mock_update.assert_called_once()

    def test_integration_find_and_navigate(self, mock_view):
        """Test integration between find_index and go_select_title."""
        text_formatter = Mock()
        text_formatter.INDEX_START = "# "
        text_formatter.EMPTY_SYMBOL = "ㅤ"
        
        manager = IndexManager(mock_view, text_formatter)
        mock_view._open_file = "test.txt"
        
        # Setup find_index to find a title
        mock_view.text_area.search.side_effect = ["5.0", ""]
        mock_view.text_area.get.return_value = "  Integration Test"
        mock_view.index_tree.get_children.return_value = []
        
        # Run find_index
        manager.find_index()
        
        # Verify title was found
        assert "Integration Test" in manager.titles_dict
        assert manager.titles_dict["Integration Test"] == 6.0
        
        # Now test navigation to that title
        manager.go_select_title("Integration Test")
        
        # Should navigate to position 16.0 (6.0 + 10.0)
        mock_view.text_area.mark_set.assert_called_with("insert", "16.0")
        mock_view.text_area.see.assert_called_with(16.0)
