import tkinter as tk
from datetime import datetime


class TextFormatter:
    """Handles text formatting operations including styles and titles."""

    # Constants for formatting
    INDEX_START = "▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"
    SUB_INDEX = "■ "
    EMPTY_SYMBOL = 'ㅤ'

    def __init__(self, view, model, on_text_change_callback=None):
        """Initialize TextFormatter.

        Args:
            view: Reference to the main view
            model: Reference to the model for style operations
            on_text_change_callback: Callback for when text changes
        """
        self.view = view
        self.model = model
        self.select_text = ""
        self.on_text_change_callback = on_text_change_callback

    def take_text(self, style: str = "nn"):
        """Take selected text and change character by character to another style.

        Args:
            style (str, optional): Text style selected to apply. Defaults to "nn".
        """
        try:
            if self.view.text_area.selection_get():
                self.select_text = self.view.text_area.selection_get()
                self.select_text = [*self.select_text]

                line, column = map(int, self.view.text_area.index('sel.first').split('.'))
                position = (str(line) + "." + str(column))
                self.view.text_area.delete('sel.first', 'sel.last')

                new_character_list = map(
                    lambda x: self.model.apply_style(x, style),
                    self.select_text
                )
                new_text = ''.join(new_character_list)
                self.view.text_area.insert(position, new_text)

                if self.on_text_change_callback:
                    self.on_text_change_callback()
        except tk.TclError:
            # No text selected
            pass

    def print_line(self, style: int = 0):
        """Set a predesigned line style.

        Args:
            style (int, optional): Type of design selected. Defaults to 0.
        """
        pointer = self.view.text_area.index(tk.INSERT)

        line_styles = {
            1: "---------------------------------------------------------------------------------------------------------------",
            2: "_______________________________________________________________________________________________________________",
            3: "▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄",
            4: "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░",
            5: "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
            6: "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
            7: "███████████████████████████████████████████████████████████████████████████████████████████████████████████████"
        }

        line = line_styles.get(style, "")
        if line:
            self.view.text_area.insert(pointer, line)

    def print_title(self, style: int = 0):
        """Use selected text to create a title style.

        Args:
            style (int, optional): Type of title selected. Defaults to 0.
        """
        try:
            if not self.view.text_area.selection_get():
                return

            self.select_text = self.view.text_area.selection_get()
            self.select_text = [*self.select_text]

            line, column = map(int, self.view.text_area.index('sel.first').split('.'))
            position = (str(line) + "." + str(0))
            self.view.text_area.delete('sel.first', 'sel.last')

            new_text = self._format_title_style(style)

            if new_text:
                self.view.text_area.insert(position, new_text)
                if self.on_text_change_callback:
                    self.on_text_change_callback()

        except tk.TclError:
            # No text selected
            pass

    def _format_title_style(self, style: int) -> str:
        """Format text according to the specified title style.

        Args:
            style (int): The title style to apply

        Returns:
            str: Formatted text
        """
        if style == 1:
            # Big title with decorative borders
            long_text = len(self.select_text) + 4
            text = ''.join(self.select_text).title()
            fill_char = 111 - long_text
            fill_char = fill_char // 2
            part1 = "░" * fill_char
            fill_char = 111 - (long_text + fill_char)
            part2 = "░" * fill_char

            return f"""{self.INDEX_START}
{part1}  {text}  {part2}
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"""

        elif style == 2:
            text = self._apply_style_to_text("fb").title()
            return '■ ' + text

        elif style == 3:
            text = self._apply_style_to_text("fd").capitalize()
            return '	▪ ' + text

        elif style == 4:
            text = self._apply_style_to_text("fi").capitalize()
            return '		· ' + text

        elif style == 5:
            text = self._apply_style_to_text("sb").capitalize()
            return '	● ' + text

        elif style == 6:
            text = self._apply_style_to_text("sd").capitalize()
            return '		• ' + text

        elif style == 7:
            text = self._apply_style_to_text("si").capitalize()
            return '			· ' + text

        elif style == 8:  # Delete style
            text = self._apply_style_to_text("nn")
            text = text.translate({ord(i): None for i in '■▪●•·▄▀░'})
            text = text.strip().lower()
            return text

        return ""

    def _apply_style_to_text(self, style: str) -> str:
        """Apply a style to the selected text.

        Args:
            style (str): Style code to apply

        Returns:
            str: Styled text
        """
        new_character_list = map(
            lambda x: self.model.apply_style(x, style),
            self.select_text
        )
        return ''.join(new_character_list)

    def print_time(self):
        """Insert the current date and time as a string."""
        time = datetime.now()
        time_str = time.strftime("%H:%M %d/%m/%Y")
        pointer = self.view.text_area.index(tk.INSERT)
        self.view.text_area.insert(pointer, time_str)

    def do_operations(self):
        """Resolve the selected math operations (placeholder for future implementation)."""
        try:
            if self.view.text_area.selection_get():
                self.select_text = self.view.text_area.selection_get()

                line, column = map(int, self.view.text_area.index('sel.first').split('.'))
                position = (str(line) + "." + str(column))
                self.view.text_area.delete('sel.first', 'sel.last')

                operation = self.select_text
                # TODO: Implement calculation logic
                solution = ""  # self.calc.calculate(operation)

                self.view.text_area.insert(position, solution)
        except tk.TclError:
            # No text selected
            pass
