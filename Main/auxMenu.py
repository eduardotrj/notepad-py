import tkinter as tk 

class Aux_menu(tk.Listbox):
    # Right click menu to show fast options in base selected text:
    
    # def __init__(self, parent, *args, **kwargs):
    #     tk.Listbox.__init__(self, parent,*args, **kwargs)
    def __init__(self, controller):
        tk.Listbox.__init__(self)
        
        self.controller = controller

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Search", command=self.controller.search)        
   
        style_menu = tk.Menu(self.popup_menu, tearoff=0)
        style_menu.add_command(label="Bold", command=lambda style= "fb": self.controller.take_text(style))
        style_menu.add_command(label="Italic",  command=lambda style= "fi": self.controller.take_text(style))
        style_menu.add_command(label="Italic Bold", command=lambda style= "fd": self.controller.take_text(style))
        style_menu.add_command(label="Script",  command=lambda style= "tn": self.controller.take_text(style))
        style_menu.add_command(label="Script Bold", command=lambda style= "tb": self.controller.take_text(style))
        style_menu.add_command(label="Gothic", command=lambda style= "gn": self.controller.take_text(style))
        style_menu.add_command(label="Gothic Bold", command=lambda style= "gb": self.controller.take_text(style))
        style_menu.add_command(label="Highlighted",  command=lambda style= "hn": self.controller.take_text(style))
        style_menu.add_command(label="Sans", command=lambda style= "sn": self.controller.take_text(style))
        style_menu.add_command(label="Sans Italic", command=lambda style= "si": self.controller.take_text(style))
        style_menu.add_command(label="Sans Bold", command=lambda style= "sb": self.controller.take_text(style))
        style_menu.add_command(label="Sans Italic Bold", command=lambda style= "sd": self.controller.take_text(style))
        style_menu.add_command(label="Typewriter", command=lambda style= "wn": self.controller.take_text(style))
        style_menu.add_command(label="Bubble", command=lambda style= "bn": self.controller.take_text(style))
        style_menu.add_command(label="Fullwidth",  command=lambda style= "ln": self.controller.take_text(style))
        style_menu.add_command(label="Super Index", command=lambda style= "mn": self.controller.take_text(style))
        style_menu.add_command(label="Remove style",  command=lambda style= "nn": self.controller.take_text(style))
        self.popup_menu.add_cascade(label="Style", menu=style_menu)
       
        designs_menu = tk.Menu(self.popup_menu, tearoff=0)
        designs_menu.add_command(label="Line -", command=lambda style= 1: self.controller.print_line(style))
        designs_menu.add_command(label="Line _", command=lambda style= 2: self.controller.print_line(style))
        designs_menu.add_command(label="Line ■", command=lambda style= 3: self.controller.print_line(style))
        designs_menu.add_command(label="Line ░", command=lambda style= 4: self.controller.print_line(style))
        designs_menu.add_command(label="Line ▒", command=lambda style= 5: self.controller.print_line(style))
        designs_menu.add_command(label="Line ▓", command=lambda style= 6: self.controller.print_line(style))
        designs_menu.add_command(label="Line █", command=lambda style= 7: self.controller.print_line(style))
        designs_menu.add_separator()
        designs_menu.add_command(label="Section",  command=lambda style= 1: self.controller.print_title(style))
        designs_menu.add_command(label="Title", command=lambda style= 2: self.controller.print_title(style))
        designs_menu.add_command(label="Subtitle", command=lambda style= 3: self.controller.print_title(style))
        designs_menu.add_command(label="3º Title", command=lambda style= 4: self.controller.print_title(style))     
        designs_menu.add_command(label="1º List", command=lambda style= 5: self.controller.print_title(style))
        designs_menu.add_command(label="2º List", command=lambda style= 6: self.controller.print_title(style))
        designs_menu.add_command(label="3º List", command=lambda style= 7: self.controller.print_title(style))
        designs_menu.add_command(label="Reset title",  command=lambda style= 8: self.controller.print_title(style))   
        # 5, 6, 7 style are for sans style with ●, •, ·.
        self.popup_menu.add_cascade(label="Design", menu=designs_menu)
        
        
        self.popup_menu.add_command(label="Calculate", command=self.controller.calculate)
        self.popup_menu.add_command(label="Add time", command=self.controller.print_time)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="copy", command=self.controller.copy)
        self.popup_menu.add_command(label="cut", command=self.controller.cut)
        self.popup_menu.add_command(label="paste", command=self.controller.paste)
        self.popup_menu.add_command(label="Delete", command=self.controller.delete)
        self.popup_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.controller.select_all)
        
    #def aux_menu(self, x: int=0, y:int=0, entry=""):
        
        
        #self.tk.call('tk_popup', self._w, x, y, entry)
        
    def delete_selected(self):
        print("something") 