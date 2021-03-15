import os
from datetime import datetime
from tkinter import *
from tkinter.font import Font

# TITLE: INITIALIZE ROOT
root = Tk()

# TITLE: DEFAULT TKINTER FONTS
HeadingFont = Font(
    family='Helvetica',
    size=20,
    weight='bold'
)
DefaultFont = Font(
    family='Helvetica',
    size=20,
    weight='normal'
)

# TITLE: MAIN
MainFrame = Frame(root)

identifier = 'Unknown'
save_folder = ''
errorLabel1 = Label()
errorLabel2 = Label()

microphone = None

# TITLE: MENTAL ARITHMETIC
ma_setup_frame = None
mental_arithmetic_frame = None
checks = None
timer = None
# exit_button = Button()

