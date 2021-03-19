import os
from datetime import datetime
from tkinter import *
from tkinter.font import Font
import speech_recognition as sr

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
errorLabel1 = Label() # necessary to display errors on multiple lines
errorLabel2 = Label() # necessary to display errors on multiple lines

# TITLE: SPEECH_RECOGNITION

microphone, recognizer = sr.Microphone(), sr.Recognizer()
recognizer.pause_threshold = 0.5  # minimum length of silence after speaking
recognizer.energy_threshold = 100  # set energy threshold
recognizer.dynamic_energy_threshold = False  # do not update ambient noise threshold

# TITLE: MENTAL ARITHMETIC
ma_setup_frame = None
mental_arithmetic_frame = None
checks = None
timer = None
# exit_button = Button()

