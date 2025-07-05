from Main.View.view import View
from Main.View.auxMenu import Aux_menu
from Main.Model.model import Model

# Import the new manager classes
from Main.ViewModel.fileManager import FileManager
from Main.ViewModel.keyboardHandler import KeyboardHandler
from Main.ViewModel.textFormatter import TextFormatter
from Main.ViewModel.searchManager import SearchManager
from Main.ViewModel.indexManager import IndexManager
from Main.View.viewManager import ViewManager
from Main.ViewModel.editManager import EditManager


class ViewModel(object):
    """Manage the main application, controlling the front executions.

    This class now acts as a coordinator that delegates responsibilities
    to specialized manager classes.
    """

    EXTENSION_LIST: tuple = (".txt", ".md", ".html")

    def __init__(self) -> None:
        """Create a coordinated instance with all manager classes.

        Initialize all managers and set up their relationships.
        """
        # Initialize core components
        self.model = Model()
        self.view = View(self)
        self.instances = [self.view]

        # Initialize all manager classes
        self.file_manager = FileManager(
            self.view,
            on_file_change_callback=self._on_file_change
        )

        self.text_formatter = TextFormatter(
            self.view,
            self.model,
            on_text_change_callback=self._on_text_change
        )

        self.search_manager = SearchManager(self.view, self.instances)

        self.index_manager = IndexManager(self.view, self.text_formatter)

        self.view_manager = ViewManager(self.view)

        self.edit_manager = EditManager(self.view)

        # Initialize keyboard handler last since it needs other managers
        self.keyboard_handler = KeyboardHandler(
            self.view,
            self.file_manager,
            self.text_formatter,
            self.search_manager,
            self.view_manager,
            self.edit_manager
        )

        # Set up additional bindings
        self.view.bind("<Button-3>", self.callAux)

    def _on_file_change(self):
        """Callback when file content changes."""
        self.index_manager.find_index()

    def _on_text_change(self):
        """Callback when text content changes."""
        self.index_manager.find_index()

    def run(self):
        """Start the main application loop."""
        self.view.run()

    def callAux(self, event):
        """Create a Right-Click menu.

        Args:
            event: Tkinter event object
        """
        self.left_menu = Aux_menu(self)

        try:
            self.left_menu.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.left_menu.popup_menu.grab_release()

    def close_app(self):
        """Handle closing app."""
        self.view.destroy()

    # Delegate methods to appropriate managers for backward compatibility

    # File operations
    def new_file(self, event=1):
        """Create a new empty file."""
        return self.file_manager.new_file(event)

    def open_file(self, event=1):
        """Open an existing file."""
        return self.file_manager.open_file(event)

    def save_file(self, event=1):
        """Save the current file."""
        return self.file_manager.save_file(event)

    def save_as(self, event=1):
        """Save the file with a new name."""
        return self.file_manager.save_as(event)

    def open_recents(self, event=1):
        """Open recent files."""
        return self.file_manager.open_recents(event)

    # View operations
    def zoom_in(self, event=1):
        """Zoom in."""
        return self.view_manager.zoom_in(event)

    def zoom_out(self, event=1):
        """Zoom out."""
        return self.view_manager.zoom_out(event)

    def zoom_reset(self, event=1):
        """Reset zoom."""
        return self.view_manager.zoom_reset(event)

    def switch_mode(self, event=1):
        """Switch day/night mode."""
        return self.view_manager.switch_mode(event)

    def select_type_plaintext(self, event=1):
        """Select plain text document type."""
        return self.view_manager.select_type_plaintext(event)

    def select_type_markdown(self, event=1):
        """Select markdown document type."""
        return self.view_manager.select_type_markdown(event)

    def select_type_html(self, event=1):
        """Select HTML document type."""
        return self.view_manager.select_type_html(event)

    # Edit operations
    def cut(self):
        """Cut selected text."""
        return self.edit_manager.cut()

    def copy(self):
        """Copy selected text."""
        return self.edit_manager.copy()

    def paste(self):
        """Paste text from clipboard."""
        return self.edit_manager.paste()

    def select_all(self, event=1):
        """Select all text."""
        return self.edit_manager.select_all(event)

    def delete(self):
        """Delete selected text."""
        return self.edit_manager.delete()

    # Text formatting operations
    def take_text(self, style: str = "nn"):
        """Apply style to selected text."""
        return self.text_formatter.take_text(style)

    def print_line(self, style: int = 0):
        """Print a decorative line."""
        return self.text_formatter.print_line(style)

    def print_title(self, style: int = 0):
        """Format selected text as a title."""
        return self.text_formatter.print_title(style)

    def print_time(self):
        """Insert current date and time."""
        return self.text_formatter.print_time()

    def do_operations(self):
        """Perform mathematical operations on selected text."""
        return self.text_formatter.do_operations()

    # Search operations
    def search(self):
        """Open search dialog."""
        return self.search_manager.search()

    def search_text(self):
        """Perform text search."""
        return self.search_manager.search_text()

    def search_all(self):
        """Search all occurrences."""
        return self.search_manager.search_all()

    def select_tag(self):
        """Select current search result."""
        return self.search_manager.select_tag()

    def replace_text(self):
        """Replace current search result."""
        return self.search_manager.replace_text()

    def next_tag(self):
        """Go to next search result."""
        return self.search_manager.next_tag()

    def last_tag(self):
        """Go to previous search result."""
        return self.search_manager.last_tag()

    def show_replace(self):
        """Show/hide replace option."""
        return self.search_manager.show_replace()

    # Index operations
    def go_select_title(self, index: str = ""):
        """Navigate to a specific title."""
        return self.index_manager.go_select_title(index)

    def find_index(self):
        """Find and update document index."""
        return self.index_manager.find_index()

    def update_index(self):
        """Update the index display."""
        return self.index_manager.update_index()

    # Instance management
    def delete_instance(self, instance=None):
        """Delete a window instance."""
        return self.search_manager.delete_instance(instance)

    # Properties for backward compatibility
    @property
    def file(self):
        """Get current file path."""
        return self.file_manager.file

    @property
    def search_word(self):
        """Get current search word."""
        return self.search_manager.search_word

    @property
    def replace_word(self):
        """Get current replace word."""
        return self.search_manager.replace_word

    @property
    def total_matches(self):
        """Get total search matches."""
        return self.search_manager.total_matches

    @property
    def titles_dict(self):
        """Get titles dictionary."""
        return self.index_manager.titles_dict

    @property
    def sub_titles_dict(self):
        """Get sub-titles dictionary."""
        return self.index_manager.sub_titles_dict

    # Legacy properties that might be used by other components
    @property
    def enable_replace(self):
        """Get enable replace variable."""
        return self.search_manager.enable_replace

    @property
    def input_search(self):
        """Get search input variable."""
        return self.search_manager.input_search

    @property
    def input_replace(self):
        """Get replace input variable."""
        return self.search_manager.input_replace
