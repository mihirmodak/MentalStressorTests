from tkinter import *
import variables as db
import settings as s
from tests import sr_mental_arithmetic, stroop, nback, sr_mental_arithmetic_new
import calibration


# Make it look nice
db.root['padx'] = 100
db.root['pady'] = 100
db.root.title("Stress Test")
db.root.geometry("1500x800")


def main():

    # Step 1: Create a Frame to hold everything and add an exit button
    db.MainFrame = Frame(db.root)

    # Step 2: Ask for subject identifier
    # The label
    identifier_label_text = "Enter the subject identifier:"
    Label(db.MainFrame, text=identifier_label_text, font=db.HeadingFont).grid(row=1)

    # The answer box
    identifier_widget = Entry(db.MainFrame, font=db.DefaultFont, width=int(len(identifier_label_text)//1.5),
                              justify='center')
    identifier_widget.grid(row=2, pady=10)

    # Step 3: Choose a test
    Label(db.MainFrame, text="Choose a test, or press q to exit.", font=db.HeadingFont).grid(row=4)

    Button(
        master=db.MainFrame,
        text="Calibration",
        # command=lambda: s.calibrate(identifier_widget),
        command=lambda: s.activate_test(calibration, identifier_widget),
        activebackground="blue",
        activeforeground="white",
        bg="white",
        fg="black",
        font=db.HeadingFont,
        width=50,
        state=NORMAL
    ).grid(row=5, pady=10)

    Button(
        master=db.MainFrame,
        text="Mental Arithmetic Test",
        # command=lambda: s.activate_mental_arithmetic(identifier_widget),
        command=lambda: s.activate_test(sr_mental_arithmetic, identifier_widget),
        activebackground="blue",
        activeforeground="white",
        bg="white",
        fg="black",
        font=db.HeadingFont,
        width=50,
        state=NORMAL
    ).grid(row=6, pady=10)

    Button(
        master=db.MainFrame,
        text="2-Step Mental Arithmetic Test",
        # command=lambda: s.activate_new_mental_arithmetic(identifier_widget),
        command=lambda: s.activate_test(sr_mental_arithmetic_new, identifier_widget),
        activebackground="blue",
        activeforeground="white",
        bg="white",
        fg="black",
        font=db.HeadingFont,
        width=50,
        state=NORMAL
    ).grid(row=7, pady=10)

    Button(
        master=db.MainFrame,
        text="N-Back Test",
        # command=lambda: s.activate_nback(identifier_widget),
        command=lambda: s.activate_test(nback, identifier_widget),
        activebackground="blue",
        activeforeground="white",
        bg="white",
        fg="black",
        font=db.HeadingFont,
        width=50,
        state=NORMAL
    ).grid(row=8, pady=10)

    Button(
        master=db.MainFrame,
        text="Stroop Color Test",
        # command=lambda: s.activate_stroop(identifier_widget),
        command=lambda: s.activate_test(stroop, identifier_widget),
        activebackground="blue",
        activeforeground="white",
        bg="white",
        fg="black",
        font=db.HeadingFont,
        width=50,
        state=NORMAL
    ).grid(row=9, pady=10)

    db.MainFrame.pack()
    db.root.mainloop()


if __name__ == '__main__':
    main()
