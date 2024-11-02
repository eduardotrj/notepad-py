import cmath
# from Main.fonts import fonts

class Calculation:
    
    def __init__(self):

       
        #self.SYMBOLS: tuple = ('(', ')','^', 'x','*',':', '/', '+', '-')
        self.SYMBOLS: tuple = ('*','/','+','-')
        self.previous_value = ''
        self.value = ''
        self.operator = ''
        
      
    
    # times_character: int = 0
    # first_position: int = 0
    # last_position: int = 0
    # result: str = ""
    # Tuple ordened by priority to read it.
    
    
    def calculate(self, math_op: str = "") -> str:
        
        a: float = 0
        b: float = 0
        numbers = list()
        SYMBOLS: tuple = ('*','/','+','-')
        
        # record = str(record).split('@',1)[1]      → Split by chart and get element [1]
        # record = record.replace(' ', '')
        # list		→ […,…,…]
        # float(string) // str(float)
        # isDigit()  len()   count()   find() rfind() startwith()  endwith()   index() rindex()   strip()
        
        
        
        print(math_op)
        operation: str = math_op.replace(' ', '')
        
        # if  len(operation) < 1:
        #     return "Error"
        
        if operation.find(SYMBOLS[2]) != -1:
            numbers = operation.split(SYMBOLS[2],-1)
            a = float(numbers[0])
            b = float(numbers[1])        
        
        result = self._do_add(a,b)

        print(str(result))
        
        return str(result)
        
        
        
    def _do_add(self, a, b):
        return a + b

        
        
        # chart_list = [*chart]
        # split_text = text.split(',')
        
        # self.times_character = chart.count("(")


        # while(self.times_character):
        #     self.__do_brackets(chart)
            
        
            
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
        
    
   