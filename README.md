
# NOTEPAD python APP.

## Description:

Notepad with different functions, which allows writing a text, and applying different styles effects as can bold or italic fonts, keeping the same format and compatibility with other notepads.


## Use:

Requires to use:
- Python 3.10 or latest.

Use the modules and libraries:
- 0s
- Tkinder
- Datetime
- ctypes


## Functions:

- [x] Write text.
- [x] Save documents as **.txt**.
- [x] Open and edit documents.
- [x] Zoom option.
- [x] Copy, Cut, Paste and Select All functions.
- [x] Night mode.
- [x] Apply different text styles .txt.
- [ ] Search option.
- [ ] Replace option.
- [ ] Minimap.
- [ ] Index option.
- [ ] Special titles.
- [ ] Undo/Redo options.



## Design history:

### Initial stage:


The development was builded initially in one class, without choosing a architectural pattern:

**NotePad_Old.py** file.

```
Design steps:

	By functions:

		First declared the functions.
		Later create the root and tk elements.
		call the functions from actions.

	
	By God class:

		Initical main class "Notepad".
			▪ Initiate Tk main elements: Text area, Menu and Scrollbar
			▪ General variables.
			▪ The constructor:
				▪ Get Width and Heigh if is.
				▪ Adds the different menu options.
				▪ Shortcut
				▪ Define positions and frame size.
				▪ Define placement for textArea and Scrollbar.
				▪ Configurations about (grid placement).

			▪ Function: set_title			→ set title screen. 
			▪ Function: new_file 			→ Create new file by cleaning text_area and file.
			▪ Function: open_file			→ Open a new file: what ask for open and try to open.
			▪ Function: save_file			→ Create a new file and save there the text area info.
			▪ Function: save_as				→ Save always asking for a new name.
			▪ Function: close_app			→ kill the execution.

			▪ Function: cut					→ generate cut event.
			▪ Function: copy				→ generate copy event.
			▪ Function: paste				→ generate paste event.
			▪ Function: bold_serif			→ define select style as fb
			▪ Function: italic_serif		→ define select style as fi
			▪ Function: bold_italic_serif	→ define select style as fd
			▪ Function: none_style			→ define select style as nn
			▪ Function: take_text			→ get selecction and call apply style by chart.
			▪ Function: apply_style			→ Change the character for the new one.

			▪ Function: select_all			→ Select all text in text_area.
			▪ Function: zoom_in				→ Increase zoom by icreasing font size.
			▪ Function: zoom_out			→ Decrease zoom by decreasing font size
			▪ Function: zoom_reset			→ Set default font size.
			▪ Function: shot_about			→ Alert with message about NotePad.
			▪ Function: switch_mode			→ Invert the colors to nigth mode.
			▪ Function: run					→ Execute the GUI app.

	By VC (View and Controller)  From MVC

		Heritage Tk class, allows don't need to use root element.

```
### Final stage:

When the app code started to grow up more and more, keep all code started to be more complicated to add more functions, test parts, etc... Then, It was tried to apply a MVC (Model Vista Controller). Due to the requirement to work constantly in the View, this pattern was not enough effective and would require a lot of duplicate lines.

After analysing different patterns, the best model to follow was (MVVM) Model-View-ViewModel, which allow to apply many changes directly in the View without need to use constantly an intermediary, and allows separating logic from the view.

Additionally, the code was improved to make it easier to read, and optimize different parts, specially *apply_style* method, which now don not require be edited after add new font styles.


## Structure:

