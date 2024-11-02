

import os
import gc
from collections import OrderedDict
from Main.view import View
from Main.extraView import ExtraWindow
from Main.auxMenu import Aux_menu
from Main.model import Model
from Main.calculate import Calculation
# from Main.searchMenu import SearchMenu
import tkinter as tk 
from tkinter.filedialog import *
from datetime import datetime
from tkinter import messagebox as MessageBox



class ViewModel(object):  
    
    instances = []
    file = None
    select_text = ""
    search_word: str = ""
    replace_word: str = ""
    search_list = list()
    search_list_idx = list()
    total_matches: int = 0
    tag_position: int = 0
    titles_dict: dict = {}
    sub_titles_dict: dict = {}
    key_alt_r: bool = False
    key_control_l: bool = False
    index_start: str = "▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"
    #index_end: str = "▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
    sub_index: str =  "■"
    
    
    def __init__(self) -> None:
        #self.name = name
        self.model = Model()#
        self.calc = Calculation()
        self.view = View(self)
        self.instances.append(self.view)
        # self.aux_menu = Aux_menu(self)
        self.search_view = None
        
                
        
         # SHORTCUTS:
        self.view.bind("<Control-n>", self.new_file)
        self.view.bind("<Control-o>", self.open_file)
        self.view.bind("<Control-s>", self.save_file)
        self.view.bind("<Control-S>", self.save_as)
        
        #self.view.text_area.bind("<Control-Key>", self.control_key_pressed)  #Desactiva ctrl+c, ctrl+v, etc..
        self.view.bind("<Control-m>", self.switch_mode)
        self.view.bind("<Control-plus>", self.zoom_in)
        self.view.bind("<Control-minus>", self.zoom_out)
        self.view.bind("<Control-0>", self.zoom_reset)
        self.view.bind("<KeyPress>", self.key_pressed)
        self.view.bind("<KeyRelease>", self.key_released)
        
        self.view.bind("<Button-3>", self.callAux) 
        
        #self.view.bind("<Alt_R>", self.key_AltGr)
        
        
        self.view.text_area.bind("<Control-Alt_R>", self.test123)
        # When is pressed, check and transform any key pressed. → key_AltGr
        

        self.view.text_area.bind("<KeyRelease-Return>", self.save_step)
        
        
    def test123(self, event):
        print("Working!")

    def run(self):
        self.view.run()
        
    def callAux(self, event):
        self.left_menu = Aux_menu(self)
        
        try:
            self.left_menu.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.left_menu.popup_menu.grab_release()
            
            # left_menu Before was called search_view
        
    def do_operations(self):
        if self.view.text_area.selection_get():
            
            
            self.select_text = self.view.text_area.selection_get()
            # self.select_text = [*self.select_text]
       
            
            
            line, column = map(int, self.view.text_area.index('sel.first').split('.'))
            position = (str(line) + "." + str(column))
            self.view.text_area.delete('sel.first','sel.last')
            
            operation:str = self.select_text
            
            solution = self.calc.calculate(operation)
            # Calculation.calculate(operation)
         
            self.view.text_area.insert(position,solution) 
       
        
    # def open_search(self):
    #     self.searchMenu = SearchMenu(self)
    #     self.searchMenu.search()
        
        #self.model.apply_style(x, "fb"), self.select_text)
    

        
    # To get information about keys    
    def key_pressed(self, event):
        
        if event.keysym=='Alt_R':
            self.key_alt_r = True
            
        if event.keysym=='Control_L':
            self.key_control_l = True
            
        if self.key_alt_r:
            pointer = self.view.text_area.index(tk.INSERT)
            symbol = ''
            if event.keysym=='2':
                symbol ='⚠️'
            elif event.keysym=='3':
                symbol ='‼'
            elif event.keysym=='5':
                symbol ='✶'
            elif event.keysym=='6':
                symbol ='●'
            elif event.keysym=='7':
                symbol ='░'
            elif event.keysym=='8':
                symbol ='▒'
            elif event.keysym=='9':
                symbol ='▓'
            elif event.keysym=='0'or event.keysym=='slash':
                symbol ='█'
            elif event.keysym=='p' or event.keysym=='P':
                symbol ='←'     
            elif event.keysym=='bracketleft' or event.keysym=='braceleft':
                symbol ='↑'      
            elif event.keysym=='bracketright' or event.keysym=='braceright':
                symbol ='→'      
            elif event.keysym=="apostrophe" or event.keysym=="at":
                symbol ='↓'      
            elif event.keysym=='t' or event.keysym=='T':
                symbol ='■'
            elif event.keysym=='y' or event.keysym=='Y':
                symbol ='▪'
                
            self.view.text_area.insert(pointer, symbol)
            
        elif self.key_control_l:
            if event.keysym=='r':
                self.take_text("nn")
            
            elif event.keysym=='b':
                self.take_text("fb")
                
            elif event.keysym=='j':
                self.take_text("fi")
                
            elif event.keysym=='h':
                self.take_text("hn")

                
            elif event.keysym=='w':
                self.take_text("wn")
                
            elif event.keysym=='l':
                self.take_text("ln")
                
                
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
                
            elif event.keysym=='plus' or event.keysym=='equal':
                self.zoom_in() 
                
            elif event.keysym=='minus':
                self.zoom_out()  
                
            elif event.keysym=='0':
                self.zoom_reset()     
                
            elif event.keysym=='f':
                self.search()   
                # self.open_search()      
                
            elif event.keysym=='m':
                self.switch_mode()
            
            
            elif event.keysym=='1':
                self.print_title(1)
                
            elif event.keysym=='2':
                self.print_title(2)
                
            elif event.keysym=='3':
                self.print_title(3)
                
            elif event.keysym=='4':
                self.print_title(4)
                
            elif event.keysym=='5':
                self.print_title(5)
                
            elif event.keysym=='6':
                self.print_title(6)
                
            elif event.keysym=='7':
                self.print_title(7)
                
            elif event.keysym=='8':
                self.print_title(8)
                            
        return "break"
    
    def key_released(self, event):
        if event.keysym=='Alt_R':
            self.key_alt_r = False
        if event.keysym=='Control_L':
            self.key_control_l = False
        # print(event.keysym)
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
            file = open(self.file,"r", encoding="utf-8") 
            self.view.text_area.insert(1.0,file.read()) 
            file.close()
            
            
    def open_recents(self, event=1): 
        # It show a list with the last 5 files opened
        # They are save in a file as a list[5]. 
        # IF this file in list ? move to first position : add to first postion, delete last.
        pass
            
    def save_file(self, event=1): 
        if self.file == None:   # Save as new file 
            self.save_as()        
        else:                   # Choose an existing file
            file = open(self.file,"w", encoding="utf-8") 
            file.write(self.view.text_area.get(1.0,tk.END)) 
            file.close() 
            
            
    def save_as(self, event=1):
        self.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", 
                                      filetypes=[("All Files","*.*"), ("Text Documents","*.txt")]) 
        if self.file == "": 
            self.file = None
        else:                   # Try to save the file 
            file = open(self.file,"w", encoding="utf-8") 
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
        
    def delete(self):
        if self.view.text_area.selection_get():
            
            line, column = map(int, self.view.text_area.index('sel.first').split('.'))
            position = (str(line) + "." + str(column))
            self.view.text_area.delete('sel.first','sel.last')
        
    
    # It's sent a data with the code style.
    def take_text(self, style:str="nn" ):
        if self.view.text_area.selection_get():
            
            # print("the style taken: ",style)
            self.select_text = self.view.text_area.selection_get()
            self.select_text = [*self.select_text]
  
            line, column = map(int, self.view.text_area.index('sel.first').split('.'))
            position = (str(line) + "." + str(column))
            self.view.text_area.delete('sel.first','sel.last')
            
            new_character_list = map(lambda x: self.model.apply_style(x, style), self.select_text)
            #print(list(new_character_list))    #! LEAVE TO CHECK ERROrs
            new_text = ''.join(new_character_list)
            # print(new_text)
            self.view.text_area.insert(position,new_text)       
    
    # Apply lines styles.
    def print_line(self, style:int=0):
        
        pointer = self.view.text_area.index(tk.INSERT)
        # print(style)
        line = ""
        if style == 1:
            line = "---------------------------------------------------------------------------------------------------------------"
        elif style == 2:
            line = "_______________________________________________________________________________________________________________"
        elif style == 3:
            line = "▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
        elif style == 4:
            line = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"
        elif style == 5:
            line = "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
        elif style == 6:
            line = "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓"
        elif style == 7:
            line = "███████████████████████████████████████████████████████████████████████████████████████████████████████████████"
        
        self.view.text_area.insert(pointer,line) 
        
    # Apply title styles.    
    def print_title(self, style:str=0):
        
        
        # CHECK IF HAVE A BREAK LINE, IF HAVE, APPLY 1 TIME EFFECT FOR EACH LINE
        # ADD THE EFFECTS IN OTHER FUNTION AT SIDE.
        # THINK ABOUT MAKE EXTERNAL ALL STYLES FUNTION.
        
        if self.view.text_area.selection_get():
        
           # print("the style taken: ",style)
            self.select_text = self.view.text_area.selection_get()
            self.select_text = [*self.select_text]
  
            line, column = map(int, self.view.text_area.index('sel.first').split('.'))
            position = (str(line) + "." + str(0))
            self.view.text_area.delete('sel.first','sel.last')
            
            if style == 1:
                #115 = ░░░ + '  ' + TEXTO + '  ' + ░░░
                
                long_text = len(self.select_text) + 4
                new_text = ''.join(self.select_text)
                new_text = new_text.title()
                fill_char = 111 - long_text
                fill_char = fill_char//2
                part1 = "░" * fill_char
                # print(fill_char)
                fill_char = 111 - (long_text + fill_char)
                part2 = "░" * fill_char
                # print(fill_char)
                new_text = f"""▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
{part1}  {new_text}  {part2}
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"""
                
                
            elif style == 2:
                new_character_list = map(lambda x: self.model.apply_style(x, "fb"), self.select_text)
                new_text = ''.join(new_character_list)
                new_text = new_text.title()
                new_text = '■ ' + new_text
            elif style == 3:
                new_character_list = map(lambda x: self.model.apply_style(x, "fd"), self.select_text)
                new_text = ''.join(new_character_list)
                new_text = new_text.capitalize()
                new_text = '	▪ ' + new_text
            elif style == 4:
                new_character_list = map(lambda x: self.model.apply_style(x, "fi"), self.select_text)
                new_text = ''.join(new_character_list)
                new_text = new_text.capitalize()
                new_text = '		· ' + new_text     
                
            elif style == 5:
                new_character_list = map(lambda x: self.model.apply_style(x, "sb"), self.select_text)
                new_text = ''.join(new_character_list)
                new_text = new_text.capitalize()
                new_text = '	● ' + new_text
            elif style == 6:
                new_character_list = map(lambda x: self.model.apply_style(x, "sd"), self.select_text)
                new_text = ''.join(new_character_list)
                new_text = new_text.capitalize()
                new_text = '		• ' + new_text
            elif style == 7:
                new_character_list = map(lambda x: self.model.apply_style(x, "si"), self.select_text)
                new_text = ''.join(new_character_list)
                new_text = new_text.capitalize()
                new_text = '			· ' + new_text        
            
            elif style == 8: #(Delete style)
                new_character_list = map(lambda x: self.model.apply_style(x, "nn"), self.select_text)
                new_text = ''.join(new_character_list)
                new_text = new_text.translate({ord(i): None for i in '■▪●•·▄▀░'})
                new_text = new_text.strip()
                new_text = new_text.lower()
    
            
            # print(new_text)
            
            
            self.view.text_area.insert(position,new_text)
            self.find_index()
        
        

            
        
    def print_time(self):       # 00:44 08/09/2022  date/time
        time = datetime.now()
        time = time.strftime("%H:%M %d/%m/%Y")
        pointer = self.view.text_area.index(tk.INSERT)
        self.view.text_area.insert(pointer,time)
        
    
    def search(self):
        # Check if use too memory by creating new instances.
        # Must be limited the number of window to one: If is open...
        self.enable_replace = tk.StringVar()
        self.input_search = tk.StringVar()
        self.input_replace = tk.StringVar()
        
        
        if isinstance(self.search_view, ExtraWindow):
            print("Ya existe")
            print(self.search_view)
            self.search_view.focus_search()
        #     search_input.focus_set()
        
        # if (self.instance_exists(self.search_view)):
        #     print("Ya existe")
        else:
            print("No existe")
            self.search_view = ExtraWindow(self, "Search")
            self.instances.append(self.search_view)
        
        # if instance.ExtraWindow == ExtraWindow for instance in instances:
        #     print("EXISTE")
        #     # If the search_frame already exists, bring it to the front
        #     self.search_view.lift()
        # else:
        #     print("No existe")
        #     self.search_view = ExtraWindow(self, "Search")
        
        
        
        
        
        
    
            
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
            self.view.text_area.configure(bg="#2A2F2D", fg="white")
            self.view.day_mode = "🌞"
            self.view.menu_bar.entryconfig(5, label = "🌞")  
                  
        else:
            self.view.text_area.configure(bg="white", fg="black")
            self.view.day_mode = "🌙"
            self.view.menu_bar.entryconfig(5, label="🌙")
            
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ INDEX ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    
    def go_select_title(self, index):
        
        idx = str(self.titles_dict[index] + 10.0)  # Add + 10 to center the focus.
        
        counter_list = []
        counter_list = str(idx).split('.')
        
        # add athe pointer entry before the new find word, and put focus on it.
        self.view.text_area.mark_set("insert", "%d.%d" % (float(int(counter_list[0])), 
                                                            float(int(counter_list[1]))))
        self.view.text_area.see(float(int(counter_list[0])))
        
        
 # Create a temp_dict. Charge all titles.
 # Check is is changes between temp_dict and self.titles_dict.
