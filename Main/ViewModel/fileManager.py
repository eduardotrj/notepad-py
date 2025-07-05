import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


class FileManager:
    """Handles all file operations like new, open, save, and save as."""

    EXTENSION_LIST: tuple = (".txt", ".md", ".html")

    def __init__(self, view, on_file_change_callback=None):
        """Initialize FileManager.

        Args:
            view: Reference to the main view
            on_file_change_callback: Callback function when file changes
        """
        self.view = view
        self.file = None
        self.on_file_change_callback = on_file_change_callback

    def new_file(self, event=1):
        """Create a new empty file.

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        self.view.set_title()
        self.file = None
        self.view.text_area.delete(1.0, tk.END)
        if self.on_file_change_callback:
            self.on_file_change_callback()

    def open_file(self, event=1):
        """Open an existing file.

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        self.file = askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Documents", "*.txt"),
                ("HTML files", "*.html"),
                ("Markdown files", "*.md")
            ]
        )
        if self.file == "":  # No file to open
            self.file = None
        else:  # Try to open the file
            self.view.set_title(os.path.basename(self.file))
            self.view.text_area.delete(1.0, tk.END)
            try:
                with open(self.file, "r", encoding="utf-8") as file:
                    self.view.text_area.insert(1.0, file.read())
                if self.on_file_change_callback:
                    self.on_file_change_callback()
            except Exception as e:
                print(f"Error opening file: {e}")

    def save_file(self, event=1):
        """Save the file using an existing document.

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        if self.file is None:  # Save as new file
            self.save_as()
        else:  # Save to existing file
            try:
                with open(self.file, "w", encoding="utf-8") as file:
                    file.write(self.view.text_area.get(1.0, tk.END))
            except Exception as e:
                print(f"Error saving file: {e}")

    def save_as(self, event=1):
        """Save the document with a specific name in a specific location.

        Args:
            event (int, optional): Event parameter. Defaults to 1.
        """
        self.file = asksaveasfilename(
            initialfile='Untitled.txt',
            defaultextension=self.EXTENSION_LIST[self.view.type_doc_selected],
            filetypes=[
                ("All Files", "*.*"),
                ("Text Documents", "*.txt"),
                ("HTML files", "*.html"),
                ("Markdown files", "*.md")
            ]
        )
        if self.file == "":
            self.file = None
        else:  # Try to save the file
            try:
                with open(self.file, "w", encoding="utf-8") as file:
                    file.write(self.view.text_area.get(1.0, tk.END))
                self.view.set_title(os.path.basename(self.file))
            except Exception as e:
                print(f"Error saving file: {e}")

    def open_recents(self, event=1):
        """Open recent files functionality (placeholder for future implementation)."""
        # TODO: Implement recent files functionality
        pass

    def get_current_file(self):
        """Get the current file path."""
        return self.file

    def has_file(self):
        """Check if a file is currently open."""
        return self.file is not None
