
from tkinter.messagebox import *
from tkinter.filedialog import *
from Main.fonts import fonts


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
        for font in fonts.values():
            if chart in font:
                new_chart = font.index(chart)
                
        if new_chart:
            new_chart = fonts[style][new_chart]
            
        else:
            new_chart = chart
        return new_chart
        
        

        
        
        
        