#       IF() → Update it.
 
 
    def find_index(self):
        temp_dict: dict = {}
        # for key in 
        idx = "1.0"
        
        print("Nuevo DICCIONARIOL:")
        while(idx):
            # Get position 1.0 only the first time.
            if temp_dict == {}:  # if list is empty, move one position in the list.
                temp_dict[self.view._open_file]= 1.0
            else:
                # Make sure the dict is sorted. Them, get the last position.
                #? Because a new dict is created, not need to sort it.
                # sorted_dict = {key: value for key, value in sorted(self.titles_dict.items(), key=lambda item: item[1])}
                # idx = str(list(sorted_dict.values())[-1])
                idx = str(list(temp_dict.values())[-1]) 
                idx = self.view.text_area.search(self.index_start, idx, nocase=1, stopindex=tk.END) # Search next.
                
                if idx:
                    next_line = float(idx) + 1  # Where the title is located
                    lastPosition = str(next_line).split('.',1)[0]
                    line_content = self.view.text_area.get(f"{next_line}", f"{lastPosition}.end")
                    line_content = line_content.split('  ',-1)[1]
                    
                    temp_dict[line_content]=next_line
                    
                    print(temp_dict)
                    
                    
                
                else:
                    break


        # Uptade self.titles_dict using the temp_dict
        self.titles_dict.update(temp_dict)
        self.titles_dict = {key: value for key, value in sorted(self.titles_dict.items(), key=lambda item: item[1])}
        # Clean deleted elements:
        
        for key in self.titles_dict.copy():
            if not key in temp_dict:
                del self.titles_dict[key]
 
        
        print("DICCIONARIOL Updated:")
        print(self.titles_dict)
        # def on_closing(self):
        # self.new_window.destroy()
        # self.controller.delete_instance(self)
        self.view.set_index()
            
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
   
       
        self.search_word = self.input_search.get()
        self.replace_word = self.input_replace.get()
        
        if self.search_word and self.replace_word and self.total_matches > 0:
           # self.select_tag()
        #! IF exist replace_word → Remplace word
            self.replace_text()
        
        if self.search_word:
 
            self.search_list.clear()
            self.search_list_idx.clear()
            self.view.text_area.tag_remove(tk.SEL, 1.0,"end-1c")
            self.total_matches = 0
            self.tag_position = 0
                

            
            self.total_matches = self.search_all()
            
            if self.total_matches > 0:
                self.select_tag()
            else:
                #! NEED TO AVOID CLOSE WINDOW
                MessageBox.showinfo("Search complete","No matches")
                # print("0 MATCHES")
        
        
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
        # It should save the document as temporal file each x minutes.
        pass
    
    
    
    def save_step(self, obj):
        # Must be called after press any arrow, enter, backspace or (click and write)
        # print("The cursor is at: ", entry.index(INSERT))
        pass
        
        
    # def instance_exists(self, name):
    #     return any(name for instance in self.instances)    
    
    def delete_instance(self, instance):
        #print("LA instancia recibida es de "+ instance)
        
        
        # if instance == "search_view":
        
        if isinstance(instance, ExtraWindow) and self.search_view:
            self.search_view = None
            gc.collect()
            
        # if self.index_tree:
        #     self.index_tree = None
        #     gc.collect()    
            
            
            
        # if (self.search_view):
        #     self.search_view = None
        #     gc.collect()
                
        # if instance == "index":
        #     pass
        
        
        
        
        
        
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
               