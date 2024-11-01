import cmath


class Calculation:
    
    
    times_character: int = 0
    first_position: int = 0
    last_position: int = 0
    result: str = ""
    
    
    def calculate(self, chart: str) -> str:
        
        # chart_list = [*chart]
        # split_text = text.split(',')
        
        self.times_character = chart.count("(")


        while(self.times_character):
            self.__do_brackets(chart)
            
        
            
            # Control symbol. 
                # if (**)  → do_exponents
                # if(/ *)  → mult
                # if(+ -)  → add
        
        #self.find_brackets(chart)
        
        #times_character = chart.count("+")
        # self.result = self.__do_add(chart)
        
        
        # print(self.result)
        
        
        
    
    def __do_brackets(self, number):
            
            # first_position = times_character.find("(")
            # last_position = times_character.find (")")
            
        self.times_character-=1
        
        print(self.times_character)
        
    
    def __do_exponents(self, number):
        pass
    
    def __do_porcent(self,number):
        pass
    
    def __do_mult(self, number):
        pass
    
    def __do_add(self, number):
        pass
    
    # First: ( )
    # second: * / 
    # after: + -
    
   # 45 + (4-6)    45 +      ...     4-6)
    
    
    
    # 6 + 8 -5 = 9
    
    # 5 * 5 -10 = 15
    
    # 2**2**3  = 2^(2^(3))  = 256
    
    # 5^(3)+10/(10-5) = 127
    
    # 81^(1/4)*3 = 9
    
    # log(105) = 2,021189…
    
    # 42%10 = 4,2            //     30%5  = 1,5
    
    
    
    
    
    
    # Check if is brackers inside the brackuers.
    # Check if is ^ or Log before brackers → do_exponents.
    
    
   # Logica:
        
    #    comprobar si hay brackers SI? → No Continue
        
    