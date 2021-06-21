from tkinter import *
import variables as db
import settings as s
import numpy as np
import time
import random
import array
import speech_recognition as sr

# TITLE: INITIALIZE VARIABLES
db.stroop_setup_frame = Frame(db.root)
db.stroop_frame = Frame(db.root)
selected_difficulty = None
options = ('green', 'blue', 'yellow', 'orange')
num_trials = None
question_prompt = None
file = None
label_t = None
answer1, answer2 = None, None
check_label = Label(db.stroop_frame, font=db.DefaultFont)
default_time, start_time = None, None
skip_enabled = None
stop_listening = None
problematic_nums = {
    'two': 2
}


def create_record(save):
    global file
    print("Identifier entered as:" + db.identifier)
    try:
        if save:
            db.save_folder = s.create_save_path()
            filename = str(db.save_folder) + "stroop.txt"
            file = open(filename, "a+")
        else:
            return None
    except Exception as e:
        s.error_handler(db.stroop_setup_frame, e, 5)


def question():
    # global check_label
    # check_label.grid_forget()
    try:
        global options, question_prompt, answer1, answer2, default_time, start_time

        default_time = time.time()
        db.timer = start_time

        color = random.choice(options)

        if random.random() <= db.congruency_proportion:
            word = random.choice(options).upper()
        else:
            word = color.upper()

        answer1 = db.pronounce[color]
        answer2 = color

        db.errorLabel1.grid_forget()
        db.errorLabel2.grid_forget()

        Label(db.stroop_frame, text="", width=45, bg='white', fg=color, font=db.HeadingFont).grid(row=3)
        time.sleep(0.00001)
        Label(db.stroop_frame, text=word, width=45, bg='gray', fg=color, font=db.HeadingFont).grid(row=3)

        return answer1, answer2
    except Exception as e:
        s.error_handler(db.stroop_frame, e, 5)


def end_program(test_frame):
    global file, stop_listening
    if file is not None:
        file.close()
    label_t.destroy()
    s.exit_test(test_frame, stop_listening)


def start():
    # Step 1: Get all the necessary variables
    global selected_difficulty, num_trials, file, label_t, answer1, answer2, \
        default_time, skip_enabled, stop_listening, start_time

    # Step 2: Set up Exception Handling
    try:
        create_record(save=True)  # Create empty save files

        # Step 3: Identify the Difficulty and the Test Types (Addition, Subtraction, etc.)
        selected = []
        for value in list(db.stroop_checks.values()):
            selected.append(value.get())
        selected_difficulty = list(db.stroop_checks.keys())[selected.index(1)]

        if selected_difficulty == "EASY":
            db.congruency_proportion = 0.7
        elif selected_difficulty == "MODERATE":
            db.congruency_proportion = 0.5
        elif selected_difficulty == "HARD":
            db.congruency_proportion = 0.1
        else:
            raise Exception("Please select a difficulty")

    except Exception as e:
        s.error_handler(db.stroop_setup_frame, e, 5, 5)
        return

    try:
        # Step 4: Get rid of the setup screen and start the test
        db.stroop_setup_frame.forget()

        # Step 4b: Add an exit button
        Button(
            master=db.stroop_frame,
            text="X",
            command=lambda: end_program(db.stroop_frame),
            bg='#a60000',
            fg='white',
            activebackground='#d60000',
            activeforeground='white',
            font=db.DefaultFont
        ).grid(row=0, column=100, sticky=NE)

        num_trials = 0
        answer1, answer2 = question()
        default_time = time.time()
        start_time = round(time.time() - default_time, 2)
        db.timer = start_time

        # Step 5: Start writing test difficulty data to the save files
        if file is not None:
            file.write(selected_difficulty + ' ' + str(selected_difficulty) + '\n')
            file.write("START,     Time Stamp: {}\n".format(start_time))
        print(selected_difficulty)
        print("START,      Time Stamp: ", start_time)

        # Step 6: Add a timer
        label_t = Label(db.stroop_frame, text='0.0', font=db.HeadingFont)
        label_t.grid(row=1, column=0, columnspan=2, pady=50)

        # Step 7: Start listening through microphone
        with db.microphone as source:
            db.recognizer.adjust_for_ambient_noise(source)

        stop_listening = db.recognizer.listen_in_background(db.microphone, submit)

        # Step 8: Create instructions label
        Label(db.stroop_frame, text="Say the color of the text", font=db.DefaultFont) \
            .grid(row=4, column=0, columnspan=2)
        # Step 9: Display it all
        db.stroop_frame.pack()

        # Step 10: Endlessly update timer
        while True:
            # put the timer value into the label
            label_t.config(text=str(db.timer))
            # wait for 0.1 seconds
            time.sleep(0.1)
            # needed with time.sleep()
            db.stroop_frame.update()
            # update timer
            db.timer = round(time.time() - default_time, 2)

    except Exception as e:
        s.error_handler(db.stroop_frame, e, 5, display=False)


