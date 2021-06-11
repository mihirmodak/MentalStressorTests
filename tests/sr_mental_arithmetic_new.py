from tkinter import *
import variables as db
import settings as s
import numpy as np
import time
import random
import speech_recognition as sr

# TITLE: INITIALIZE VARIABLES
db.new_ma_setup_frame = Frame(db.root)
db.new_mental_arithmetic_frame = Frame(db.root)
num_range = None
selected_difficulty = None
mode = []
num_trials = None
question_prompt = None
file = None
label_t = None
answer = None
check_label = Label(db.new_mental_arithmetic_frame, font=db.DefaultFont)
default_time, start_time = None, None
skip_enabled = True
stop_listening = None
pronounce = {'two': 2, 'pass': -1}


def create_record(save):
    global file
    print("Identifier entered as:" + db.identifier)
    try:
        if save:
            db.save_folder = s.create_save_path()
            filename = str(db.save_folder) + "new_mental_arithmetic.txt"
            file = open(filename, "a+")
        else:
            return None
    except Exception as e:
        s.error_handler(db.new_ma_setup_frame, e, 5)


def question():
    try:
        global num_range, mode, question_prompt, answer, default_time, start_time, num_trials

        default_time = time.time()
        db.timer = start_time

        num_trials = 0

        prompt = "Invalid test mode(s) selected"

        number = random.randrange(num_range[0], num_range[1])
        intermediate = 0
        for i in str(number):
            intermediate += int(i)

        a = random.choice(mode)

        if a == 'ADDITION':
            answer = number + intermediate
            prompt = (str(number) + ", + ")
        elif a == 'SUBTRACTION':
            answer = number - intermediate
            prompt = (str(number) + ", - ")
        elif a == 'MULTIPLICATION':
            answer = number * intermediate
            prompt = (str(number) + ", * ")
        elif a == 'DIVISION':
            answer = number // intermediate
            prompt = (str(number) + ", ÷ ")
        else:
            raise Exception(prompt)

        if num_trials == 0:
            question_prompt = Label(db.new_mental_arithmetic_frame, text=prompt, width=45,
                                    bg='orange', font=db.GiantFont)
            question_prompt.grid(row=2, column=0, columnspan=2, ipadx=0, sticky=NW)
            # question_prompt.bind("<Button-1>", s.font_resize)
        else:
            # question_prompt = Label(db.new_mental_arithmetic_frame)
            question_prompt.config(text=prompt)

        db.errorLabel1.grid_forget()
        db.errorLabel2.grid_forget()

        return answer
    except Exception as e:
        s.error_handler(db.new_mental_arithmetic_frame, e, 5)


def end_program(test_frame):
    global file, stop_listening, label_t
    if file is not None:
        file.close()
    if label_t is not None:
        label_t.grid_forget()
    s.exit_test(test_frame, stop_listening)


def start():
    # Step 1: Get all the necessary variables
    global num_range, selected_difficulty, mode, num_trials, file, label_t, answer, \
        default_time, skip_enabled, stop_listening, start_time

    # Step 2: Set up Exception Handling
    try:
        create_record(save=True)  # Create empty save files

        # Step 3: Identify the Difficulty and the Test Types (Addition, Subtraction, etc.)
        selected = []
        for value in list(db.new_ma_checks.values()):
            selected.append(value.get())
        selected_difficulty = list(db.new_ma_checks.keys())[selected.index(1, 0, 3)]
        if selected[3] == 1:
            skip_enabled = True

        if selected_difficulty == "EASY":
            num_range = [1, 99]
        elif selected_difficulty == "MEDIUM":
            num_range = [100, 999]
        elif selected_difficulty == "HARD":
            num_range = [1000, 9999]
        else:
            raise Exception("Please select a difficulty")

        mode_indices = np.where(np.isin(selected, 1))[0]
        mode_indices = mode_indices[mode_indices > 3]
        mode = [list(db.new_ma_checks.keys())[i] for i in mode_indices]

    except Exception as e:
        s.error_handler(db.new_ma_setup_frame, e, 5, 5)
        return

    try:
        # Step 4: Get rid of the setup screen and start the test
        db.new_ma_setup_frame.forget()

        # Step 4b: Add an exit button
        Button(
            master=db.new_mental_arithmetic_frame,
            text="X",
            command=lambda: end_program(db.new_mental_arithmetic_frame),
            bg='#a60000',
            fg='white',
            activebackground='#d60000',
            activeforeground='white',
            font=db.SmallFont
        ).grid(row=0, column=1, sticky=N)

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
        label_t = Label(db.new_mental_arithmetic_frame, text=f'Time:0.0, Attempts: {2 - num_trials}',
                        font=db.HeadingFont)
        label_t.grid(row=1, column=0, columnspan=2, pady=50)

        # Step 7: Start listening through microphone
        with db.microphone as source:
            db.recognizer.adjust_for_ambient_noise(source)

        stop_listening = db.recognizer.listen_in_background(db.microphone, submit)

        # Step 8: Create instructions label
        Label(db.new_mental_arithmetic_frame, text="Listening...", font=db.DefaultFont) \
            .grid(row=4, column=0, columnspan=2)

        # Step 9: Display it all
        db.new_mental_arithmetic_frame.pack()

        # Step 10: Endlessly update timer
        while True:
            # put the timer value into the label
            label_t.config(text=f"Time: {db.timer}, Attempts: {2 - num_trials}")
            # wait for 0.1 seconds
            time.sleep(0.1)
            # needed with time.sleep()
            db.new_mental_arithmetic_frame.update()
            # update timer
            db.timer = round(time.time() - default_time, 2)

    except Exception as e:
        s.error_handler(db.new_mental_arithmetic_frame, e, 5, display=False)


