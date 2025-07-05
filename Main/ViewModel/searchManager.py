import tkinter as tk
import gc
from Main.View.extraView import ExtraWindow, MessageWindow


class SearchManager:
    """Handles search and replace functionality."""

    def __init__(self, view, instances_list):
        """Initialize SearchManager.

        Args:
            view: Reference to the main view
            instances_list: List to track window instances
        """
        self.view = view
        self.instances = instances_list
        self.search_view = None

        # Search state
        self.search_word = ""
        self.replace_word = ""
        self.search_list = list()
        self.search_list_idx = list()
        self.total_matches = 0
        self.tag_position = 0

        # UI variables
        self.enable_replace = None
        self.input_search = None
        self.input_replace = None

    def search(self):
        """Create a new Search_view window if not exist, make focus on current instance if exist."""
        self.enable_replace = tk.StringVar()
        self.input_search = tk.StringVar()
        self.input_replace = tk.StringVar()

        # If exist a instance, make focus.
        if isinstance(self.search_view, ExtraWindow):
            self.search_view.focus_search()
        else:
            print("No existe")
            self.search_view = ExtraWindow(self, "Search")
            self.instances.append(self.search_view)

    def search_text(self):
        """Handle Search Request from Search_view.

        - Take values from Search_view
        - Decide if enable replace_text option
        - Reset index, matches and search_list
        - Show the selected result if exist
        - Show a Warning window when 0 results
        """
        self.search_word = self.input_search.get()
        self.replace_word = self.input_replace.get()

        # Check if both inputs are filled and exist matches
        if self.search_word and self.replace_word and self.total_matches > 0:
            # Avoid change the word if replace_check == False
            if self.enable_replace.get() == 'true':
                self.replace_text()

        # Reset values
        if self.search_word:
            self.search_list.clear()
            self.search_list_idx.clear()
            self.view.text_area.tag_remove(tk.SEL, 1.0, "end-1c")
            self.total_matches = 0
            self.tag_position = 0

            # Find and take all results
            self.total_matches = self.search_all()

            # If find a result, show it. If not, Show Warning Message
            if self.total_matches > 0:
                self.select_tag()
            else:
                MessageWindow.show_message("Not results found", "warning")

    def search_all(self):
        """Search "self.search_word" in the text area.

        - For each result, add +1 to number_matches
        - Add each match start index to "search_list_idx" list
        - Add each match end index to "search_list" list

        Returns:
            int: Quantity of results found
        """
        number_matches = 0

        while self.search_word:
            if self.search_list == []:  # if list is empty, start from beginning
                idx = "1.0"
            else:
                idx = self.search_list[-1]

            idx = self.view.text_area.search(
                self.search_word, idx, nocase=1, stopindex=tk.END
            )
            lastidx = '%s+%dc' % (idx, len(self.search_word))

            if idx and lastidx:
                number_matches += 1
                self.search_list_idx.append(idx)
                self.search_list.append(lastidx)
            else:
                break

        return number_matches

    def select_tag(self):
        """Use search_list index to select the desired String in the text area."""
        self.search_view.updating_results()

        # Before take index, check if self.search_list is empty
        if len(self.search_list) > 0:
            lastidx = self.search_list[self.tag_position]
            idx = self.search_list_idx[self.tag_position]
        else:
            self.total_matches = 0
            self.tag_position = 0
            lastidx = "1.0"
            idx = "1.0"

        # Remove previous selection
        self.view.text_area.tag_remove(tk.SEL, 1.0, "end-1c")

        # Add new selection in the new found word
        self.view.text_area.tag_add(tk.SEL, idx, lastidx)

        # Separate the position in row/columns
        counter_list = str(idx).split('.')

        # Add the pointer entry before the new found word, and put focus on it
        self.view.text_area.mark_set(
            "insert", "%d.%d" % (float(int(counter_list[0])),
                                 float(int(counter_list[1])))
        )
        self.view.text_area.see(float(int(counter_list[0])))

    def replace_text(self):
        """Get the position of the selected result. Delete and insert the new word."""
        lastidx = self.search_list[self.tag_position]
        idx = self.search_list_idx[self.tag_position]

        self.view.text_area.delete(idx, lastidx)
        self.view.text_area.insert(idx, self.replace_word)

    def next_tag(self):
        """Allow to read all self.tag_position in loop.

        if self.tag_position is >= self.total_matches-1:
            True = 0
            False → +1
        """
        if len(self.search_list) > 0:
            if self.tag_position >= (self.total_matches - 1):
                self.tag_position = 0
            else:
                self.tag_position += 1
        else:
            self.tag_position = 0

        self.select_tag()

    def last_tag(self):
        """Allow to read all self.tag_position in loop.

        if self.tag_position is <= 0:
            True = self.total_matches-1
            False → -1
        """
        if len(self.search_list) > 0:
            if self.tag_position <= 0:
                self.tag_position = (self.total_matches - 1)
            else:
                self.tag_position -= 1
        else:
            self.tag_position = 0

        self.select_tag()

    def show_replace(self):
        """Show or hide the replace input in Search_view."""
        if self.enable_replace.get() == 'true':
            self.search_view.add_replace_option()
        else:
            self.search_view.remove_replace_option()

    def delete_instance(self, instance=None):
        """Find the instance and delete it.

        Args:
            instance: Instance to delete
        """
        if isinstance(instance, ExtraWindow) and self.search_view:
            self.search_view = None
            gc.collect()
