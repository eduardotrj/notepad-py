import tkinter as tk
from tkinter import RIGHT, ttk
from tkinter.messagebox import showinfo
# from tkinter.filedialog import


class View(tk.Tk):

    """Build the window with the main elements of the Notepad

    """

    EMPTY_SYMBOL: str = 'ㅤ'
    FONT_LIST = (1,2,3,4,5,6,7,8,9,11,13,14,15,16,17,18,19,20,21,22,24,26,28,30,33,36,39,43,48,54,60,72,84)
    ZOOM_LIST = ("10%","20%","30%","40%","50%","60%","70%","80%","90%","100%","110%","120%","130%","140%","150%","160%","170%","180%","190%","200%","220%","240%","260%","280%","300%","320%","350%","400%","440%","500%","550%","600%","800%")
    TYPE_DOC = ("Plain Text", "MarkDown", "HTML")


# Default Attributes:
    _title: str = " - Notepad"
    _open_file: str = ""
    type_doc_selected: int = 0
    _default_width: int = 1800       # 1150
    _default_height: int = 1000       # 600
    day_mode = "🌙"
    _zoom: float = 2.6     # 1.6 Normal,  2.6 perfect for HD full screen.
    default_size: int = 9
    n_font = default_size
    _tree_elements: dict

    def __init__(self, controller):

        super().__init__()

        self._index_active: bool = True
        self.index_tree = None
        self._index_width: int = 200  # 20 - 200
        self.controller = controller

        self._make_frame()
        self.set_icon()
        self.set_title()
        self._set_menu()
        self.set_file_menu()
        self.set_type_menu()
        self.set_edit_menu()
        # self.set_insert_menu()
        self.set_view_menu()
        self.set_help_menu()
        self.set_night_option()
        self.set_index()
        self.set_text_area()
        self.set_size()
        self.set_font()

    def run(self):
        self.mainloop()

    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ WINDOW BUILDING ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    def _make_frame(self):
        """
            Create the main frame by Grid divided in 2 columns.
        """
        self.frame = tk.Frame(self)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_columnconfigure(1, weight=1)

    def set_icon(self):
        """
            Set Window Icon
        """
        self.iconbitmap('Assets/Icons/NotePad_32.ico')

    def index_width(self):
        # ! By unknown reason is not possible to change the column width after the first config.
        # https://github.com/python/cpython/blob/main/Doc/library/tkinter.ttk.rst?plain=1

        self._index_width = 20 if (self._index_width >= 200) else 200
        # self.index_tree.column("one", width=20)
        # self.index_tree.set_column_width("one", width=self._index_width)
        self.index_tree.heading("one", text="🗊 Index")

    def set_index(self):
        """Generate a interactive Index (TreeView) in the column [0] of the Frame.

            Build the Treeview widget, with a head text "Index",
            one column of 200 width. Make the element sticky to NSW,
            and a row height of 40 to leave space between the text lines.

            Define 2 Kind of events;
                ▪ When the click on Header → self.index_width()
                ▪ Click in any element(row) → self.controller.go_select_title(record)
        """
        self.index_tree = ttk.Treeview(columns="one", show='headings')
        self.index_tree.heading("one", text="Index", command=self.index_width)
        self.index_tree.column("one", width=self._index_width)
        self.index_tree.grid(row=0, column=0, sticky="nsw")
        style = ttk.Style()
        style.configure('Treeview', rowheight=40)

        def item_selected(event):
            """Find the element name in the event and sent it to
            self.controller.go_select_title(record)

            Args:
                event (_type_): _description_
            """
            # Take the text from the element clicked and send it to go_select_title().
            for selected_item in self.index_tree.selection():
                item = self.index_tree.item(selected_item)
                print(item)
                record = item['values']
                # Record = ['1.ㅤName ett']  → Remove from part from "ㅤ" & back part from "'"
                record = str(record).split(self.EMPTY_SYMBOL, 1)[1]
                record = record.split('\'', 1)[0]

                record = record.replace(self.EMPTY_SYMBOL, ' ')
                self.controller.go_select_title(record)

    # Bind the click event to the callback function
        self.index_tree.bind('<<TreeviewSelect>>', item_selected)
        # ● Adaptative height to Treeview
        # style = ttk.Style()
        # style.configure("Treeview.Heading", font=(None, LARGE_FONT), \
        #         rowheight=int(LARGE_FONT*2.5))
        # style.configure("Treeview", font=(None, MON_FONTSIZE), \
        #         rowheight=int(MON_FONTSIZE*2.5))

    def set_text_area(self):
        """Draw the Text Area Widget

        Place it in the column[1], make sticky to all sides.
        Add a Scrollbar at Y axis.

        Configure Text area:
        ▪ Scrollbar Y active.
        ▪ Select text color: #fcba03 (Imperial Yellow).
        ▪ Select text color, back focus: bd9833 (Ochre).
        ▪ Undo and Autoseparator activated.
        ▪ Default zoom size.
        """
        self.text_area = tk.Text(self)
        scrollbar = tk.Scrollbar(self.text_area)
        self.text_area.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        scrollbar.pack(side=RIGHT, fill=tk.Y)
        scrollbar.config(command=self.text_area.yview)
        self.text_area.config(
            yscrollcommand=scrollbar.set,
            selectbackground="#fcba03",
            inactiveselectbackground="#bd9833",
            undo=True,
            autoseparators=True,
            # maxundo=-1
                              )

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.tk.call('tk', 'scaling', self._zoom)

    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ WINDOW SETTINGS ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    def set_title(self, name: str = "Untitled"):
        """Set the window title.

        Args:
            name (str, optional): _description_. Defaults to "Untitled".
        """
        self._open_file = name
        self.title(name + self._title)

    def set_size(self):
        """ Set the window size in base default values

         TODO Option to take last specific size or edit default by configuration
        """

        # Calculate the center of the window.
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        left = (screen_width / 2) - (self._default_width / 2)
        top = (screen_height / 2) - (self._default_height / 2)
        self.geometry('%dx%d+%d+%d' % (
            self._default_width, self._default_height, left, top
            ))

    def set_font(self, size: int = 9):
        """ Define the font size of the notebook.

        Args:
            size (int, optional): _description_. Defaults to 9.
        """
        self.text_area.configure(font=("Consolas", self.FONT_LIST[size], "normal"))

    def set_zoom(self, size: int = 9):
        """ Define zoom size over the same font size.

        Args:
            size (int, optional): _description_. Defaults to 9.
        """
        self.menu_bar.entryconfig(5, label="🔎 "+self.ZOOM_LIST[size])

    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ MENU BUILDING ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    def _set_menu(self):
        """Build the menu bar/
        """
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # ? Add Recents: Last 5 documents opened
        # ? Add Example: Preview of a document showing all feactures like index.
    def set_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)   #command=lambda action="new": self.controller.define_action(action)
        file_menu.add_command(label="New", accelerator="Ctrl+N",command=self.controller.new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.controller.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.controller.save_file)
        file_menu.add_command(label="Save as…", accelerator="Ctrl+Shif+S", command=self.controller.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+.", command=self.controller.close_app)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def set_type_menu(self):
        type_menu = tk.Menu(self.menu_bar, tearoff=0)   #command=lambda action="new": self.controller.define_action(action)
        type_menu.add_command(label=self.TYPE_DOC[0], command=self.controller.select_type_plaintext)
        type_menu.add_command(label=self.TYPE_DOC[1], command=self.controller.select_type_markdown)
        type_menu.add_command(label=self.TYPE_DOC[2], command=self.controller.select_type_html)
        self.menu_bar.add_cascade(label= self.TYPE_DOC[self.type_doc_selected], menu=type_menu)

        # ? Add Undo / Redo options.
    def set_edit_menu(self):
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.controller.cut)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.controller.copy)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.controller.paste)
        edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.controller.select_all)
        edit_menu.add_separator()

        style_menu = tk.Menu(edit_menu, tearoff=0)
        style_menu.add_command(label="Bold", accelerator="Ctrl+B", command=lambda style= "fb": self.controller.take_text(style))
        style_menu.add_command(label="Italic", accelerator="Ctrl+J", command=lambda style= "fi": self.controller.take_text(style))
        style_menu.add_command(label="Italic Bold", command=lambda style= "fd": self.controller.take_text(style))

        style_menu.add_command(label="Script", accelerator="", command=lambda style= "tn": self.controller.take_text(style))
        style_menu.add_command(label="Script Bold", command=lambda style= "tb": self.controller.take_text(style))
        style_menu.add_command(label="Gothic", command=lambda style= "gn": self.controller.take_text(style))
        style_menu.add_command(label="Gothic Bold", command=lambda style= "gb": self.controller.take_text(style))
        style_menu.add_command(label="Highlighted", accelerator="Ctrl+H", command=lambda style= "hn": self.controller.take_text(style))
        style_menu.add_command(label="Sans", command=lambda style= "sn": self.controller.take_text(style))
        style_menu.add_command(label="Sans Italic", command=lambda style= "si": self.controller.take_text(style))
        style_menu.add_command(label="Sans Bold", command=lambda style= "sb": self.controller.take_text(style))
        style_menu.add_command(label="Sans Italic Bold", command=lambda style= "sd": self.controller.take_text(style))
        style_menu.add_command(label="Typewriter", accelerator="Ctrl+W", command=lambda style= "wn": self.controller.take_text(style))
        style_menu.add_command(label="Bubble", command=lambda style= "bn": self.controller.take_text(style))
        style_menu.add_command(label="Fullwidth", accelerator="Ctrl+L", command=lambda style= "ln": self.controller.take_text(style))
        style_menu.add_command(label="Super Index", command=lambda style= "mn": self.controller.take_text(style))

        style_menu.add_command(label="Remove style", accelerator="Ctrl+R", command=lambda style= "nn": self.controller.take_text(style))

        edit_menu.add_cascade(label="Style", menu=style_menu)
        edit_menu.add_separator()

        designs_menu = tk.Menu(edit_menu, tearoff=0)
        designs_menu.add_command(label="Line -", command=lambda style=1: self.controller.print_line(style))
        designs_menu.add_command(label="Line _", command=lambda style=2: self.controller.print_line(style))
        designs_menu.add_command(label="Line ■", command=lambda style=3: self.controller.print_line(style))
        designs_menu.add_command(label="Line ░", command=lambda style=4: self.controller.print_line(style))
        designs_menu.add_command(label="Line ▒", command=lambda style=5: self.controller.print_line(style))
        designs_menu.add_command(label="Line ▓", command=lambda style=6: self.controller.print_line(style))
        designs_menu.add_command(label="Line █", command=lambda style=7: self.controller.print_line(style))
        designs_menu.add_separator()
        designs_menu.add_command(label="Section", accelerator="Ctrl+1",  command=lambda style=1: self.controller.print_title(style))
        designs_menu.add_command(label="Title", accelerator="Ctrl+2", command=lambda style=2: self.controller.print_title(style))
        designs_menu.add_command(label="Subtitle", accelerator="Ctrl+3", command=lambda style=3: self.controller.print_title(style))
        designs_menu.add_command(label="3º Title", accelerator="Ctrl+4", command=lambda style=4: self.controller.print_title(style))
        designs_menu.add_command(label="1º List", accelerator="Ctrl+5", command=lambda style=5: self.controller.print_title(style))
        designs_menu.add_command(label="2º List", accelerator="Ctrl+6", command=lambda style=6: self.controller.print_title(style))
        designs_menu.add_command(label="3º List", accelerator="Ctrl+7", command=lambda style=7: self.controller.print_title(style))
        designs_menu.add_command(label="Reset title", accelerator="Ctrl+8",  command=lambda style=8: self.controller.print_title(style))
        # 5, 6, 7 style are for sans style with ●, •, ·.
        edit_menu.add_cascade(label="Designs", menu=designs_menu)

        edit_menu.add_command(label="Search", command=self.controller.search)
        edit_menu.add_command(label="Calculate", command=self.controller.do_operations)
        edit_menu.add_command(label="Date/Time", command=self.controller.print_time)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # TODO Expansion of the menu. Each option should call a extraView to show different options.
        # • Header → Input to put text. Style of text. BG style. Size.
        # • Footer → Style. If add any text or link.
        # • Idex → Create a index using self.titles_dict + sub_titles_dict.
        # • Table → Design a table with x Columns, x rows. Style. Size per cell.
        # • Characters → A panel map with tabs with different special chars.
        # • Emoji → A panel map with tabs with different emojis.
        # • Picture → Option to select a image to ASCII. Define size. Define Style used chars.
        # • Formula → To write a formula by using special characters.
        # • QR Code → Input with Link/text. → Insert by ASCII.
        # ? Move to here designs lines: self.controller.print_line().
    # def set_insert_menu(self):
    #     insert_menu = tk.Menu(self.menu_bar, tearoff=0)
    #     insert_menu.add_command(label="Header", accelerator="-", command=self.controller.test123)
    #     insert_menu.add_command(label="Footer", accelerator="-", command=self.controller.test123)
    #     insert_menu.add_command(label="Index", accelerator="-", command=self.controller.test123)
    #     insert_menu.add_separator()
    #     insert_menu.add_command(label="Table", accelerator="-", command=self.controller.test123)
    #     insert_menu.add_command(label="Characters", accelerator="-", command=self.controller.test123)
    #     insert_menu.add_command(label="Emoji", accelerator="-", command=self.controller.test123)
    #     insert_menu.add_command(label="Picture", accelerator="-", command=self.controller.test123)
    #     insert_menu.add_command(label="Formula", accelerator="-", command=self.controller.test123)
    #     insert_menu.add_command(label="Chart", accelerator="-", command=self.controller.test123)
    #     insert_menu.add_command(label="QR Code", accelerator="-", command=self.controller.test123)
    #     self.menu_bar.add_cascade(label="Insert", menu=insert_menu)

    def set_view_menu(self):
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Zoom In", accelerator="Ctrl+Plus", command=self.controller.zoom_in)
        view_menu.add_command(label="Zoom Out", accelerator="Ctrl+minus", command=self.controller.zoom_out)
        view_menu.add_command(label="Restore Zoom", accelerator="Ctrl+0", command=self.controller.zoom_reset)
        self.menu_bar.add_cascade(label="🔎 100%", menu=view_menu)

    def set_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About NotePad", command=self.show_about)
        self.menu_bar.add_cascade(label="About…", menu=help_menu)

    def set_night_option(self):
        self.menu_bar.add_command(label=self.day_mode, accelerator="Ctrl+M", command=self.controller.switch_mode) # Mode 🌞🌙

    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ OTHERS WINDOWS ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    def show_about(self):
        showinfo("Notepad", "Developed by Eduardo Trujillo in Python")

    # add configuration:
    # Change size window by default
    # Change text size by default
    # Color background, color selection.
    # Change font????
