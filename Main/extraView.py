import tkinter as tk 
from tkinter import ttk


#Option to create a class which create generic windows. 
#In base the desired option, add a searh profile, settings, profile, etc...

# to choice which window is desire, needs receive a name.
class ExtraWindow():
    _title = "Search"
    _width = 500
    _height = 200
    
    def __init__(self, controller, name:str) -> None:
        super().__init__()
        
        self.controller = controller
        root_frame = controller.view
    
        # new_window = tk.Toplevel(root_frame)  
        self.open_window(root_frame)
        self.window_title(name)
        self.window_icon(name)
        
        if name == "Search":
             self.search_view()
             
        self.position(root_frame)
        
    
    def open_window(self,root_frame):
        self.new_window = tk.Toplevel(root_frame)  
        self.new_window.grid_columnconfigure(0, weight=1)
        self.new_window.grid_rowconfigure(0, weight=1)
    
    def window_title (self, name="Pad"):
        self.new_window.title(name)
        
    def window_icon(self, name):
        self.new_window.iconbitmap('Assets/Icons/Note'+name+'_32.ico' )

        
    def position(self, root_frame):
        # To put the new window in the middle of the root window:
        # position_x = root_position + (root_width / 2) - ( widget_width/2)
        widget_x, widget_y = root_frame.winfo_rootx(), root_frame.winfo_rooty() 
        widget_width, widget_height = root_frame.winfo_width(), root_frame.winfo_height()	
        
        left = (widget_x + widget_width/2) - (self._width / 2)
        top = (widget_y + widget_height/2 - 50) - (self._height / 2)
        self.new_window.geometry('%dx%d+%d+%d' % (
            self._width, self._height,left, top
            )) 
        
    
            
    def search_view(self):
        #Min width and height: 380, 175
        
        search_word = ""#tk.StringVar()
        
        enable_replace: bool = False

        self.new_window.minsize(380, 175)
        self.search_frame = tk.Frame(self.new_window)
        
        
        label_title = ttk.Label(master = self.search_frame, text = "Search:")
        label_title.grid(column=0, row=0, sticky='w')
        
        search_input = ttk.Entry(master = self.search_frame, textvariable = self.controller.search_word)
        search_input.grid(column=0, row=1, columnspan=2, sticky='ew', padx=10, pady=4)
        
        quantity_label = ttk.Label(master = self.search_frame, text = "0 found")
        quantity_label.grid(column=2, row=1, padx=10, pady=4, sticky='w')
        
        replace_check = ttk.Checkbutton(
            master = self.search_frame, 
            text = "Replace", 
            command=self.controller.show_replace,
            variable=self.controller.enable_replace,
            onvalue='true',
            offvalue='false'
            )
        replace_check.grid(column=2, row=2, padx=10, pady=4, sticky='w')
        
        back_button = ttk.Button(self.search_frame, text = "Back", style='TButton') #command
        #back_button.config(bg='#f7cd5a')
        back_button.grid(column=0, row=3, padx=10, pady=10, sticky='ws')
        
        
        
        next_button = ttk.Button(self.search_frame, text = "Next") #command
        next_button.grid(column=1, row=3, padx=10, pady=10, sticky='ws')
        
        accept_button = ttk.Button(self.search_frame, text = "Accept", command = self.controller.search_text) #command
        accept_button.grid(column=2, row=3, padx=10, pady=10, sticky='s')
        
        self.search_frame.grid(row=0, padx=10, pady=10,sticky='nsew')
        
        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_frame.grid_rowconfigure(3, weight=1)
        
        print(search_word)
        
    def add_replace_option(self):
        self.replace_input = ttk.Entry(master = self.search_frame, textvariable = self.controller.replace_word)
        self.replace_input.grid(column=0, row=2, columnspan=2, sticky='ew', padx=10, pady=4)
        
    def remove_replace_option(self):
        self.replace_input.grid_remove()
    