```
     ┏━━━━━━━━┓   ←    ┏━━━━━━━━━━━┓   ← →   ┏━━━━━━━━┓
     ┃ Model  ┣━━━━━━━━┫ ViewModel ┣━━━━━━━━━┫  View  ┃
     ┗━━━━━━━━┛        ┗━━━━━━━━━━━┛         ┗━━━━━━━━┛
	 ↓		    ⇫
     ┌───────┐	      ╔═══════════╗
     │ fonts │        ║    Main   ║
     └───────┘        ╚═══════════╝      


Main
└──────┤ start_notepad()		*(Run the app executing run() )*


ViewModel
└───────────┤ run()			*(Call view.run())*
	    │ new_file()		*(Clean text_area)*
	    │ open_file()		*(Open a existend file)*
	    │ save_file()		*(Save a file in the system)*
	    │ save_as()			*(Save a file which determinate name)*
	    │ close_app()		*(Stop the app breaking mainloop)*
	    │ cut()			*(Call cut system action)*
	    │ copy()			*(Call copy system action)*
	    │ paste()			*(Call paste system action)*
	    │ select_all()		*(Select all string in text_area)*
	    │ print_time()		*(Print de current date and time)*
	    │ zoom_in()			*(Increase font size)*
	    │ zoom_out()		*(Decrease font size)*
	    │ zomm_reset()		*(Set default font size "9")*
	    │ switch_mode()		*(Switch between default and night mode)*		

View
└───────────┤ run()			*(call mainloop to start window app)*
	    │ make_frame()		*(Create the main framee or root)*
	    │ set_text_area()		*(Create a text widget called text_area)*
	    │ set_title()		*(Set the title name of the window)*
	    │ set_size()		*(Set the window size)*
	    │ set_font()		*(Set the font size)*
	    │ set_zoom()		*(Set the zoom quantity applied on the menu)*
	    │ set_menu()		*(Create the widget menu)*
	    │ set_file_menu()		*(Create and Add file_menu to widget menu)*
	    │ set_edit_menu()		*(Create and Add edit_menu to widget menu)*
	    │ set_view_menu()		*(Create and Add view_menu to widget menu)*
	    │ set_help_menu()		*(Create and Add help_menu to widget menu)*
	    │ show_about()		*(Show an informative window about)*
	    │ set_night_option()	*(Create and Add day_mode to widget menu)*

Model
└───────────┤ apply_style()		*(Change the character to the style desired)
              └─────────────┤font	*(Dictionary with the different fonts styles)*
```

## Files:

### main.py

Main file, start the app.

windll.shcore.SetProcessDpiAwareness(1): 	Define the dpi resolution.

start_notepad(function): Initiate ViewModel and run app calling the view/viewmodel.run()


### viewmodel.py

Handles all the logic from the view, and takes control over View and Model.

- Initiate `file` with none.
- Initiate `selected_text` with an empty string.

**Constructor:**
- Initiate Model().
- Initiate View(self), and send a reference of viewmodel.
- Shorcuts with bind to the menu options:
  - Control + N: Execute **new_file()**
  - Control + O: Execute **open_file()**
  - Control + S: Execute **save_file()**
  - Control + Shitf + S: Execute **save_as()**
  - Control + M: Execute **switch_mode()**
  - Control + "+": Execute **zoom_in()**
  - Control + "-": Execute **zoom_out()**
  - Control + 0: Execute **zoom_reset()**

**run(self):** Call the method `run()` from View. → Execute run the window.

*Many of the next functions, use a event=1 parameter to avoid the parameter sent by bind function.

**def new_file(self, event=1):** Reset the title, the file var and clean the text_area.

**def open_file(self, event=1):** ask to open a file. If open, set file name as title. Put file info inside of the text_area.

**def save_file(self, event=1):** If exist with the same title as name file, save the file over the file exiting. If not, call `save_as` method.

**def save_as(self, event=1):** Ask for name to save the file and put the new name as title.

**def close_app(self):** Call the method `destroy()` from View. → Close the window.

**def cut(self):** Call Cut system event to take a the selected text out of the text_area.

**def copy(self):**  Call Copy system event to copy a the selected text of the text_area.

**def paste(self):**  Call Paste system event to put a text copied before in the text_area.

**def select_all(self, event=1):**  Select all text inside of the text_area.

**def take_text(self, style:str="nn" ):** Check if is any selected. In that case, save the selected text and the position. Delete the select text. Use map to call `apply_style` from model, character by character and save the result. Make a new string with all these characters returned from `apply_style` and put it in the same position where was the selection. *Style is set as "nn" by default here and in `apply_style` to avoid possible errors.

**def print_time(self):** Take the current time and print it where is the pointer in "%H:%M %d/%m/%Y" format.

**def zoom_in(self, event=1):** Check if the text size is less than the limit and add 1 to n_font in View. Call `set_font` and `set_zoom` methods from View with the new value.

**def zoom_out(self, event=1):** Check if the text size is more than 0 and rest 1 of n_font in the View. Call `set_font` and `set_zoom` methods from View with the new value.

**def zoom_reset(self, event=1):** Reset by the default value. Call `set_font` and `set_zoom` methods from View with the default value.

**def switch_mode(self, event=1):** Check if is on day mode and apply night mode, or apply day mode. 
- Day mode (default): apply a white background, black color text and "🌙" icon in the menu_bar.
- Night  mode: apply a black background, white text and "🌞" icon in the menu_bar.


### view.py

Handles the window render with tkinder.

