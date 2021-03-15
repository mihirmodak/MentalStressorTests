from tkinter import *
import variables as db
import settings as s
from functools import partial
import numpy as np
import time
import random

# TITLE: INITIALIZE VARIABLES
db.ma_setup_frame = Frame(db.root)
db.mental_arithmetic_frame = Frame(db.root)
num_range1 = None
num_range2 = None
selected_difficulty = None
mode = []
num_trials = None
question_prompt = None
file = None
label_t = None
answer = None
check_label = Label(db.mental_arithmetic_frame, font=db.DefaultFont)
default_time = None
pass_enabled = None


# TITLE: HELPER FUNCTIONS
def create_record(save):
    global file
    print("Identifier entered as:" + db.identifier)
    try:
        if save:
            db.save_folder = s.create_save_path()
            filename = str(db.save_folder) + "mental_arithmetic.txt"
            file = open(filename, "a+")
        else:
            return None
    except Exception as e:
        s.error_handler(db.ma_setup_frame, e, 5)


def question():
    try:
        global num_range1, num_range2, mode, question_prompt, answer
        # raise NotImplementedError("The question generator function has not been implemented")

        prompt = "Invalid test mode(s) selected"

        number1 = random.randrange(num_range1[0], num_range1[1])
        number2 = random.randrange(num_range2[0], num_range2[1])

        a = random.choice(mode)

        if a == 'ADDITION':
            answer = number1 + number2
            prompt = (str(number1) + " + " + str(number2))
        elif a == 'SUBTRACTION':
            answer = max(number1, number2) - min(number1, number2)
            prompt = (str(max(number1, number2)) + " - " + str(min(number1, number2)))
        elif a == 'MULTIPLICATION':
            answer = number1 * number2
            prompt = (str(number1) + " * " + str(number2))
        elif a == 'DIVISION':
            temp_answer = number1 * number2
            answer = number1
            prompt = (str(temp_answer) + " / " + str(number2))
        else:
            raise Exception(prompt)

        if num_trials == 0:
            question_prompt = Label(db.mental_arithmetic_frame, text=prompt, width=45, bg='orange', font=db.DefaultFont)
            question_prompt.grid(row=2, column=0, columnspan=2)
        else:
            # question_prompt = Label(db.mental_arithmetic_frame)
            question_prompt.config(text=prompt)

        return answer
    except Exception as e:
        s.error_handler(db.mental_arithmetic_frame, e, 5)


def submit(entry_widget):
    global answer, check_label, file, default_time
    try:
        # raise NotImplementedError("The answer submitter function has not been implemented")
        global num_trials

        num_trials += 1
        submitted = int(entry_widget.get().strip())

        if answer != submitted:
            if num_trials == 1:
                check_label = Label(db.mental_arithmetic_frame, text="Wrong", fg='red', font=db.DefaultFont)
                check_label.grid(row=5, column=0, columnspan=2)
                entry_widget.delete(0, 'end')

            else:
                check_label.config(text="Wrong", fg='red')
                entry_widget.delete(0, 'end')

            if file is not None:
                # if db.var == 1:
                file.write("Wrong,      Time Stamp: {}\n\n".format(round(time.time() - default_time, 2)))
            print("Wrong,      Time Stamp: ", round(time.time() - default_time, 2))
            answer = question()

        else:
            if num_trials == 1:
                check_label = Label(db.mental_arithmetic_frame, text="Correct", fg='black', font=db.DefaultFont)
                check_label.grid(row=5, column=0, columnspan=2)
                entry_widget.delete(0, 'end')
            else:
                check_label.config(text="Correct", fg='black')
                entry_widget.delete(0, 'end')

            if file is not None:
                file.write("Correct,   Time Stamp: {}\n\n".format(round(time.time() - default_time, 2)))
            print("Correct,    Time Stamp: ", round(time.time() - default_time, 2))
            answer = question()

    except Exception as e:
        s.error_handler(db.mental_arithmetic_frame, e, 5, 2)


