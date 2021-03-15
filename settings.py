import variables as db
from tkinter import *
import os
from datetime import datetime
import speech_recognition as sr
import argparse

from tests import mental_arithmetic


def create_save_path():
    if sys.platform == "linux":
        if not os.path.isdir(
                f"./saves/{str(datetime.now().strftime('%Y-%m-%d'))}/{db.identifier}"):  # Check if the directory already exists
            os.makedirs(
                f"./saves/{str(datetime.now().strftime('%Y-%m-%d'))}/{db.identifier}")  # If it doesn't, then make it
        save_folder = f"{os.getcwd()}/saves/{datetime.now().strftime('%Y-%m-%d')}/{db.identifier}/"  # Set the save_folder path
    elif sys.platform == "win32":
        if not os.path.isdir(f".\\saves\\{str(datetime.now().strftime('%Y-%m-%d'))}\\{db.identifier}\\"):
            os.makedirs(f".\\saves\\{str(datetime.now().strftime('%Y-%m-%d'))}\\{db.identifier}\\")
        save_folder = f"{os.getcwd()}\\saves\\{str(datetime.now().strftime('%Y-%m-%d'))}\\{db.identifier}\\"

    return save_folder


def error_handler(frame, error, row_num, colspan=1, display=True):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    db.errorLabel1 = Label(
        frame,
        text=f"{exc_type} in file {os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]}, line {exc_tb.tb_lineno}",
        font=db.DefaultFont,
        fg='red'
    )
    if display: db.errorLabel1.grid(row=row_num, column=0, columnspan=colspan)

    db.errorLabel2 = Label(
        frame,
        text=f"Error: {error}",
        font=db.DefaultFont,
        fg='red'
    )
    if display: db.errorLabel2.grid(row=row_num + 1, column=0, columnspan=colspan)


def speech_recognition_init():
    try:
        # parser = argparse.ArgumentParser(description='Decide Time Limit')
        # parser.add_argument('--time', '-t', type=int)
        # db.mic_time_limit = parser.parse_args()

        r = sr.Recognizer()  # recognizer instance
        r.pause_threshold = 0.5  # minimum length of silence after speaking
        r.energy_threshold = 100  # set energy threshold
        r.dynamic_energy_threshold = False  # do not update ambient noise threshold

        db.microphone = sr.Microphone()  # microphone instance

        # raise NotImplementedError("The speech recognition has not been implemented")
    except Exception as e:
        error_handler(db.ma_setup_frame, e, 5)

# TITLE: BUTTON FUNCTIONS
def activate_mental_arithmetic(identifier_widget):
    db.identifier = identifier_widget.get().strip()
    db.MainFrame.forget()
    mental_arithmetic.main()


def exit_test(TestFrame):
    db.errorLabel1.destroy()
    db.errorLabel2.destroy()
    db.microphone.close()
    TestFrame.forget()
    db.MainFrame.pack()
