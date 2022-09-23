

import os
from Main.view import View
from Main.extraView import ExtraWindow
from Main.model import Model
import tkinter as tk 
from tkinter.filedialog import *
from datetime import datetime
from tkinter import messagebox as MessageBox

class ViewModel(object):  
    
    file = None
    select_text = ""
    search_word: str = ""
    replace_word: str = ""
    search_list = list()
    
    def __init__(self) -> None:
        self.model = Model()
        self.view = View(self)
        # self.ex_view = ExtraWindow(self)
        
        
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
        
    
    def search(self):
        # Check if use too memory by creating new instances.
        self.enable_replace = tk.StringVar()
        self.input_search = tk.StringVar()
        self.replace_word = tk.StringVar()    
        self.search_view = ExtraWindow(self, "Search")
        
    
            
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
            
            
            
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ SEARCH FUNCTION ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
            
    # TODO     Pending task    :
    # Search inputs send to (search_word)  and (replace_word)
    # For Search function:
    #   ▪ Take all text_area text and save it in lowercase.☑
    #   ▪ Disable styles too to "nn" style.☑
    #   ▪ Make and all positions where (search_word) in text_area.
    #   ▪ Send back the number or array elements to display it in (quantity_label).
    #   ▪ Select the first position and allow move between with NEXT and BACK buttons.
    
    # For Replace function:
    #   ▪ If enable_replace = True, replace_word>'',  and Accept → pressed: 
    #       put on select text position.
    #   ▪ When (enable_replace) = False, (replace_word) = ''.
    
    #! CLEAN MORE THE CODE specially extraView.
            
    # Search_list take each find word position. Need to make first a loop to find all words.
    # Use the array to move between and count total and current position.
    
    # Special characters?? 2 mains options:
    #   Try to change all text:
    #       - Needs to change all text, which could take more time.
    #       - Total compatibility with any special character style.
    #   Do a text_area.search(…) using self.search_word with each style.
    #       - Will require less time.
    #       - Only will be able to find complete style words: 𝑒𝓍𝒶𝓂𝓅𝓁𝑒 ☑, 𝑒𝓍𝒶𝓂𝐩𝐥𝐞	❎
    
    #   Another point to improve the optimization, could add a checkbox to search over styles too.
               
        

            
            
    def search_text(self):
        
        #self.search_word = self.search_word if self.search_word is not None else ""
       
        
        # if S != current entry value → clean list and remove tags:: New search
        print("Prime: ",self.search_word)
        if self.search_word != self.input_search.get():
            #print("ha entrado")
            self.search_list.clear()
            self.view.text_area.tag_remove(tk.SEL, 1.0,"end-1c")
            
        self.search_word = self.input_search.get()
        print("secomd: ",self.search_word)
        # if search exist: and list is empty, start in 1.0
        if self.search_word:
            #if list is not empty, move one position in the list.
            print("search_list: ", self.search_list)
            if self.search_list == []:
                idx = "1.0"
                print("ha entrado")
            else:
                idx = self.search_list[-1]
                #print("idx value: ",idx)
            # indx = indx.first element found. lastidx = end word position.
            idx = self.view.text_area.search(self.search_word, idx, nocase=1, stopindex=tk.END)
            lastidx = '%s+%dc' % (idx, len(self.search_word))
            
            #print("idx value: ",idx)
            #print("lastidx value: ",lastidx)
            # Remove any selection before the found word.
            try:
                self.view.text_area.tag_remove(tk.SEL, 1.0, lastidx)
                
            except:
                pass
            
            # If cant find more elements, go to the exception.
            try:
                # self.view.text_area.focus_set(  )
                # Add new selection in the new find word.
                self.view.text_area.tag_add(tk.SEL, idx, lastidx)
                # Separate the position in row/columns.
                counter_list = []
                counter_list = str(idx).split('.')
                print(counter_list)
                # add a New mark on the new find word, and put focus on it.
                self.view.text_area.mark_set("insert", "%d.%d" % (float(int(counter_list[0])), 
                                                                  float(int(counter_list[1]))))
                self.view.text_area.see(float(int(counter_list[0])))
                # add to the list, 'new index + (leng word)c
                self.search_list.append(lastidx)
                print(self.search_list)
                
            #if dont find more words.
            except:
                MessageBox.showinfo("Search complete","No further matches")
                self.search_list.clear()
                self.view.text_area.tag_remove(tk.SEL, 1.0,"end-1c")
                
            
            
            # Take the text as lowercase none style.
            # all_text = self.view.text_area.get(1.0,tk.END)
            # all_text = map(lambda x: self.model.apply_style(x, 'nn'), all_text)
            # all_text = ''.join(all_text)
            # all_text = all_text.lower()
            # position = all_text.index(self.search_word)   
            
            
            # self.view.text_area.see(position)
            # print(all_text)
            
            # print(self.input_search.get())
            # if self.replace_word.get():
            #     print(self.replace_word.get())
        
        
    def show_replace(self):       
        if self.enable_replace.get() == 'true':
            self.search_view.add_replace_option()
        else:
            self.search_view.remove_replace_option()
        
        
    
    
    

        