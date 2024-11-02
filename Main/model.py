
from tkinter.messagebox import *
from tkinter.filedialog import *
from Main.fonts import FONTS


class Model:
    
    
    # def __init__(self):
    #     self.algo = "nothing"
           
           
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ STYLE APPLY ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ 
        
# Gets self(obj), the chart(str), and style(str).
# Initiate New_chart as empty string.
# go over each element in fonts(dic), and try to find the character position.
# If have the position, apply the style character at the same position.
# If not, leave the chart with the same value.
    def apply_style(self,chart:str ,style:str="nn") -> str:
        new_chart = ""
        print(chart)
        for font in FONTS.values():
            if chart in font:
                new_chart = font.index(chart)
    
        if new_chart:
            new_chart = FONTS[style][new_chart]
        
        elif str(new_chart) == '0': # To avoid treat 0 as false, or null.
            new_chart = FONTS[style][0]
        
        else:
            new_chart = chart
        

        return new_chart
        
        
    # def save_conf():
    # pass
        

        
        