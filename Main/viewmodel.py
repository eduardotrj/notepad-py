

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
    search_list_idx = list()
    total_matches: int = 0
    tag_position: int = 0
    
    def __init__(self) -> None:
        self.model = Model()
        self.view = View(self)
        # self.ex_view = ExtraWindow(self)
        
        
        
         # SHORTCUTS:
        self.view.bind("<Control-n>", self.new_file)
        self.view.bind("<Control-o>", self.open_file)
        self.view.bind("<Control-s>", self.save_file)
        self.view.bind("<Control-S>", self.save_as)
        
        self.view.text_area.bind("<Control-Key>", self.control_key_pressed)  #Desactiva ctrl+c, ctrl+v, etc..
        self.view.bind("<Control-m>", self.switch_mode)
        self.view.bind("<Control-plus>", self.zoom_in)
        self.view.bind("<Control-minus>", self.zoom_out)
        self.view.bind("<Control-0>", self.zoom_reset)
        self.view.bind("<KeyPress>", self.key_pressed)
        self.view.bind("<KeyRelease>", self.key_released)
        
        
        # self.view.bind("<Control-1>", self.take_text("fb"))
        # self.view.bind("<Control-2>", self.take_text("fi"))
        # self.view.bind("<Control-3>", self.take_text("fd"))
        
        
        self.view.text_area.bind("<Control-Alt_R>", self.test123)
        # When is pressed, check and transform any key pressed. → key_AltGr
        

        self.view.text_area.bind("<KeyRelease-Return>", self.save_step)
        

    def test123(self, event):
        print("Working!")

    def run(self):
        self.view.run()
        
        
    # Should add more symbols using ALT+GR shorcut.
    # These symbols are used by me to layout .txt documents.   
    def key_AltGr(self, event):
        # Add personal configuration to keyboard:
        # At the moment many of these symbols are not compatible with Tkinder
        if event.keysym=='2':
            self.view.text_area.insert('⚠️')
        elif event.keysym=='3':
            self.view.text_area.insert('‼')
        elif event.keysym=='5':
            self.view.text_area.insert('✶')
        elif event.keysym=='6':
            self.view.text_area.insert('1.0', '●')
        elif event.keysym=='7':
            self.view.text_area.insert('░')
        elif event.keysym=='8':
            self.view.text_area.insert('▒')
        elif event.keysym=='9':
            self.view.text_area.insert('▓')
        elif event.keysym=='0':
            self.view.text_area.insert('█')
        elif event.keysym=='p' or event.keysym=='P':
            self.view.text_area.insert('←')      
        elif event.keysym=='[' or event.keysym=='{':
            self.view.text_area.insert('↑')      
        elif event.keysym==']' or event.keysym=='}':
            self.view.text_area.insert('→')      
        elif event.keysym=="'" or event.keysym=="@":
            self.view.text_area.insert('↓')      
        elif event.keysym=='t' or event.keysym=='T':
            self.view.text_area.insert('■')
        elif event.keysym=='y' or event.keysym=='Y':
            self.view.text_area.insert('▪')
            
        return 'break'
        
    
    # This is to define the shortcut using CTRL.
    def control_key_pressed(self,event):
        
        #! ⚠️ Not all shorcuts allows being rewriten:
        # ctrl + t, ctrl + 5, Ctrl + .
        
        # if event.keysym=='i' or event.keysym=='I':
        #     self.take_text("fi")
        if event.keysym=='r':
            self.take_text("nn")
            
        elif event.keysym=='b' or event.keysym=='2':
            self.take_text("fb")
            
        elif event.keysym=='j' or event.keysym=='3':
            self.take_text("fi")
            
        elif event.keysym=='4':
            self.take_text("fd")
            
        elif event.keysym=='5':
            self.take_text("td")
            
        elif event.keysym=='h' or event.keysym=='6':
            self.take_text("hn")
            
        elif event.keysym=='7':
            self.take_text("sn")
            
        elif event.keysym=='w' or event.keysym=='8':
            self.take_text("wn")
            
        elif event.keysym=='l' or event.keysym=='9':
            self.take_text("ln")
            
        elif event.keysym=='c':
            self.copy()
            
        elif event.keysym=='v':
            self.paste()
             
        elif event.keysym=='a':
            self.select_all() 
             
        elif event.keysym=='x':
            self.cut()
             
        elif event.keysym=='o':
            self.open_file() 
             
        elif event.keysym=='s' and event.keysym=='Shift_L':
            self.save_as() 
            
        elif event.keysym=='s':
            self.save_file()  
             
        elif event.keysym=='.':
            self.close_app() 
            
            
            
            
            
        elif event.keysym=='n':
            self.new_file()  
             
        elif event.keysym=='plus':
            self.zoom_in() 
            
        elif event.keysym=='minus':
            self.zoom_out()  
             
        elif event.keysym=='0':
            self.zoom_reset()     
             
        elif event.keysym=='f':
            self.search()     
             
        elif event.keysym=='m':
            self.switch_mode()            
            
              
        return 'break'
        
    def key_pressed(self, event):
        print("esto: ",event.keysym)
        print(vars(event))

        
        if event.keysym=='Control-2' and event.state & 4:
            print("entro")
            self.take_text("fi")
        elif event.keysym=='Control-m':
            self.switch_mode()
        return "break"
    
    def key_released(self, event):
        print(event.keysym)
        return "break"


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
        self.input_replace = tk.StringVar()    
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

        
        # To add advance search → 
        # 1º funct: search all items and add it to and array, position value?
        # Add quantities to a total_value.
        # return the array and the total_value
        # 2º funct: allos move between array values with buttons next or back.
        # thierd?? replace the array position element for another and remove it.
    
    
    def search_all(self):
        number_matches = 0
         #  Must return an Array with all positions and the number of them.
        
        while self.search_word: 
            if self.search_list == []:  # if list is empty, move one position in the list.
                idx = "1.0"
            else:
                idx = self.search_list[-1]
                
            idx = self.view.text_area.search(self.search_word, idx, nocase=1, stopindex=tk.END) # Search next.
            lastidx = '%s+%dc' % (idx, len(self.search_word))       # define long word.    
           
            
            if idx and lastidx:
                number_matches += 1
                self.search_list_idx.append(idx)
                self.search_list.append(lastidx)    
            
            else:
                break
            
        return number_matches #, self.search_list
            
            
    def search_text(self):
        
    #self.search_word = self.search_word if self.search_word is not None else ""
       
       # search_list:  ['4.10+2c', '5.8+2c', '6.13+2c', '8.12+2c', '27.14+2c']
       # print("Prime: ",self.search_word)

       
        #if self.replace_word != self.replace_word.get():
        #    pass
       
        self.search_word = self.input_search.get()
        self.replace_word = self.input_replace.get()
        
        if self.search_word and self.replace_word and self.total_matches > 0:
           # self.select_tag()
        #! IF exist replace_word → Remplace word
            self.replace_text()
        
        if self.search_word:
            # if S != current entry value → clean list and remove tags:: New search
            #if self.search_word != self.input_search.get():
            self.search_list.clear()
            self.search_list_idx.clear()
            self.view.text_area.tag_remove(tk.SEL, 1.0,"end-1c")
            self.total_matches = 0
            self.tag_position = 0
                
            #self.search_word = self.input_search.get()
            
            self.total_matches = self.search_all()
            
            if self.total_matches > 0:
                self.select_tag()
            else:
                #! NEED TO AVOID CLOSE WINDOW
                MessageBox.showinfo("Search complete","No matches")
                print("0 MATCHES")
        
        
    def select_tag(self):
        self.search_view.updating_results()   
        # '27.14+2c'  idx = 27.14 
        
        # lastidx =  self.search_list_idx[self.tag_position]
        #lastidx = lastidx.removesuffix('+c') 
        # lastidx = lastidx[:lastidx.rfind("+")]
        
        lastidx = self.search_list[self.tag_position]
        idx = self.search_list_idx[self.tag_position]

        
        self.view.text_area.tag_remove(tk.SEL, 1.0, "end-1c")
        
        # Add new selection in the new find word.
        self.view.text_area.tag_add(tk.SEL, idx, lastidx)
        
        # Separate the position in row/columns.
        counter_list = []
        counter_list = str(idx).split('.')
        
        # add athe pointer entry before the new find word, and put focus on it.
        self.view.text_area.mark_set("insert", "%d.%d" % (float(int(counter_list[0])), 
                                                            float(int(counter_list[1]))))
        self.view.text_area.see(float(int(counter_list[0])))
        
    def replace_text(self): 
        lastidx = self.search_list[self.tag_position]
        idx = self.search_list_idx[self.tag_position]
        
        self.view.text_area.delete(idx,lastidx)
        self.view.text_area.insert(idx,self.replace_word) 
        
        
    def next_tag(self):      
        if self.tag_position >= (self.total_matches-1):
            self.tag_position = 0
        else:
            self.tag_position += 1
    
        self.select_tag()
        
        
    def last_tag(self): 
        if self.tag_position <= 0:
            self.tag_position = (self.total_matches-1)
        else:
            self.tag_position -= 1
            
        self.select_tag()   
        
        
        
    def show_replace(self):       
        if self.enable_replace.get() == 'true':
            self.search_view.add_replace_option()
        else:
            self.search_view.remove_replace_option()
            
            

    def auto_save(self):
        pass
    
    def save_step(self):
        # Must be called after press any arrow, enter, backspace or (click and write)
        # print("The cursor is at: ", entry.index(INSERT))
        print("hello")
        pass
        
        
        
        
        
        
        
    #* TO ADD UNDO, REDO:
    # Create a list with 10 positions.
    # Remove last and add new in 0.
    # Add a copy of all text automatically with each change (when focus or actie end)
    # Undo → increase list(n)
    # Redo → decrease list(n)
    
    
    

                    
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
               