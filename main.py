from Main.viewmodel import ViewModel
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)


# Start the app.
def start_notepad():
    notepad = ViewModel()   #(width=1050,height=600)
    notepad.run()


if __name__ == '__main__':
	start_notepad()