import variables as db
from tkinter import *
from tkinter.font import Font
import os, sys
from datetime import datetime

from tests import sr_mental_arithmetic, stroop, nback, sr_mental_arithmetic_new


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

    db.errorLabel1.grid_forget()
    db.errorLabel2.grid_forget()

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


def font_resize(event):
    print(dir(event))
    db.GiantFont.config(size=event.__sizeof__())


# TITLE: BUTTON FUNCTIONS
def activate_mental_arithmetic(identifier_widget):
    db.identifier = identifier_widget.get().strip()
    if db.identifier == "":
        db.identifier = "Unknown"
    db.MainFrame.forget()
    sr_mental_arithmetic.setup()

def activate_new_mental_arithmetic(identifier_widget):
    db.identifier = identifier_widget.get().strip()
    if db.identifier == "":
        db.identifier = "Unknown"
    db.MainFrame.forget()
    sr_mental_arithmetic_new.setup()


def activate_stroop(identifier_widget):
    db.identifier = identifier_widget.get().strip()
    if db.identifier == "":
        db.identifier = "Unknown"
    db.MainFrame.forget()
    stroop.setup()


def activate_nback(identifier_widget):
    db.identifier = identifier_widget.get().strip()
    if db.identifier == "":
        db.identifier = "Unknown"
    db.MainFrame.forget()
    nback.setup()


def exit_test(TestFrame, callback_fun):
    db.errorLabel1.grid_forget()
    db.errorLabel2.grid_forget()
    if callback_fun is not None:
        callback_fun(wait_for_stop=False)
    TestFrame.forget()
    db.MainFrame.pack()
