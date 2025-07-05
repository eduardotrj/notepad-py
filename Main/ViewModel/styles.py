
# Apply lines styles.
def print_line(self, style:int=0):

    pointer = self.view.text_area.index(tk.INSERT)
    print(style)
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

    self.view.text_area.insert(pointer, line)

# Apply title styles.
def print_title(self, style: str=0):
    # CHECK IF HAVE A BREAK LINE, IF HAVE, APPLY 1 TIME EFFECT FOR EACH LINE
    # ADD THE EFFECTS IN OTHER FUNTION AT SIDE.
    # THINK ABOUT MAKE EXTERNAL ALL STYLES FUNTION.
    if self.view.text_area.selection_get():

        print("the style taken: ", style)
        self.select_text = self.view.text_area.selection_get()
        self.select_text = [*self.select_text]

        line, column = map(int, self.view.text_area.index('sel.first').split('.'))
        position = (str(line) + "." + str(0))
        self.view.text_area.delete('sel.first', 'sel.last')

        if style == 1:
            # 115 = ░░░ + '  ' + TEXTO + '  ' + ░░░

            long_text = len(self.select_text) + 4
            new_text = ''.join(self.select_text)
            fill_char = 111 - long_text
            fill_char = fill_char//2
            part1 = "░" * fill_char
            print(fill_char)
            fill_char = 111 - (long_text + fill_char)
            part2 = "░" * fill_char
            print(fill_char)
            new_text = f"""▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
{part1}  {new_text}  {part2}
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"""

        elif style == 2:
            new_character_list = map(lambda x: self.model.apply_style(x, "fb"), self.select_text)
            new_text = ''.join(new_character_list)
            new_text = '■ ' + new_text
        elif style == 3:
            new_character_list = map(lambda x: self.model.apply_style(x, "fd"), self.select_text)
            new_text = ''.join(new_character_list)
            new_text = '	▪ ' + new_text
        elif style == 4:
            new_character_list = map(lambda x: self.model.apply_style(x, "fi"), self.select_text)
            new_text = ''.join(new_character_list)
            new_text = '		· ' + new_text

        elif style == 5:
            new_character_list = map(lambda x: self.model.apply_style(x, "sb"), self.select_text)
            new_text = ''.join(new_character_list)
            new_text = '	● ' + new_text
        elif style == 6:
            new_character_list = map(lambda x: self.model.apply_style(x, "sd"), self.select_text)
            new_text = ''.join(new_character_list)
            new_text = '		• ' + new_text
        elif style == 7:
            new_character_list = map(lambda x: self.model.apply_style(x, "si"), self.select_text)
            new_text = ''.join(new_character_list)
            new_text = '			· ' + new_text

        print(new_text)

        self.view.text_area.insert(position, new_text)
