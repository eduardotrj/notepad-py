import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox as msgb


#Option to create a class which create generic windows. 
#In base the desired option, add a searh profile, settings, profile, etc...

# to choice which window is desire, needs receive a name.
class ExtraWindow():
    """ Manage the creation of others windows.
    """
    #_title = "Search"
    _title: str = ""
    _width: int = 500
    _height: int = 200
    existWindow: bool = False
    _focusElement: object
    
    
    def __init__(self, controller: object, name:str = "") -> None:
        """Create a new window and find which kind of window by Name.

        Args:
            controller (object): _description_          → Controller//Viewmodel obj.
            name (str, optional): _description_. Defaults to "".    → new Window name.
        """
        super().__init__()  
        self.name = name 
        self.controller = controller
        root_frame = controller.view
    
        self.open_window(root_frame)
        self.window_title(name)
        self.window_icon(name)
        
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        # if (isinstance.search_frame()):
        #self.open_window.protocol("WM_DELETE_WINDOW", self.open_window.iconify)
        # make Esc exit the program
        #self.open_window.bind('<Escape>', lambda e: self.open_window.destroy())
        
        if name == "Search":
            self.search_view()
        elif name == "Info" or name == "warning" or name == "Error":
            self.showMessage("No results found.")
            
        # def showMessage(self, message, type='info', timeout=2500):
             
        self.position(root_frame)
        
    
    def open_window(self,root_frame: object):
        """ Draw the new Widget window 1:1.

        Args:
            root_frame (object): _description_  → To which element is linked.
        """
        self.new_window = tk.Toplevel(root_frame)  
        self.new_window.grid_columnconfigure(0, weight=1)
        self.new_window.grid_rowconfigure(0, weight=1)
    
    
    def window_title (self, name:str):
        self.new_window.title(name)
        
        
    def window_icon(self, name:str="Pad"):
        self.new_window.iconbitmap('Assets/Icons/Note'+name+'_32.ico' )

        
    def position(self, root_frame: object):
        """Define position and size of the new window.

        Args:
            root_frame (object): _description_
        """
        # TODO use to select different size windows.
        # To put the new window in the middle of the root window:
        # position_x = root_position + (root_width / 2) - ( widget_width/2)
        widget_x, widget_y = root_frame.winfo_rootx(), root_frame.winfo_rooty() 
        widget_width, widget_height = root_frame.winfo_width(), root_frame.winfo_height()	
        
        left = (widget_x + widget_width/2) - (self._width / 2)
        top = (widget_y + widget_height/2 - 50) - (self._height / 2)
        self.new_window.geometry('%dx%d+%d+%d' % (
            self._width, self._height,left, top
            )) 
        
    def on_closing(self):
        """Delete the window instance when close.
        """
        self.new_window.destroy()
        self.controller.delete_instance(self)
        

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■ SEARCH WINDOW  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    def search_view(self):
        """ Set elements inside of Search Window.
        
        Details:
        ▪ Size: 380 x 175.                              [3 Columns, 4 Rows]
        ▪ Label: label_title            "Search".       Position [0,0]
        ▪ Input: Search_input.                          Position [0,1]-[1,1]
        ▪ Label: Quantity_label         "0 found"       Position [2,1]
        ▪ CheckButton: replace_check    "Replace"       Position [2,2]
        ▪ Button: back_button           "Back"          Position [0,3]
        ▪ Button: next_button           "Next"          Position [1,3]
        ▪ Button: accept_button         "Accept"        Position [2,3]
        
        """
        self.new_window.minsize(380, 175)   #* Min width and height: 380, 175
        self.search_frame = tk.Frame(self.new_window)
        label_title = ttk.Label(master = self.search_frame, text = "Search:")
        label_title.grid(column=0, row=0, sticky='w')
        search_input = ttk.Entry(master = self.search_frame, textvariable = self.controller.input_search)
        search_input.grid(column=0, row=1, columnspan=2, sticky='ew', padx=10, pady=4)
        self._focusElement = search_input
        self.focus_search()         # search_input.focus_set()
        self.quantity_label = ttk.Label(master = self.search_frame, text = "0 found")
        self.quantity_label.grid(column=2, row=1, padx=10, pady=4, sticky='w')
        
        replace_check = ttk.Checkbutton(
            master = self.search_frame, 
            text = "Replace", 
            command=self.controller.show_replace,
            variable=self.controller.enable_replace,
            onvalue='true',
            offvalue='false'
            )
        replace_check.grid(column=2, row=2, padx=10, pady=4, sticky='w')
        back_button = ttk.Button(self.search_frame, text = "Back", style='TButton', command = self.controller.last_tag)
        #back_button.config(bg='#f7cd5a')
        back_button.grid(column=0, row=3, padx=10, pady=10, sticky='ws')
        
        next_button = ttk.Button(self.search_frame, text = "Next", command = self.controller.next_tag)
        next_button.grid(column=1, row=3, padx=10, pady=10, sticky='ws')

        accept_button = ttk.Button(self.search_frame, text = "Accept", command = self.controller.search_text) #command
        accept_button.grid(column=2, row=3, padx=10, pady=10, sticky='s')
        
        self.search_frame.grid(row=0, padx=10, pady=10,sticky='nsew')
        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_frame.grid_rowconfigure(3, weight=1)

    def focus_search(self):
        """Apply focus on the window or element desired.
        """
        self._focusElement.focus_set()
        
        
    def add_replace_option(self):
        """ When in Search_view, CheckButton "replace_check" is active, add:
        ▪ Input: replace_input                          Position [0,2]-[1,2]
        """
        self.replace_input = ttk.Entry(master = self.search_frame, textvariable = self.controller.input_replace)
        self.replace_input.grid(column=0, row=2, columnspan=2, sticky='ew', padx=10, pady=4)
        
        
    def remove_replace_option(self):
        """ When in Search_view, CheckButton "replace_check" is disable, remove:
        ▪ Input: replace_input                          Position [0,2]-[1,2]
        """
        self.replace_input.grid_remove()
    
    def updating_results(self):
        """In Search_view, reemplace text on:
        ▪ Label: Quantity_label         "nº found"       Position [2,1]
        """
        self.quantity_label.config(text = str(self.controller.tag_position+1) + "/" + str(self.controller.total_matches) + " found")

# <Main.extraView.ExtraWindow object at 0x000001E8C3441950>



# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■ ALERS WINDOW  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

    
class MessageWindow:
    """ Create Toplevel Widgets.
    """
    DURATION: str = 2000
        
    def show_message(message:str="", type:str='info', timeout:int=2500):
        """ Create a Toplevel Widget to show messages, alerts and erros.
        
        These windows are closing after timeout time.

        Args:
            message (str, optional): _description_. Defaults to "".
            type (str, optional): _description_. Defaults to 'info'.
            timeout (int, optional): _description_. Defaults to 2500.
        """        
        root = tk.Tk()
        root.withdraw()

        try:
            print(message)
            root.after(timeout, root.destroy)
            if type == 'info':
                msgb.showinfo('Info', message, master=root)
            elif type == 'warning':
                msgb.showwarning("Warning" , message, master=root)
            elif type == 'error':
                msgb.showerror('Error', message, master=root)
        except:
            pass      