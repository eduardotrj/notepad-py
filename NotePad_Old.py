
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from ctypes import windll

#Allow to show the text sharp.
windll.shcore.SetProcessDpiAwareness(1)
#     __root.tk.call('tk', 'scaling', 1.0)


    #Add a explain of funct
class Notepad:
    
    __root = Tk() 
    __text_area = Text(__root)
    __scrollbar = Scrollbar(__text_area)
    __menu_bar = Menu(__root)

    
# Default Values:
    __title = "Notepad"
    __space_title = " - "
    __default_width = 600
    __default_height = 400
    __file = None
    __n_font =  9
    __day_mode = "🌙"
    __font_list = (1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,18,19,20,21,22,24,26,28,30,33,36,39,43,48,54,60,72,84)
    __zoom_list = ("10%","20%","30%","40%","50%","60%","70%","80%","90%","100%","110%","120%","130%","140%","150%","160%","170%","180%","190%","200%","220%","240%","260%","280%","300%","320%","350%","400%","440%","500%","550%","600%","800%")
    __text_area.configure(font = ("Consolas", __font_list[__n_font], "normal"))
    __font_style = ()
    __select_text = ""
    
    __nn = ('0', '1', '2' ,'3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
    __fb = ('𝟎', '𝟏', '𝟐', '𝟑', '𝟒', '𝟓', '𝟔', '𝟕', '𝟖', '𝟗', '𝐀', '𝐁', '𝐂', '𝐃', '𝐄', '𝐅', '𝐆', '𝐇', '𝐈', '𝐉', '𝐊', '𝐋', '𝐌', '𝐍', '𝐎', '𝐏','𝐐', '𝐑', '𝐒', '𝐓', '𝐔', '𝐕', '𝐖', '𝐗', '𝐘', '𝐙', '𝐚', '𝐛', '𝐜', '𝐝', '𝐞', '𝐟', '𝐠', '𝐡', '𝐢', '𝐣', '𝐤', '𝐥', '𝐦', '𝐧', '𝐨', '𝐩', '𝐪', '𝐫', '𝐬', '𝐭', '𝐮', '𝐯', '𝐰', '𝐱', '𝐲', '𝐳')
    __fi = ('𝟶', '𝟷', '𝟸', '𝟹', '𝟺', '𝟻', '𝟼', '𝟽', '𝟾', '𝟿', '𝐴', '𝐵', '𝐶', '𝐷', '𝐸', '𝐹', '𝐺', '𝐻', '𝐼', '𝐽', '𝐾', '𝐿', '𝑀', '𝑁', '𝑂', '𝑃', '𝑄', '𝑅', '𝑆', '𝑇', '𝑈', '𝑉', '𝑊', '𝑋', '𝑌', '𝑍', '𝑎', '𝑏', '𝑐', '𝑑', '𝑒', '𝑓', '𝑔', 'ℎ', '𝑖', '𝑗', '𝑘', '𝑙', '𝑚', '𝑛', '𝑜', '𝑝', '𝑞', '𝑟', '𝑠', '𝑡', '𝑢', '𝑣', '𝑤', '𝑥', '𝑦', '𝑧')
    __fd = ('𝟎', '𝟏', '𝟐', '𝟑', '𝟒', '𝟓', '𝟔', '𝟕', '𝟖', '𝟗', '𝑨', '𝑩', '𝑪', '𝑫', '𝑬', '𝑭', '𝑮', '𝑯', '𝑰', '𝑱', '𝑲', '𝑳', '𝑴', '𝑵', '𝑶', '𝑷', '𝑸', '𝑹', '𝑺', '𝑻', '𝑼', '𝑽', '𝑾', '𝑿', '𝒀', '𝒁', '𝒂', '𝒃', '𝒄', '𝒅', '𝒆', '𝒇', '𝒈', '𝒉', '𝒊', '𝒋', '𝒌', '𝒍', '𝒎', '𝒏', '𝒐', '𝒑', '𝒒', '𝒓', '𝒔', '𝒕', '𝒖', '𝒗', '𝒘', '𝒙', '𝒚', '𝒛')
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■ CONSTRUCTOR ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■     
    def __init__(self, **kwargs): 
    #SIZE:
        try:
            self.__default_width = kwargs['width']
        except KeyError:
            print("Not any width was specified.")
        
        try:
            self.__default_height = kwargs['height']
        except KeyError:
            print("Not any height was specified.")
        
    # TITLE & ICON:
        self.__set_title()
        
        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            print("the Notepad.ico was not found.")
        
    # MENU:    
        __file_menu = Menu(self.__menu_bar, tearoff=0)
        __file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.__new_file)
        __file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.__open_file)
        __file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.__save_file)
        __file_menu.add_command(label="Save as…", accelerator="Ctrl+Shif+S", command=self.__save_as)
        __file_menu.add_separator()
        __file_menu.add_command(label="Exit", accelerator="Ctrl+.", command=self.__close_app)
        self.__menu_bar.add_cascade(label="File", menu=__file_menu)
        
        __edit_menu = Menu(self.__menu_bar, tearoff=0)
        __edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.__cut)
        __edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.__copy)
        __edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.__paste)
        __file_menu.add_separator()
        
        __style_menu = Menu(__edit_menu, tearoff=0)
        __style_menu.add_command(label="Bold", accelerator="Ctrl+B", command=self.__bold_serif)
        __style_menu.add_command(label="Italic", accelerator="Ctrl+I", command=self.__italic_serif)
        __style_menu.add_command(label="Italic Bold", accelerator="Ctrl+B", command=self.__bold_italic_serif)
        __style_menu.add_command(label="Remove style", accelerator="Ctrl+B", command=self.__none_style)
        __edit_menu.add_separator()
        __edit_menu.add_cascade(label="Style", menu=__style_menu)
        __edit_menu.add_separator()
        __edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.__select_all)

        self.__menu_bar.add_cascade(label="Edit", menu=__edit_menu)
        
        __view_menu = Menu(self.__menu_bar, tearoff=0)
        __view_menu.add_command(label="Zoom In", accelerator="Ctrl+Plus", command=self.__zoom_in)
        __view_menu.add_command(label="Zoom Out", accelerator="Ctrl+minus", command=self.__zoom_out)
        __view_menu.add_command(label="Restore Zoom", accelerator="Ctrl+0", command=self.__zoom_reset)
        self.__menu_bar.add_cascade(label="🔎 100%", menu=__view_menu)
        
        __help_menu = Menu(self.__menu_bar, tearoff=0)
        __help_menu.add_command(label="About NotePad", command=self.__show_about)
        self.__menu_bar.add_cascade(label="About…", menu=__help_menu)
        
        self.__menu_bar.add_command(label=self.__day_mode, command=self.__switch_mode) # Modo 🌞🌙
        
        self.__root.config(menu=self.__menu_bar)
        
        
    # SHORTCUTS:
        self.__root.bind("<Control-n>", self.__new_file)
        self.__root.bind("<Control-o>", self.__open_file)
        self.__root.bind("<Control-s>", self.__save_file)
        self.__root.bind("<Control-S>", self.__save_as)
        
        self.__root.bind("<Control-m>", self.__switch_mode)
        self.__root.bind("<Control-plus>", self.__zoom_in)
        self.__root.bind("<Control-minus>", self.__zoom_out)
        self.__root.bind("<Control-0>", self.__zoom_reset)

        
    # POSITION:
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        left = (screen_width / 2) - (self.__default_width / 2)
        top = (screen_height / 2) - (self.__default_height / 2)
        self.__root.geometry('%dx%d+%d+%d' % (
            self.__default_width, self.__default_height, left, top
            ))
        
    # CONTENT:
        self.__text_area.grid(sticky = N + E + S + W)
        self.__scrollbar.pack(side=RIGHT,fill=Y)
        self.__scrollbar.config(command=self.__text_area.yview)
        self.__text_area.config(yscrollcommand=self.__scrollbar.set)
        
        
    # CONFIGURATION:
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1) 

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■ FUNCTIONS ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■        
    def __set_title(self,name="Untitled"):
        self.__root.title(name + self.__space_title + self.__title)

        
