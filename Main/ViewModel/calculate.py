# import cmath
# from Main.fonts import OPERATORS as OP
# from Main.extraView import MessageWindow

# # from sitecustomize import timeit_decorator


# # Process:

# #   1. Check if the ecuation is correct:    Have pair number brackers, have only allowed letters, etc...
# #   2. Analize each part by ended brackets to define sections.
# #   3. Calculate in base priorities.




# class Calculation:

#     def __init__(self):


#         #self.SYMBOLS: tuple = ('(', ')','^', 'x','*',':', '/', '+', '-')
#         self.SYMBOLS: tuple = ('*','/','+','-')
#         self.previous_value = ''
#         self.value = ''
#         self.operator = ''



#     # times_character: int = 0
#     # first_position: int = 0
#     # last_position: int = 0
#     # result: str = ""
#     # Tuple ordened by priority to read it.

#         # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ VALIDATION ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

#     def _validate_operation(self,operation: str) -> bool:

#         """ Validate if the operation is well writed or is possible to result it.

#         Args:
#         operation (str): The input string to check.

#         Returns:
#             bool: True when meets all requirements.
#         """

#         return self._correct_characters(operation) and self._brackers_balanced(operation)



#     def _correct_characters(self, s: str) -> bool:

#         """
#             Check if a string contains only characters or strings inside the dictionary values.

#         Args:
#             s (str): The input string to check.
#             operators (dict): A dictionary containing lists or tuples of valid operators.

#         Returns:
#             bool: True if the string contains only valid characters or strings, otherwise False.
#         """

#          # Flatten the dictionary values into a set of strings
#         valid_values = set(
#             str(item)  # Convert to string since dictionary contains both int and str
#             for values in OP.values()
#             for item in values
#         )

#         # Split the input string into potential tokens (words, symbols, etc.)
#         tokens = s.split()  # Split by spaces (or use a tokenizer for more complex strings)

#         # Check if all tokens are in the set of valid values
#         return all(token in valid_values for token in tokens)




#     def _brackers_balanced(self, s: str) -> bool:

#         """ Validate if the operation is well writed or is possible to result it.

#         Args:
#         s (str): The input string to check.

#         Returns:
#             bool: True if the counts match, otherwise False.
#         """

#         return s.count("(") == s.count(")") and s.count("[") == s.count("]") and s.count("{") == s.count("}")



#         # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ CALCULATION ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■



#     @timeit_decorator
#     def calculate(self, math_op: str = "") -> str:

#         a: float = 0
#         b: float = 0
#         numbers = list()
#         SYMBOLS: tuple = ('*','/','+','-')

#         # record = str(record).split('@',1)[1]      → Split by chart and get element [1]
#         # record = record.replace(' ', '')
#         # list		→ […,…,…]
#         # float(string) // str(float)
#         # isDigit()  len()   count()   find() rfind() startwith()  endwith()   index() rindex()   strip()


#         print(math_op)
#         operation: str = math_op.replace(' ', '')


#         # result = self._analyze_operation(operation)

#         if operation.find(SYMBOLS[2]) != -1:
#             numbers = operation.split(SYMBOLS[2],-1)
#             result = self._do_add(
#                 float(numbers[0]),
#                 float(numbers[1])
#                 )

#         elif operation.find(SYMBOLS[3]) != -1:
#             numbers = operation.split(SYMBOLS[3],-1)
#             result = self._do_sub(
#                 float(numbers[0]),
#                 float(numbers[1])
#                 )

#         elif operation.find(SYMBOLS[0]) != -1:
#             numbers = operation.split(SYMBOLS[0],-1)
#             result = self._do_mult(
#                 float(numbers[0]),
#                 float(numbers[1])
#                 )

#         elif operation.find(SYMBOLS[1]) != -1:
#             numbers = operation.split(SYMBOLS[1],-1)
#             result = self._do_div(
#                 float(numbers[0]),
#                 float(numbers[1])
#                 )


#         # print(str(result))

#         return str(result)

#     def _analyze_operation(self, operation):


#         for i in range (3):
#             if (operation.find(OP["BRACK_O"][i]) != -1) and (operation.find(OP["BRACK_C"][i]) != -1):

#                 start = operation.index(OP["BRACK_O"][i])
#                 numbers = operation.split(self.SYMBOLS[2],-1)

#                 end = operation.index(OP["BRACK_C"][i])



#             elif (operation.find(OP["BRACK_O"][i]) != -1) != (operation.find(OP["BRACK_C"][i]) != -1):

#                 print("1 not pair" )

#             else:
#                 print("Not Brackets")



#             # if (operation.find(symbol) != -1) and (operation.find(symbol) != -1):    # → it have it

#             #     type_bracket = OP["BRACK_O"].index(symbol)
#             #     closed_bracket = OP["BRACK_C"][type_bracket]
#             #     start = operation.index(symbol)
#             #     end = operation


#                # numbers = operation.split(SYMBOLS[0],-1)



#         # if operation.find():
#         #     pass
#         # pass
#         return "hhello"



#     def _do_add(self, a, b):
#         return a + b

#     def _do_sub(self, a, b):
#         return a - b

#     def _do_mult(self, a, b):
#         return a * b

#     def _do_div(self, a, b):
#         try:
#             return a / b
#         except:
#             MessageWindow.show_message("Division by 0", "error")
#             return '∞'




#         # chart_list = [*chart]
#         # split_text = text.split(',')

#         # self.times_character = chart.count("(")


#         # while(self.times_character):
#         #     self.__do_brackets(chart)



#             # Control symbol.
#                 # if (**)  → do_exponents
#                 # if(/ *)  → mult
#                 # if(+ -)  → add

#         #self.find_brackets(chart)

#         #times_character = chart.count("+")
#         # self.result = self.__do_add(chart)


#         # print(self.result)

#     # ■■■■■■■■■■■■■■■■■■■■■■■■■■■ PRIORITIES ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■


#     def __do_brackets(self, number):

#             # first_position = times_character.find("(")
#             # last_position = times_character.find (")")

#         self.times_character-=1

#         print(self.times_character)


#     def __do_exponents(self, number):
#         pass

#     def __do_porcent(self,number):
#         pass

#     def __do_mult(self, number):
#         pass




#     # First: ( )
#     # second: * /
#     # after: + -

#    # 45 + (4-6)    45 +      ...     4-6)



#     # 6 + 8 -5 = 9

#     # 5 * 5 -10 = 15

#     # 2**2**3  = 2^(2^(3))  = 256

#     # 5^(3)+10/(10-5) = 127

#     # 81^(1/4)*3 = 9

#     # log(105) = 2,021189…

#     # 42%10 = 4,2            //     30%5  = 1,5






#     # Check if is brackers inside the brackuers.
#     # Check if is ^ or Log before brackers → do_exponents.


#    # Logica:

#     #    comprobar si hay brackers SI? → No Continue


