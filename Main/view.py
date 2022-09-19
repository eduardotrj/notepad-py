import tkinter as tk 
from tkinter import RIGHT, ttk 
from tkinter.messagebox import *
from tkinter.filedialog import *


class View(tk.Tk):
    
    _title = " - Notepad"
    _default_width = 1050
    _default_height = 600
    day_mode = "🌙"
    _zoom = 1.6
    default_size = 9
    n_font =  default_size
    font_list = (1,2,3,4,5,6,7,8,9,11,13,14,15,16,17,18,19,20,21,22,24,26,28,30,33,36,39,43,48,54,60,72,84)
    zoom_list = ("10%","20%","30%","40%","50%","60%","70%","80%","90%","100%","110%","120%","130%","140%","150%","160%","170%","180%","190%","200%","220%","240%","260%","280%","300%","320%","350%","400%","440%","500%","550%","600%","800%")

    
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        
        self._make_frame()
        self.set_title()
        self._set_menu()
        self.set_file_menu()
        self.set_edit_menu()
        self.set_view_menu()
        self.set_help_menu()
        self.set_night_option()
        self.set_text_area()
        self.set_size()
        self.set_font()
    
        
    def run(self):
        self.mainloop()
    
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ WINDOW BUILDING ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■   

    def _make_frame(self):
        self.frame= tk.Frame(self)
        
          
    def set_text_area(self):
        self.text_area = tk.Text(self)
        scrollbar = tk.Scrollbar(self.text_area)
        
        self.text_area.grid(sticky = tk.N + tk.E + tk.S + tk.W)
        scrollbar.pack(side=RIGHT,fill=tk.Y)
        scrollbar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scrollbar.set)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1) 
        self.tk.call('tk', 'scaling', self._zoom)
        
        
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ WINDOW SETTINGS ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ 
        
    def set_title(self, name:str="Untitled"):
        self.title(name + self._title )
        
                        
    def set_size(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        left = (screen_width / 2) - (self._default_width / 2)
        top = (screen_height / 2) - (self._default_height / 2)
        self.geometry('%dx%d+%d+%d' % (
            self._default_width, self._default_height,left, top
            ))        
        
        
    def set_font(self, size:int=9):
        self.text_area.configure(font = ("Consolas", self.font_list[size], "normal"))
        
    def set_zoom(self, size:int=9):
        self.menu_bar.entryconfig(3, label = "🔎 "+self.zoom_list[size])
        
   
        
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ MENU BUILDING ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■   
    
    def _set_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        
    def set_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)   #command=lambda action="new": self.controller.define_action(action)
        file_menu.add_command(label="New", accelerator="Ctrl+N",command=self.controller.new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.controller.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.controller.save_file)
        file_menu.add_command(label="Save as…", accelerator="Ctrl+Shif+S", command=self.controller.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+.", command=self.controller.close_app) 
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        
    def set_edit_menu(self):
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.controller.cut)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.controller.copy)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.controller.paste)
        edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.controller.select_all)
        edit_menu.add_separator()
        
        style_menu = tk.Menu(edit_menu, tearoff=0)
        style_menu.add_command(label="Bold", accelerator="Ctrl+B", command=lambda style= "fb": self.controller.take_text(style))
        style_menu.add_command(label="Italic", accelerator="Ctrl+I", command=lambda style= "fi": self.controller.take_text(style))
        style_menu.add_command(label="Italic Bold", accelerator="Ctrl+B", command=lambda style= "fd": self.controller.take_text(style))
        
        style_menu.add_command(label="Script", command=lambda style= "tn": self.controller.take_text(style))
        style_menu.add_command(label="Script Bold", command=lambda style= "tb": self.controller.take_text(style))
        style_menu.add_command(label="Gothic", command=lambda style= "gn": self.controller.take_text(style))
        style_menu.add_command(label="Gothic Bold", command=lambda style= "gb": self.controller.take_text(style))
        style_menu.add_command(label="Highlighted", command=lambda style= "hn": self.controller.take_text(style))
        style_menu.add_command(label="Sans", command=lambda style= "sn": self.controller.take_text(style))
        style_menu.add_command(label="Sans Italic", command=lambda style= "si": self.controller.take_text(style))
        style_menu.add_command(label="Sans Bold", command=lambda style= "sb": self.controller.take_text(style))
        style_menu.add_command(label="Sans Italic Bold", command=lambda style= "sd": self.controller.take_text(style))
        style_menu.add_command(label="Typewriter", command=lambda style= "wn": self.controller.take_text(style))
        style_menu.add_command(label="Bubble", command=lambda style= "bn": self.controller.take_text(style))
        style_menu.add_command(label="Fullwidth", command=lambda style= "ln": self.controller.take_text(style))
        style_menu.add_command(label="Super Index", command=lambda style= "mn": self.controller.take_text(style))


        style_menu.add_command(label="Remove style", accelerator="Ctrl+B", command=lambda style= "nn": self.controller.take_text(style))
    
        edit_menu.add_cascade(label="Style", menu=style_menu)
        edit_menu.add_separator()
        edit_menu.add_command(label="Date/Time", command=self.controller.print_time)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        
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
        showinfo("Notepad","Developed by Eduardo Trujillo in Python")         