def submit(recognizer, audio):
    global answer1, answer2, check_label, file, default_time, options, num_trials

    if num_trials == 1:
        check_label = Label(db.stroop_frame, text="Thinking...", fg='black', font=db.DefaultFont)
        check_label.grid(row=5, column=0, columnspan=2)
    else:
        check_label.config(text="Thinking...", fg='black')

    try:
        # raise NotImplementedError("The answer submitter function has not been implemented")

        num_trials += 1
        try:
            submitted = recognizer.recognize_google(audio)
            print(submitted)
            try:
                assert submitted in options or submitted == db.skip_keyword or submitted in db.pronounce.values()\
                    or answer1 in db.pronounce.values()
            except AssertionError:
                raise Exception("Please say a valid color: Red, Yellow, Blue, or Green.")
        except sr.UnknownValueError:
            raise Exception("Sorry, didn't catch that")
        except sr.RequestError as e:
            raise Exception(f"Couldn't request results from Google Speech Recognition service; {e}")

        if submitted == db.skip_keyword:
            message = f"Question Skipped"
            db.errorLabel1.grid_forget()
            db.errorLabel2.grid_forget()

            if num_trials == 1:
                check_label = Label(db.stroop_frame, text=message, fg='black', font=db.DefaultFont)
                check_label.grid(row=5, column=0, columnspan=2)
            else:
                check_label.config(text=message, fg='black')

            if file is not None:
                # if db.var == 1:
                file.write("Skipped, Time Stamp: {}\n\n".format(round(time.time() - default_time, 2)))
            print("Skipped, Time Stamp: ", round(time.time() - default_time, 2))
            pass
        else:
            if submitted.lower() not in [answer1.lower(), answer2.lower()]:
                message = f"Wrong"
                db.errorLabel1.grid_forget()
                db.errorLabel2.grid_forget()

                if num_trials == 1:
                    check_label = Label(db.stroop_frame, text=message, fg='red', font=db.DefaultFont)
                    check_label.grid(row=5, column=0, columnspan=2)
                else:
                    check_label.config(text=message, fg='red')

                if file is not None:
                    # if db.var == 1:
                    file.write("Wrong, Time Stamp: {}\n\n".format(round(time.time() - default_time, 2)))
                print("Wrong, Time Stamp: ", round(time.time() - default_time, 2))

            else:
                message = f"Correct"
                db.errorLabel1.grid_forget()
                db.errorLabel2.grid_forget()
                if num_trials == 1:
                    check_label = Label(db.stroop_frame, text=message, fg='green', font=db.DefaultFont)
                    check_label.grid(row=5, column=0, columnspan=2)
                else:
                    check_label.config(text=message, fg='green')

                if file is not None:
                    file.write("Correct, Time Stamp: {}\n\n".format(round(time.time() - default_time, 2)))
                print("Correct, Time Stamp: ", round(time.time() - default_time, 2))

        answer1, answer2 = question()
        db.stroop_frame.after(2000, check_label.grid_forget)

    except Exception as e:
        s.error_handler(db.stroop_frame, e, 6, 2)


# TITLE: GUI
def setup():
    try:
        # Step 1: Add an exit button
        Button(
            master=db.stroop_setup_frame,
            text="X",
            command=lambda: end_program(db.stroop_setup_frame),
            bg='#a60000',
            fg='white',
            activebackground='#d60000',
            activeforeground='white',
            font=db.DefaultFont
        ).grid(row=0, column=100, sticky=NE)

        # Add some spacing below the exit button
        # db.stroop_setup_frame.grid_rowconfigure(1, weight=1, minsize=50)

        # Step 2: Create Checkboxes for Test Type and Difficulty
        difficulties = ('EASY', 'MODERATE', 'HARD', 'PASS')
        db.stroop_checks = {}

        for index, name in enumerate(difficulties):
            # print(name, index)
            db.stroop_checks[name] = IntVar()
            Checkbutton(
                master=db.stroop_setup_frame,
                text=difficulties[index],
                variable=db.stroop_checks[name],
                font=db.DefaultFont
            ).grid(row=2, column=index, sticky=W)

        # Add some spacing below the exit button
        db.stroop_setup_frame.grid_rowconfigure(3, weight=1, minsize=150)

        # Step 3: Add a 'Start' Button
        Button(
            master=db.stroop_setup_frame,
            text="Start Test",
            command=start,
            activebackground="blue",
            activeforeground="white",
            bg="white",
            fg="black",
            font=db.DefaultFont,
        ).grid(row=3, columnspan=5, ipadx=200, pady=20)

    except Exception as e:
        s.error_handler(db.stroop_setup_frame, e, 5)

    db.stroop_setup_frame.pack()
