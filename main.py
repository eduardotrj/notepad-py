from Main.ViewModel.viewModel import ViewModel
from ctypes import windll


# TODO → Make sharp the image.
windll.shcore.SetProcessDpiAwareness(1)


# Start the app.
def start_notepad():
    notepad = ViewModel()   # (width=1050,height=600)
    notepad.run()


if __name__ == '__main__':
    start_notepad()

# Add menu by tittles