# FUNCTIONS FILE:       
    def __new_file(self, event=1):
        self.__set_title()
        self.__file = None
        self.__text_area.delete(1.0,END)
        print(type(event))
        
        
    def __open_file(self, event=1): 
        self.__file = askopenfilename(defaultextension=".txt", 
									filetypes=[("All Files","*.*"), 
										("Text Documents","*.txt")]) 
        if self.__file == "":   # no file to open 
            self.__file = None     
        else:                   # Try to open the file
            self.__set_title(os.path.basename(self.__file)) 
            self.__text_area.delete(1.0,END) 
            file = open(self.__file,"r") 
            self.__text_area.insert(1.0,file.read()) 
            file.close()
            
            
    def __save_file(self, event=1): 
        if self.__file == None: # Save as new file 
            self.__save_as()        
        else: 
            file = open(self.__file,"w") 
            file.write(self.__text_area.get(1.0,END)) 
            file.close() 
            
    def __save_as(self, event=1):
        self.__file = asksaveasfilename(initialfile='Untitled.txt', 
											defaultextension=".txt", 
											filetypes=[("All Files","*.*"), 
												("Text Documents","*.txt")]) 
        if self.__file == "": 
            self.__file = None
        else:                   # Try to save the file 
            file = open(self.__file,"w") 
            file.write(self.__text_area.get(1.0,END)) 
            file.close() 
            self.__set_title(os.path.basename(self.__file))
                
            
    def __close_app(self):
        self.__root.destroy()
   