def submit(recognizer, audio):
    global answer, check_label, file, default_time, num_trials

    if num_trials == 1:
        check_label = Label(db.stroop_frame, text="Thinking...", fg='black', font=db.DefaultFont)
        check_label.grid(row=5, column=0, columnspan=2)
    else:
        check_label.config(text="Thinking...", fg='black')

    try:
        # raise NotImplementedError("The answer submitter function has not been implemented")

        try:
            submitted = recognizer.recognize_google(audio)
            print(submitted)
            try:
                if submitted in pronounce.keys():
                    submitted = pronounce[submitted]
                if submitted == db.skip_keyword and skip_enabled:
                    pass
                else:
                    submitted = int(submitted)
            except ValueError:
                raise Exception("I can only understand numbers. Please repeat your answer.")
        except sr.UnknownValueError:
            raise Exception("Sorry, didn't catch that")
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Google Speech Recognition service; {e}")

        check_label.destroy()
        db.errorLabel1.grid_forget()
        db.errorLabel2.grid_forget()

        if answer != submitted:
            num_trials += 1
            if submitted != db.skip_keyword:
                message = f"Wrong"
                db.errorLabel1.grid_forget()
                db.errorLabel2.grid_forget()
                check_label = Label(db.new_mental_arithmetic_frame, text=message, fg='red', font=db.DefaultFont)
                check_label.grid(row=5, column=0, columnspan=2)

                if file is not None:
                    # if db.var == 1:
                    file.write("Wrong,      Time Stamp: {}\n\n".format(round(time.time() - default_time, 2)))
                print("Wrong,      Time Stamp: ", round(time.time() - default_time, 2))

                if num_trials >= 2:
                    answer = question()

            else:
                message = f"Question skipped."
                db.errorLabel1.grid_forget()
                db.errorLabel2.grid_forget()
                check_label = Label(db.new_mental_arithmetic_frame, text=message, fg='black', font=db.DefaultFont)
                check_label.grid(row=5, column=0, columnspan=2)

                if file is not None:
                    file.write(f"Skipped")
                answer = question()

        else:
            message = f"Correct"
            db.errorLabel1.grid_forget()
            db.errorLabel2.grid_forget()
            check_label = Label(db.new_mental_arithmetic_frame, text=message, fg='green', font=db.DefaultFont)
            check_label.grid(row=5, column=0, columnspan=2)

            if file is not None:
                file.write("Correct,   Time Stamp: {}\n\n".format(round(time.time() - default_time, 2)))
            print("Correct,    Time Stamp: ", round(time.time() - default_time, 2))
            answer = question()

        db.new_mental_arithmetic_frame.after(2000, check_label.grid_forget)

    except Exception as e:
        s.error_handler(db.new_mental_arithmetic_frame, e, 6, 2)


# TITLE: GUI
def setup():
    try:
        # Step 1: Add an exit button
        Button(
            master=db.new_ma_setup_frame,
            text="X",
            command=lambda: end_program(db.new_ma_setup_frame),
            bg='#a60000',
            fg='white',
            activebackground='#d60000',
            activeforeground='white',
            font=db.SmallFont
        ).grid(row=0, column=100, sticky=NE)

        # Add some spacing below the exit button
        # db.new_ma_setup_frame.grid_rowconfigure(1, weight=1, minsize=50)

        # Step 2: Create Checkboxes for Test Type and Difficulty
        difficulties = ('EASY', 'MEDIUM', 'HARD', 'SKIP')
        types = ('ADDITION', 'SUBTRACTION', 'MULTIPLICATION', 'DIVISION')
        db.new_ma_checks = {}

        for index, name in enumerate(difficulties):
            # print(name, index)
            db.new_ma_checks[name] = IntVar()
            Checkbutton(
                master=db.new_ma_setup_frame,
                text=difficulties[index],
                variable=db.new_ma_checks[name],
                font=db.DefaultFont
            ).grid(row=2, column=index, sticky=W)

        for index, name in enumerate(types):
            # print(name, index)
            db.new_ma_checks[name] = IntVar()
            Checkbutton(
                master=db.new_ma_setup_frame,
                text=types[index],
                variable=db.new_ma_checks[name],
                font=db.DefaultFont
            ).grid(row=3, column=index, sticky=W)

        # Add some spacing below the exit button
        db.new_ma_setup_frame.grid_rowconfigure(4, weight=1, minsize=150)

        # Step 3: Add a 'Start' Button
        Button(
            master=db.new_ma_setup_frame,
            text="Start Test",
            command=start,
            activebackground="blue",
            activeforeground="white",
            bg="white",
            fg="black",
            font=db.DefaultFont,
        ).grid(row=4, columnspan=5, ipadx=200, pady=20)

    except Exception as e:
        s.error_handler(db.new_ma_setup_frame, e, 5)

    db.new_ma_setup_frame.pack()
