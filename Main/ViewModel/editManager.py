import tkinter as tk


class EditManager:
    """Handles text editing operations like cut, copy, paste, delete."""

    def __init__(self, view):
        """Initialize EditManager.

        Args:
            view: Reference to the main view
        """
        self.view = view

    def cut(self):
        """Cut selected text to clipboard."""
        self.view.text_area.event_generate("<<Cut>>")

    def copy(self):
        """Copy selected text to clipboard."""
        self.view.text_area.event_generate("<<Copy>>")

    def paste(self):
        """Paste text from clipboard."""
        self.view.text_area.event_generate("<<Paste>>")

    def select_all(self, event=1):
        """Select all text in the text area.

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        self.view.text_area.tag_add('sel', '1.0', 'end')

    def delete(self):
        """Delete selected text."""
        try:
            if self.view.text_area.selection_get():
                line, column = map(
                    int,
                    self.view.text_area.index('sel.first').split('.')
                )
                self.view.text_area.delete('sel.first', 'sel.last')
        except tk.TclError:
            # No text selected
            pass

    def auto_save(self, time):
        """Auto-save functionality (placeholder for future implementation).

        Should save the document as temporal file each x minutes:
        Document_Name + "_temporal_" + date + .txt

        Args:
            time: Time interval for auto-save
        """
        # TODO: Implement auto-save functionality
        pass
