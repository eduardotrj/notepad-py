class ViewManager:
    """Handles view-related operations like zoom and mode switching."""

    def __init__(self, view):
        """Initialize ViewManager.

        Args:
            view: Reference to the main view
        """
        self.view = view

    def zoom_in(self, event=1):
        """Increase font size (zoom in).

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        if self.view.n_font < 32:
            self.view.n_font += 1
        self.view.set_font(self.view.n_font)
        self.view.set_zoom(self.view.n_font)

    def zoom_out(self, event=1):
        """Decrease font size (zoom out).

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        if self.view.n_font > 0:
            self.view.n_font -= 1
        self.view.set_font(self.view.n_font)
        self.view.set_zoom(self.view.n_font)

    def zoom_reset(self, event=1):
        """Reset font size to default.

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        self.view.n_font = self.view.default_size
        self.view.set_font(self.view.n_font)
        self.view.set_zoom(self.view.n_font)

    def switch_mode(self, event=1):
        """Switch between day and night mode.

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        if self.view.day_mode == "🌙":
            self.view.text_area.configure(bg="#2A2F2D", fg="white")
            self.view.day_mode = "🌞"
            self.view.menu_bar.entryconfig(7, label="🌞")
        else:
            self.view.text_area.configure(bg="white", fg="black")
            self.view.day_mode = "🌙"
            self.view.menu_bar.entryconfig(7, label="🌙")

    def select_type_plaintext(self, event=1):
        """Define interface to Plain text.

        - Transform Doc to Plain text
        - Change styles effect to Plain text
        - Save by default as .txt

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        self.view.type_doc_selected = 0
        self.change_menu_type()

    def select_type_markdown(self, event=1):
        """Define interface to Markdown.

        - Transform Doc to Markdown
        - Change styles effect to Markdown
        - Save by default as .md

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        self.view.type_doc_selected = 1
        self.change_menu_type()

    def select_type_html(self, event=1):
        """Define interface to HTML.

        - Transform Doc to HTML
        - Change styles effect to HTML
        - Save by default as .html

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        self.view.type_doc_selected = 2
        self.change_menu_type()

    def change_menu_type(self):
        """Update the menu to reflect the selected document type."""
        self.view.menu_bar.entryconfig(
            2,
            label=self.view.TYPE_DOC[self.view.type_doc_selected]
        )
