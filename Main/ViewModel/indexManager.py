import tkinter as tk


class IndexManager:
    """Handles document indexing and navigation functionality."""

    def __init__(self, view, text_formatter):
        """Initialize IndexManager.

        Args:
            view: Reference to the main view
            text_formatter: Reference to TextFormatter for constants
        """
        self.view = view
        self.text_formatter = text_formatter
        self.titles_dict = {}
        self.sub_titles_dict = {}

    def go_select_title(self, index: str = ""):
        """Make focus on the element desired "Title".

        Take the Title word, find the match in the dictionary Key
        Take the Value for this key, text index, and use to focus it.

        Args:
            index (str): The Title Word.
        """
        idx = str(self.titles_dict[index] + 10.0)  # Add + 10 to center the focus

        counter_list = str(idx).split('.')

        # Add the pointer entry before the new found word, and put focus on it
        self.view.text_area.mark_set(
            "insert",
            "%d.%d" % (float(int(counter_list[0])), float(int(counter_list[1])))
        )
        self.view.text_area.see(float(int(counter_list[0])))

    def find_index(self):
        """Update the information in self.titles_dict.

        - Create a new temporal Dictionary: temp_dict
        - Find any title in the text by using "INDEX_START"
        - Clean the title text and add it to temp_dict as key
        - Add the referent index as value to temp_dict
        - Use temp_dict to update values in self.titles_dict
        - Sort self.titles_dict and delete values which aren't in temp_dict
        """
        temp_dict = {}
        idx = "1.0"

        while idx:
            # Get position 1.0 only the first time
            if temp_dict == {}:  # if list is empty, move one position in the list
                temp_dict[self.view._open_file] = 1.0
            else:
                idx = str(list(temp_dict.values())[-1])
                idx = self.view.text_area.search(
                    self.text_formatter.INDEX_START,
                    idx,
                    nocase=1,
                    stopindex=tk.END
                )

                if idx:
                    next_line = float(idx) + 1  # Where the title is located
                    lastPosition = str(next_line).split('.', 1)[0]
                    line_content = self.view.text_area.get(
                        f"{next_line}",
                        f"{lastPosition}.end"
                    )
                    line_content = line_content.split('  ', -1)[1]

                    temp_dict[line_content] = next_line
                else:
                    break

        # Update self.titles_dict using the temp_dict
        self.titles_dict.update(temp_dict)
        self.titles_dict = {
            key: value for key, value in sorted(
                self.titles_dict.items(),
                key=lambda item: item[1]
            )
        }

        # Clean deleted elements
        for key in self.titles_dict.copy():
            if key not in temp_dict:
                del self.titles_dict[key]

        self.update_index()

    def update_index(self):
        """Update the values inside of the index (Treeview).

        1. Validate if self._index_active to draw the widget, if not, disabled
        2. Define local variables:
           - EMPTY_SYMBOL: str → Define an empty space character 'ㅤ'
           - index_number: int → Number of each index element
        3. Build the Treeview widget, with a head text "Index",
           one column of 200 width. Make the element sticky to NSW,
           and a row height of 40 to leave space between the text lines
        """
        index_number = 0

        for element in self.view.index_tree.get_children():
            self.view.index_tree.delete(element)

        for key, value in self.titles_dict.items():
            index_number += 1
            new_value = (
                str(index_number) + "." +
                self.text_formatter.EMPTY_SYMBOL +
                str(key).replace(" ", self.text_formatter.EMPTY_SYMBOL)
            )
            iid = self.view.index_tree.insert("", tk.END, values=(new_value))
