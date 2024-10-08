import os
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import speech_recognition as sr
import time

# TITLE: INITIALIZE ROOT
root = Tk()

# TITLE: DEFAULT TKINTER FONTS
HeadingFont = Font(
    family='Helvetica',
    size=30,
    weight='bold'
)
DefaultFont = Font(
    family='Helvetica',
    size=30,
    weight='normal'
)
SmallFont = Font(
    family='Helvetica',
    size=20,
    weight='normal'
)
GiantFont = Font(
    family='Helvetica',
    size=40,
    weight='bold'
)

# TITLE: MAIN
MainFrame = Frame(root)

identifier = 'Unknown'
save_folder = ''
errorLabel1 = Label() # necessary to display errors on multiple lines
errorLabel2 = Label() # necessary to display errors on multiple lines
timer = None
global_start_time = time.time()

# TITLE: SPEECH_RECOGNITION
microphone, recognizer = sr.Microphone(), sr.Recognizer()
recognizer.pause_threshold = 0.5  # minimum length of silence after speaking
recognizer.energy_threshold = 200  # set energy threshold
recognizer.dynamic_energy_threshold = False  # do not update ambient noise threshold
pronounce_defaults = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', 'orange': 'orange', 'yellow': 'yellow', 'blue': 'blue', 'green': 'green'}
pronounce = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', 'orange': 'orange', 'yellow': 'yellow', 'blue': 'blue', 'green': 'green'}
skip_keyword = "skip"


# TITLE: MENTAL ARITHMETIC
ma_setup_frame, mental_arithmetic_frame = None, None
ma_checks = None

# TITLE: MENTAL ARITHMETIC
new_ma_setup_frame, new_mental_arithmetic_frame = None, None
new_ma_checks = None

# TITLE: STROOP
stroop_setup_frame, stroop_frame = None, None
congruency_proportion = 0.5
stroop_checks = None

# TITLE: NBACK
nb_setup_frame, nback_frame = None, None
grid_boxes = None

# TITLE: CALIBRATION

style = ttk.Style()
style.configure('my.TMenubutton', font=DefaultFont)

calibration_frame = None
calibration_setup = None
calib_checks = None
set_lang = None
languages = {
 'Afrikaans': 'af',
 'Basque': 'eu',
 'Bulgarian': 'bg',
 'Catalan': 'ca',
 'Arabic (Egypt)': 'ar-EG',
 'Arabic (Jordan)': 'ar-JO',
 'Arabic (Kuwait)': 'ar-KW',
 'Arabic (Lebanon)': 'ar-LB',
 'Arabic (Qatar)': 'ar-QA',
 'Arabic (UAE)': 'ar-AE',
 'Arabic (Morocco)': 'ar-MA',
 'Arabic (Iraq)': 'ar-IQ',
 'Arabic (Algeria)': 'ar-DZ',
 'Arabic (Bahrain)': 'ar-BH',
 'Arabic (Lybia)': 'ar-LY',
 'Arabic (Oman)': 'ar-OM',
 'Arabic (Saudi Arabia)': 'ar-SA',
 'Arabic (Tunisia)': 'ar-TN',
 'Arabic (Yemen)': 'ar-YE',
 'Czech': 'cs',
 'Dutch': 'nl-NL',
 'English (Australia)': 'en-AU',
 'English (Canada)': 'en-CA',
 'English (India)': 'en-IN',
 'English (New Zealand)': 'en-NZ',
 'English (South Africa)': 'en-ZA',
 'English(UK)': 'en-GB',
 'English(US) - default': 'en-US',
 'Finnish': 'fi',
 'French': 'fr-FR',
 'Galician': 'gl',
 'German': 'de-DE',
 'Hebrew': 'he',
 'Hungarian': 'hu',
 'Icelandic': 'is',
 'Italian': 'it-IT',
 'Indonesian': 'id',
 'Japanese': 'ja',
 'Korean': 'ko',
 'Latin': 'la',
 'Mandarin Chinese': 'zh-CN',
 'Traditional Taiwan': 'zh-TW',
 'Simplified Hong Kong': 'zh-HK',
 'Yue Chinese (Traditional Hong Kong)': 'zh-yue',
 'Malaysian': 'ms-MY',
 'Norwegian': 'no-NO',
 'Polish': 'pl',
 'Pig Latin': 'xx-piglatin',
 'Portuguese': 'pt-PT',
 'Portuguese (brasil)': 'pt-BR',
 'Romanian': 'ro-RO',
 'Russian': 'ru',
 'Serbian': 'sr-SP',
 'Slovak': 'sk',
 'Spanish (Argentina)': 'es-AR',
 'Spanish(Bolivia)': 'es-BO',
 'Spanish( Chile)': 'es-CL',
 'Spanish (Colombia)': 'es-CO',
 'Spanish(Costa Rica)': 'es-CR',
 'Spanish(Dominican Republic)': 'es-DO',
 'Spanish(Ecuador)': 'es-EC',
 'Spanish(El Salvador)': 'es-SV',
 'Spanish(Guatemala)': 'es-GT',
 'Spanish(Honduras)': 'es-HN',
 'Spanish(Mexico)': 'es-MX',
 'Spanish(Nicaragua)': 'es-NI',
 'Spanish(Panama)': 'es-PA',
 'Spanish(Paraguay)': 'es-PY',
 'Spanish(Peru)': 'es-PE',
 'Spanish(Puerto Rico)': 'es-PR',
 'Spanish(Spain)': 'es-ES',
 'Spanish(US)': 'es-US',
 'Spanish(Uruguay)': 'es-UY',
 'Spanish(Venezuela)': 'es-VE',
 'Swedish': 'sv-SE',
 'Turkish': 'tr',
 'Zulu': 'zu'}