- Initiate `title` as " - Notepad". Don't  need to change.
- Initiate `default_width` to 1050.
- Initiate `default_height` to 600.
- Initiate `day_mode` as "🌙".
- Initiate `zoom` to 1,6.
- Initiate `default_size` to 9.
- Initiate `n_font` equal to `default_size`.
- Initiate `font_list` as a tupla of numbers. Don't  need to change.
- Initiate `zoom_list` as a tupla of strings. Don't  need to change.

**Constructor:**
- Inherits from the superior class (tk.TK).
- Initate the ViewModel instance as controller.
- Initiate the next methods: `make_frame()`, `set_title()`, `set_menu()`, `set_file_menu()`, `set_edit_menu()`, `set_view_menu()`, `set_help_menu()`, `set_night_option()`, `set_text_area()`, `set_size()`, and `set_font()`.


**def run(self):** Start the app calling the mainlopp() tk method.

**def _make_frame(self):** Create the main frame or root as frame.

**def set_text_area(self):** Create the main widget: Text as text_area. Configured it to cover all frame and keeps sticky to the frame borders. Add a scrollbar widget to text_area, which keep on the right side and has an adaptative size.

**def set_title(self, name:str="Untitled"):** Set the window title using the parameter name and the title variable.

**def set_size(self):** Set the window size.

**def set_font(self, size:int=9):** Set the font family, the style and the size.

**def set_zoom(self, size:int=9):** Set the number of zoom showed in the view_menu.

**def _set_menu(self):** Set the main menu as menu_bar.

**def set_file_menu(self):** Set the file_menu with these options on menu_bar:
- Label: *New*, shorcut: *Ctrl+N*, Command: **new_file()**
- Label: *Open*, shorcut: *Ctrl+O*, Command: **open_file()**
- Label: *Save*, shorcut: *Ctrl+S*, Command: **save_file()**
- Label: *Save as…*, shorcut: *Ctrl+Shif+ S*, Command: **save_as()**
- Label: *Exit*, shorcut: *Ctrl+.*, Command: **close_app()**

**def set_edit_menu(self):** Set edit_menu and submenu style_menu with these options on menu_bar:
- Label: *Cut*, shorcut: *Ctrl+X*, Command: **new_file()**
- Label: *Copy*, shorcut: *Ctrl+C*, Command: **new_file()**
- Label: *Paste*, shorcut: *Ctrl+P*, Command: **new_file()**
- Label: *Select All*, shorcut: *Ctrl+A*, Command: **new_file()**
- Label: *Style*
  - Label: *Bold*, Command: **take_text("fb")**
  - Label: *Italic*, Command: **take_text("fi")**
  - Label: *Italic Bold*, Command: **take_text("fd")**
  - Label: *Remove style*, Command: **take_text("nn")**
- Label: *Date/Time*, Command: **print_time()**

**def set_view_menu(self):** Set view_menu with these options on menu_bar:
- Label: *Zoom In*, shorcut: *Ctrl+Plus*, Command: **zoom_in()**
- Label: *Zoom Out*, shorcut: *Ctrl+minus*, Command: **zoom_out()**
- Label: *Restore Zoom*, shorcut: *Ctrl+0*, Command: **zoom_reset()**

**def set_help_menu(self):** Set help_menu with this option on menu_bar:
Label: *About NotePad*, Command: **show_about()**

**def set_night_option(self):** Add this option on menu_bar:
Label: `day_mode`, shorcut: *Ctrl+M*, Command: **switch_mode()**

**def show_about(self):** Show an informative window with a title and message.


### model.py

Handle the logic side not relationate with the view.

**def apply_style(self,chart:str ,style:str="nn"):** Find the position character and apply the corresponding character for the desired style. If not find the character, keep the same character. Receive a string of 1 character and another string with the style code. Must return another string with an only character.

### fonts.py

Dictionary with all different fonts styles saved character by character in a tupla.


## Data Tables:

