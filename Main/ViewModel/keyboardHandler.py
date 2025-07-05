import tkinter as tk


class KeyboardHandler:
    """Handles keyboard events and shortcuts for the notepad application."""

    def __init__(self, view, file_manager, text_formatter, search_manager, view_manager, edit_manager):
        """Initialize KeyboardHandler with references to other managers.

        Args:
            view: Reference to the main view
            file_manager: Reference to FileManager instance
            text_formatter: Reference to TextFormatter instance
            search_manager: Reference to SearchManager instance
            view_manager: Reference to ViewManager instance
            edit_manager: Reference to EditManager instance
        """
        self.view = view
        self.file_manager = file_manager
        self.text_formatter = text_formatter
        self.search_manager = search_manager
        self.view_manager = view_manager
        self.edit_manager = edit_manager

        # Key state tracking
        self.key_alt_r = False
        self.key_control_l = False

        self._setup_shortcuts()

    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # File operations
        self.view.bind("<Control-n>", self.file_manager.new_file)
        self.view.bind("<Control-o>", self.file_manager.open_file)
        self.view.bind("<Control-s>", self.file_manager.save_file)
        self.view.bind("<Control-S>", self.file_manager.save_as)

        # View operations
        self.view.bind("<Control-m>", self.view_manager.switch_mode)
        self.view.bind("<Control-plus>", self.view_manager.zoom_in)
        self.view.bind("<Control-minus>", self.view_manager.zoom_out)
        self.view.bind("<Control-0>", self.view_manager.zoom_reset)

        # Key events
        self.view.bind("<KeyPress>", self.key_pressed)
        self.view.bind("<KeyRelease>", self.key_released)

        # Text area specific bindings
        self.view.text_area.bind("<Control-Alt_R>", self.test123)
        self.view.text_area.bind("<KeyRelease-Return>", self.save_step)

    def test123(self, event):
        """Test function for specific key combination."""
        print("Working!")

    def key_pressed(self, event):
        """Handle key press events.

        Args:
            event: Tkinter event object

        Returns:
            str: "break" to stop event propagation
        """
        if event.keysym == 'Alt_R':
            self.key_alt_r = True

        if event.keysym == 'Control_L':
            self.key_control_l = True

        if self.key_alt_r:
            self._handle_alt_r_combinations(event)
        elif self.key_control_l:
            self._handle_control_combinations(event)

        return "break"

    def key_released(self, event):
        """Handle key release events.

        Args:
            event: Tkinter event object

        Returns:
            str: "break" to stop event propagation
        """
        if event.keysym == 'Alt_R':
            self.key_alt_r = False
        if event.keysym == 'Control_L':
            self.key_control_l = False
        return "break"

    def _handle_alt_r_combinations(self, event):
        """Handle Alt+R key combinations for special symbols.

        Args:
            event: Tkinter event object
        """
        pointer = self.view.text_area.index(tk.INSERT)
        symbol = ''

        symbol_map = {
            '2': '⚠️',
            '3': '‼',
            '5': '✶',
            '6': '●',
            '7': '░',
            '8': '▒',
            '9': '▓',
            '0': '█',
            'slash': '█',
            'p': '←',
            'P': '←',
            'bracketleft': '↑',
            'braceleft': '↑',
            'bracketright': '→',
            'braceright': '→',
            'apostrophe': '↓',
            'at': '↓',
            't': '■',
            'T': '■',
            'y': '▪',
            'Y': '▪'
        }

        symbol = symbol_map.get(event.keysym, '')
        if symbol:
            self.view.text_area.insert(pointer, symbol)

    def _handle_control_combinations(self, event):
        """Handle Control key combinations.

        Args:
            event: Tkinter event object
        """
        keysym = event.keysym

        # Text formatting shortcuts
        if keysym == 'r':
            self.text_formatter.take_text("nn")
        elif keysym == 'b':
            self.text_formatter.take_text("fb")
        elif keysym == 'j':
            self.text_formatter.take_text("fi")
        elif keysym == 'h':
            self.text_formatter.take_text("hn")
        elif keysym == 'w':
            self.text_formatter.take_text("wn")
        elif keysym == 'l':
            self.text_formatter.take_text("ln")

        # File operations (handled by view shortcuts, but keeping for completeness)
        elif keysym == 'o':
            self.file_manager.open_file()
        elif keysym == 's' and event.keysym == 'Shift_L':
            self.file_manager.save_as()
        elif keysym == 's':
            self.file_manager.save_file()
        elif keysym == 'n':
            self.file_manager.new_file()
        elif keysym == '.':
            self.view.destroy()

        # View operations
        elif keysym in ['plus', 'equal']:
            self.view_manager.zoom_in()
        elif keysym == 'minus':
            self.view_manager.zoom_out()
        elif keysym == '0':
            self.view_manager.zoom_reset()
        elif keysym == 'm':
            self.view_manager.switch_mode()

        # Search
        elif keysym == 'f':
            self.search_manager.search()

        # Title formatting
        elif keysym in ['1', '2', '3', '4', '5', '6', '7', '8']:
            self.text_formatter.print_title(int(keysym))

    def save_step(self, obj):
        """Handle save step after Return key press.

        Args:
            obj: Event object
        """
        # TODO: Implement auto-save step functionality
        pass