# FUNCTIONS EDIT:    
    def __cut(self): 
        self.__text_area.event_generate("<<Cut>>") 

    def __copy(self): 
        self.__text_area.event_generate("<<Copy>>") 

    def __paste(self): 
        self.__text_area.event_generate("<<Paste>>") 
        
        
    ## TEXT STYLES  ____________________________
    # Get the desired font and put in __font_style (tupla)
    def __bold_serif(self, event=1):
        self.__font_style = self.__fb
        self.__take_text()
    def __italic_serif(self, event=1):
        self.__font_style = self.__fi
        self.__take_text()
    def __bold_italic_serif(self, event=1):
        self.__font_style = self.__fd
        self.__take_text()
    def __none_style(self, event=1):
        self.__font_style = self.__nn
        self.__take_text()
    
    

    
    # 1. Gets the select text.
    # 2. Get the select positions (line, column)
    # 3. Clean the select zone.
    # 4. Send char by char to appy style and receive the same text with other style.
    # 5. Insert it.
    def __take_text(self):
        if self.__text_area.selection_get():
            self.__select_text = self.__text_area.selection_get()
            self.__select_text = [*self.__select_text]
            
            line, column = map(int, self.__text_area.index('sel.first').split('.'))
            position = (str(line) + "." + str(column))
            self.__text_area.delete('sel.first','sel.last')
            #print(old_character_list)
            new_character_list = map(self.apply_style, self.__select_text)
            #print(list(new_character_list))    #! LEAVE TO CHECK ERROrs
            new_text = ''.join(new_character_list)
            print(new_text)
            self.__text_area.insert(position,new_text)
               
    # clean the name of the fonts styles (tupla).
    # Find in which tupla is the character, get the index and apply it on the desired style tupla.
    def apply_style(self,b): #arguments:  [<__main__.Notepad object at 0x0000019FFDB0DE40>, 'd']
          
        nn = self.__nn
        fb = self.__fb
        fi = self.__fi
        fd = self.__fd
        new_chart = ""
        select_style = self.__font_style
        
        # print("fuente seleccionada: ",selected_style)
        print("Initial chart value: ", b)
        #check if is
        if b in nn:
            new_chart = nn.index(b)
            new_chart = select_style[new_chart]
            print("The chart received: ",new_chart)
            return(new_chart)
        elif b in fb:
            new_chart = fb.index(b)
            new_chart = select_style[new_chart]
            print("The chart received: ",new_chart)
            return(new_chart)
        elif b in fi:
            new_chart = fi.index(b)
            new_chart = select_style[new_chart]
            print("The chart received: ",new_chart)
            return(new_chart)
        elif b in fd:
            new_chart = fd.index(b)
            new_chart = select_style[new_chart]
            print("The chart received: ",new_chart)
            return(new_chart)
        else:
            print("else es: ",b)
            return(b)
        
    # Require test on:    *Fixed in the new version on MVVM.
       # asd asd-a      → Create a error with the 2º d
       # 123 asd-asd-a  → Create a error with the 1º d
    

        
    def __select_all(self, event=1):
        self.__text_area.tag_add('sel', '1.0', 'end')
        
        
        
# FUNCTION VIEW:
    def __zoom_in(self, event=1):
        if self.__n_font<32: self.__n_font +=1
        self.__text_area.configure(font = ("Consolas", self.__font_list[self.__n_font], "normal"))
        self.__menu_bar.entryconfig(3, label = "🔎 "+self.__zoom_list[self.__n_font])
        print("The new zoom is "+self.__zoom_list[self.__n_font])

    def __zoom_out(self, event=1):
        if self.__n_font>0: self.__n_font -=1
        self.__text_area.configure(font = ("Consolas", self.__font_list[self.__n_font], "normal"))
        self.__menu_bar.entryconfig(3, label = "🔎 "+self.__zoom_list[self.__n_font])
        print("The new zoom is "+self.__zoom_list[self.__n_font])
      
    def __zoom_reset(self, event=1):
        self.__n_font = 9
        self.__text_area.configure(font = ("Consolas",  self.__font_list[self.__n_font], "normal"))
        self.__menu_bar.entryconfig(3, label = "🔎 "+self.__zoom_list[self.__n_font])
        print("The new zoom is "+self.__zoom_list[self.__n_font])    
  
        
# FUNCTIONS ABOUT:         
    def __show_about(self): 
        showinfo("Notepad","Developed by Eduardo Trujillo in Python") 
        
        
# FUNCTION MODE:           
    def __switch_mode(self, event=1):
        if self.__day_mode == "🌙" :
            self.__text_area.configure(bg="black", fg="white")
            self.__day_mode = "🌞"
            self.__menu_bar.entryconfig(5, label = "🌞")
            
        else:
            self.__text_area.configure(bg="white", fg="black")
            self.__day_mode = "🌙"
            self.__menu_bar.entryconfig(5, label="🌙")

    
    def run(self):
        self.__root.mainloop()
        
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■ END CLASS ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■     
    
notepad = Notepad(width=1050,height=600) 

notepad.run()

    
    

    
    