Font style code used:
```
	      ┏━━━━━━━┳━━━━━━━┓
 Font types:  ┃ Type  ┃ Style ┃	
┌┈┈┈┈┈┈┈┈┈┈┈┈┈┠───────╂───────┨┈┈┈┈┈┈┈┈┈┈┈┈┈┐
┊ Normal      ┃   n   ┃   n   ┃ Normal      ┊	type + style = font style
┊	      ┃       ┃       ┃             ┊
┊ Serif       ┃   f   ┃   i   ┃ Italic      ┊	Examples:
┊	      ┃       ┃       ┃             ┊		Sans Italic style:      si		
┊ Sans	      ┃   s   ┃   b   ┃ Bold        ┊		Sans bold style: 	sb
┊	      ┃       ┃       ┃             ┊		Gothic Bold style: 	gb
┊ Script      ┃   t   ┃   d   ┃ Italic/Bold ┊		Default font style:     nn
┊	      ┃       ┃       ┃             ┊
┊ Gothic      ┃   g   ┃   k   ┃Strikethrough┊
┊	      ┃       ┃       ┃             ┊
┊ TypeWriter  ┃   w   ┃   u   ┃ Underline   ┊
┊	      ┃       ┃       ┃             ┊
┊ Small	      ┃   m   ┃       ┃             ┊
┊	      ┃       ┃       ┃             ┊
┊ Long	      ┃   l   ┃       ┃             ┊
┊	      ┃       ┃       ┃             ┊
┊ Futuristic  ┃   a   ┃       ┃             ┊
┊	      ┃       ┃       ┃             ┊
┊ highlighted ┃   h   ┃       ┃             ┊
┊	      ┃       ┃       ┃             ┊
┊	      ┃       ┃       ┃             ┊
└┈┈┈┈┈┈┈┈┈┈┈┈┈┗━━━━━━━┻━━━━━━━┛┈┈┈┈┈┈┈┈┈┈┈┈┈┘

```

Zoom and font size numbers and relation:
```
	    ┏━━━━━━━┳━━━━━━━┓
 Zoom List: ┃   %   ┃  Size ┃
┌┈┈┈┈┈┈┈┈┈┈┈┠───────╂───────┨
┊     0	    ┃  10   ┃   1   ┃
┊     1	    ┃  20   ┃   2   ┃
┊     2	    ┃  30   ┃   3   ┃
┊     3	    ┃  40   ┃   4   ┃
┊     4	    ┃  50   ┃   5   ┃
┊     5	    ┃  60   ┃   6   ┃
┊     6	    ┃  70   ┃   7   ┃
┊     7	    ┃  80   ┃   8   ┃
┊     8	    ┃  90   ┃   9   ┃
┊     9	    ┃ 100   ┃  11   ┃
┊    10     ┃ 110   ┃  12   ┃
┊    11	    ┃ 120   ┃  13   ┃
┊    12	    ┃ 130   ┃  14   ┃
┊    13	    ┃ 140   ┃  15   ┃
┊    14	    ┃ 150   ┃  16   ┃
┊    15	    ┃ 160   ┃  18   ┃
┊    16	    ┃ 170   ┃  19   ┃
┊    17	    ┃ 180   ┃  20   ┃
┊    18	    ┃ 190   ┃  21   ┃
┊    19	    ┃ 200   ┃  22   ┃
┊    20	    ┃ 220   ┃  24   ┃
┊    21	    ┃ 240   ┃  26   ┃
┊    22	    ┃ 260   ┃  28   ┃
┊    23	    ┃ 280   ┃  30   ┃
┊    24	    ┃ 300   ┃  33   ┃
┊    25	    ┃ 320   ┃  36   ┃
┊    26	    ┃ 350   ┃  39   ┃
┊    27	    ┃ 400   ┃  43   ┃
┊    28	    ┃ 440   ┃  48   ┃
┊    29	    ┃ 500   ┃  54   ┃
┊    30	    ┃ 550   ┃  60   ┃
┊    31	    ┃ 600   ┃  72   ┃
┊    32	    ┃ 800   ┃  84   ┃
┊           ┃       ┃       ┃
└┈┈┈┈┈┈┈┈┈┈┈┗━━━━━━━┻━━━━━━━┛
```

Options to change the `print_date()` format to so show the time and date.
```
strftime:
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ # dd/mm/YY		 ┃  16/09/2019	          ┃  today.strftime("%d/%m/%Y")           ┃
┃                        ┃                        ┃                                       ┃
┃ # month, day and year	 ┃  September 16, 2019    ┃  today.strftime("%B %d, %Y")          ┃
┃                        ┃                        ┃                                       ┃
┃ # mm/dd/y		 ┃  09/16/19	  	  ┃  today.strftime("%m/%d/%y")           ┃
┃                        ┃                        ┃                                       ┃
┃ # Mth, day and year	 ┃  Sep-16-2019	          ┃  today.strftime("%b-%d-%Y")           ┃
┃                        ┃                        ┃                                       ┃
┃ # dd/mm/YY H:M:S	 ┃  25/06/2021 07:58:56   ┃  today.strftime("%d/%m/%Y %H:%M:%S")  ┃
┃                        ┃                        ┃                                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