def start():
    # Step 1: Get all the necessary variables
    global num_range1, num_range2, selected_difficulty, mode, num_trials, file, label_t, answer, \
        default_time, pass_enabled

    # Step 2: Set up Exception Handling
    try:
        create_record(save=True)  # Create empty save files

        # Step 3: Identify the Difficulty and the Test Types (Addition, Subtraction, etc.)
        selected = []
        for value in list(db.checks.values()):
            selected.append(value.get())
        selected_difficulty = list(db.checks.keys())[selected.index(1, 0, 3)]
        if selected[3] == 1: pass_enabled = True

        if selected_difficulty == "EASY":
            num_range1 = [1, 10]
            num_range2 = [1, 10]
        elif selected_difficulty == "MODERATE":
            num_range1 = [11, 50]
            num_range2 = [1, 10]
        elif selected_difficulty == "HARD":
            num_range1 = [11, 100]
            num_range2 = [11, 100]
        else:
            raise Exception("Please select a difficulty")

        mode_indices = np.where(np.isin(selected, 1))[0]
        mode_indices = mode_indices[mode_indices > 3]
        mode = [list(db.checks.keys())[i] for i in mode_indices]

    except Exception as e:
        s.error_handler(db.ma_setup_frame, e, 5, 5)
        return

    try:
        # Step 4: Get rid of the setup screen and start the test
        db.ma_setup_frame.forget()

        # Step 4b: Add an exit button
        Button(
            master=db.mental_arithmetic_frame,
            text="X",
            command=partial(end_program, db.mental_arithmetic_frame),
            bg='#a60000',
            fg='white',
            activebackground='#d60000',
            activeforeground='white',
        ).grid(row=0, column=100, sticky=NE)

        num_trials = 0
        answer = question()
        default_time = time.time()
        start_time = round(time.time() - default_time, 2)
        db.timer = start_time

        # Step 5: Start writing test difficulty data to the save files
        if file is not None:
            file.write(selected_difficulty + ' ' + str(mode) + '\n')
            file.write("START,     Time Stamp: {}\n".format(start_time))
        print(selected_difficulty, mode[0:])
        print("START,      Time Stamp: ", start_time)

        # Step 6: Add a timer
        label_t = Label(db.mental_arithmetic_frame, text='0.0', font=db.HeadingFont)
        label_t.grid(row=1, column=0, columnspan=2, pady=50)

        # Step 7: Create an Entry Widget to allow for answer input
        # TODO: Replace the entry widget with speech recognition
        Label(db.mental_arithmetic_frame, text="Answer:", font=db.DefaultFont) \
            .grid(row=3, column=0, sticky='E', pady=50)
        entry_widget = Entry(db.mental_arithmetic_frame, font=db.DefaultFont)
        entry_widget.bind('<Return>', lambda event: submit(entry_widget))
        entry_widget.grid(row=3, column=1, sticky='W', pady=50)

        # Step 8: Create instructions label
        Label(db.mental_arithmetic_frame, text="Press Enter to submit", font=db.DefaultFont) \
            .grid(row=4, column=0, columnspan=2)
        # Step 9: Display it all
        db.mental_arithmetic_frame.pack()

        # Step 10: Endlessly update timer
        while True:
            # put the timer value into the label
            label_t.config(text=str(db.timer))
            # wait for 0.1 seconds
            time.sleep(0.1)
            # needed with time.sleep()
            db.mental_arithmetic_frame.update()
            # update timer
            db.timer = round(time.time() - default_time, 2)

    except Exception as e:
        s.error_handler(db.mental_arithmetic_frame, e, 5, display=False)


def end_program(test_frame):
    global file
    if file is not None:
        file.close()
    label_t.destroy()
    s.exit_test(test_frame)


# TITLE: GUI
def main():
    try:
        # Step 1: Add an exit button
        Button(
            master=db.ma_setup_frame,
            text="X",
            command=partial(end_program, db.ma_setup_frame),
            bg='#a60000',
            fg='white',
            activebackground='#d60000',
            activeforeground='white',
        ).grid(row=0, column=100, sticky=NE)

        # Add some spacing below the exit button
        # db.ma_setup_frame.grid_rowconfigure(1, weight=1, minsize=50)

        # Step 2: Create Checkboxes for Test Type and Difficulty
        difficulties = ('EASY', 'MODERATE', 'HARD', 'PASS')
        types = ('ADDITION', 'SUBTRACTION', 'MULTIPLICATION', 'DIVISION')
        db.checks = {}

        for index, name in enumerate(difficulties):
            # print(name, index)
            db.checks[name] = IntVar()
            Checkbutton(
                master=db.ma_setup_frame,
                text=difficulties[index],
                variable=db.checks[name],
                font=db.DefaultFont
            ).grid(row=2, column=index, sticky=W)

        for index, name in enumerate(types):
            # print(name, index)
            db.checks[name] = IntVar()
            Checkbutton(
                master=db.ma_setup_frame,
                text=types[index],
                variable=db.checks[name],
                font=db.DefaultFont
            ).grid(row=3, column=index, sticky=W)

        # Add some spacing below the exit button
        db.ma_setup_frame.grid_rowconfigure(4, weight=1, minsize=150)

        # Step 3: Add a 'Start' Button
        Button(
            master=db.ma_setup_frame,
            text="Start Test",
            command=start,
            activebackground="blue",
            activeforeground="white",
            bg="white",
            fg="black",
            font=db.DefaultFont,
        ).grid(row=4, columnspan=5, ipadx=200, pady=20)

    except Exception as e:
        s.error_handler(db.ma_setup_frame, e, 5)

    db.ma_setup_frame.pack()


if __name__ == '__main__':
    main(db.root)
