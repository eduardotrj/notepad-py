import tkinter as tk
from Main.View.extraView import ExtraWindow
from tkinter import messagebox as MessageBox






class SearchMenu(tk.Tk):


    select_text = ""
    search_word: str = ""
    replace_word: str = ""
    search_list = list()
    search_list_idx = list()
    total_matches: int = 0
    tag_position: int = 0


def __init__(self, controller):
    super().__init__()

    self.controller = controller

    self.search()


# check if is another instance of the object extraview .instance()


    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ SEARCH FUNCTION ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■


        # To add advance search →
        # 1º funct: search all items and add it to and array, position value?
        # Add quantities to a total_value.
        # return the array and the total_value
        # 2º funct: allos move between array values with buttons next or back.
        # thierd?? replace the array position element for another and remove it.


    def search(self):
        # Check if use too memory by creating new instances.
        # Must be limited the number of window to one: If is open...
        self.enable_replace = tk.StringVar()
        self.input_search = tk.StringVar()
        self.input_replace = tk.StringVar()
        self.search_view = ExtraWindow(self.controller, "Search")



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