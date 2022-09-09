
import os
from Main.view import View
from Main.model import Model
import tkinter as tk 
from tkinter.filedialog import *
from datetime import datetime

class ViewModel(object):  
    
    file = None
    select_text = ""
    
    def __init__(self) -> None:
        self.model = Model()
        self.view = View(self)
        
        
         # SHORTCUTS:
        self.view.bind("<Control-n>", self.new_file)
        self.view.bind("<Control-o>", self.open_file)
        self.view.bind("<Control-s>", self.save_file)
        self.view.bind("<Control-S>", self.save_as)
        
        self.view.bind("<Control-m>", self.switch_mode)
        self.view.bind("<Control-plus>", self.zoom_in)
        self.view.bind("<Control-minus>", self.zoom_out)
        self.view.bind("<Control-0>", self.zoom_reset)


    def run(self):
        self.view.run()
        


    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ FILE FUNCTIONS ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ 
    
    def new_file(self, event=1):
        self.view.set_title()
        self.file = None
        self.view.text_area.delete(1.0,tk.END)


    def open_file(self, event=1): 
        self.file = askopenfilename(
            defaultextension=".txt", filetypes=[("All Files","*.*"), ("Text Documents","*.txt")]
            ) 
        if self.file == "":     # No file to open 
            self.file = None     
        else:                   # Try to open the file
            self.view.set_title(os.path.basename(self.file)) 
            self.view.text_area.delete(1.0,tk.END) 
            file = open(self.file,"r") 
            self.view.text_area.insert(1.0,file.read()) 
            file.close()
            
            
    def save_file(self, event=1): 
        if self.file == None:   # Save as new file 
            self.save_as()        
        else:                   # Choose an existing file
            file = open(self.file,"w") 
            file.write(self.view.text_area.get(1.0,tk.END)) 
            file.close() 
            
            
    def save_as(self, event=1):
        self.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", 
                                      filetypes=[("All Files","*.*"), ("Text Documents","*.txt")]) 
        if self.file == "": 
            self.file = None
        else:                   # Try to save the file 
            file = open(self.file,"w") 
            file.write(self.view.text_area.get(1.0,tk.END)) 
            file.close() 
            self.view.set_title(os.path.basename(self.file))
            
            
    def close_app(self):
        self.view.destroy()
            
        
        
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ EDIT FUNCTIONS ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■     
    
    def cut(self): 
        self.view.text_area.event_generate("<<Cut>>") 


    def copy(self): 
        self.view.text_area.event_generate("<<Copy>>") 


    def paste(self): 
        self.view.text_area.event_generate("<<Paste>>") 
        
        
    def select_all(self, event=1):
        self.view.text_area.tag_add('sel', '1.0', 'end')    
        
    
    # It's sent a data with the code style.
    def take_text(self, style:str="nn" ):
        if self.view.text_area.selection_get():
            
            print("the style taken: ",style)
            self.select_text = self.view.text_area.selection_get()
            self.select_text = [*self.select_text]
  
            line, column = map(int, self.view.text_area.index('sel.first').split('.'))
            position = (str(line) + "." + str(column))
            self.view.text_area.delete('sel.first','sel.last')
            
            new_character_list = map(lambda x: self.model.apply_style(x, style), self.select_text)
            #print(list(new_character_list))    #! LEAVE TO CHECK ERROrs
            new_text = ''.join(new_character_list)
            print(new_text)
            self.view.text_area.insert(position,new_text)       
    
        
    def print_time(self):       # 00:44 08/09/2022  date/time
        time = datetime.now()
        time = time.strftime("%H:%M %d/%m/%Y")
        pointer = self.view.text_area.index(tk.INSERT)
        self.view.text_area.insert(pointer,time)
        
        
        
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ VIEW FUNCTIONS ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■     
    # Apply zoom in base font-size  
    def zoom_in(self, event=1):
        if self.view.n_font<32: self.view.n_font +=1
        self.view.set_font(self.view.n_font)
        self.view.set_zoom(self.view.n_font)
        

    def zoom_out(self, event=1):
        if self.view.n_font>0: self.view.n_font -=1
        self.view.set_font(self.view.n_font)
        self.view.set_zoom(self.view.n_font)
        
      
    def zoom_reset(self, event=1):
        self.view.n_font = self.view.default_size
        self.view.set_font(self.view.n_font)
        self.view.set_zoom(self.view.n_font)
        
        
        
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ NIGHT MODE FUNCTION ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■     
    
    def switch_mode(self, event=1):     
        if self.view.day_mode == "🌙" :
            self.view.text_area.configure(bg="black", fg="white")
            self.view.day_mode = "🌞"
            self.view.menu_bar.entryconfig(5, label = "🌞")  
                  
        else:
            self.view.text_area.configure(bg="white", fg="black")
            self.view.day_mode = "🌙"
            self.view.menu_bar.entryconfig(5, label="🌙")
            

        