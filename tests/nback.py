from email.policy import default
from tkinter import *
import variables as db
import settings as s
import time
import random
import speech_recognition as sr

db.nb_setup_frame = Frame(db.root)
db.nback_frame = Frame(db.root)
num_back, num_trials, sec_per_trial = None, None, None
file, label_t = None, None
stop_listening = None
answer1, answer2, question_prompt, prev_nums = None, None, None, []
check_label = Label(db.nback_frame, font=db.DefaultFont)
default_time, start_time = None, None
problematic_nums = {'two': 2}
err_msg = None


def create_record(save):
    global file
    print("Identifier entered as:" + db.identifier)
    try:
        if save:
            db.save_folder = s.create_save_path()
            filename = str(db.save_folder) + "nback.txt"
            file = open(filename, "a+")
        else:
            return None
    except Exception as e:
        s.error_handler(db.nb_setup_frame, e, 5)


def question():
    try:
        global answer1, answer2, question_prompt, prev_nums, num_back, default_time, start_time

        default_time = time.time()
        db.timer = start_time

        # Choose the next number
        prompt = random.choice(range(10))

        while prompt in prev_nums:
            prompt = random.choice(range(10))

        if len(prev_nums) > num_back:
            prev_nums.remove(prev_nums[0])
        prev_nums.append(prompt)

        # if len(prev_nums) >= num_back + 1:
        #     prev_nums.remove(prev_nums[0])
        # prev_nums.append(prompt)

        if num_trials == 0:
            # question_prompt = Label(db.nback_frame, text=f"{prompt}, {[prev_nums]}", width=45, bg='orange',
            #                         font=db.HeadingFont)
            question_prompt = Label(db.nback_frame, text=f"{prompt}", width=45, bg='orange',
                                    font=db.HeadingFont)
            question_prompt.grid(row=2, column=0, columnspan=3)
        else:
            question_prompt.config(text=f"{prompt}")

        try:
            db.errorLabel1.grid_forget()
            db.errorLabel2.grid_forget()
        except:
            pass

        return db.pronounce[str(prev_nums[0])], prev_nums[0]

    except Exception as e:
        s.error_handler(db.nback_frame, e, 6, colspan=3)


def submit(recognizer, audio):
    global answer1, answer2, check_label, file, default_time, num_trials, err_msg

    if num_trials == 1:
        check_label = Label(db.nback_frame, text="Thinking...", fg='black', font=db.DefaultFont)
        check_label.grid(row=7, column=0, columnspan=3)
    else:
        check_label.config(text="Thinking...", fg='black')

    try:
        # raise NotImplementedError("The answer submitter function has not been implemented")

        num_trials += 1
        try:
            submitted = recognizer.recognize_google(audio)
            try:
                # if submitted in db.pronounce.values():
                #     submitted = db.pronounce[str(list(db.pronounce.keys()).index(submitted))]
                if submitted == db.skip_keyword:
                    print("Question Skipped")
                else:
                    submitted = int(submitted)
            except ValueError:
                err_msg = "I can only understand numbers. Please repeat your answer."
                raise Exception(err_msg)
        except sr.UnknownValueError:
            err_msg = "Sorry, didn't catch that"
            raise Exception(err_msg)
        except sr.RequestError as e:
            err_msg = f"Could not request results from Google Speech Recognition service; {e}"
            raise Exception(err_msg)

        if err_msg is not None:
            if file is not None:
                file.write(f"Error: {err_msg}, Time Stamp: {round(time.time() - db.global_start_time, 2)}\n\n")

        check_label.grid_forget()
        if submitted == db.skip_keyword:
            message = "Question Skipped"
            db.errorLabel1.grid_forget()
            db.errorLabel2.grid_forget()

            if num_trials == 1:
                check_label = Label(db.nback_frame, text=message, fg='black', font=db.DefaultFont)
                check_label.grid(row=7, column=0, columnspan=3)
            else:
                check_label.config(text=message, fg='black')

            if file is not None:
                # if db.var == 1:
                file.write("Skipped,{}, Time Stamp: {}\n\n".format(submitted, round(time.time() - db.global_start_time, 2)))
            print(f"Skipped,{submitted} Time Stamp: {round(time.time() - db.global_start_time, 2)}")
            print(prev_nums)
            pass
        else:
            if submitted not in [answer1, answer2]:
                if submitted != db.skip_keyword:
                    message = f"Wrong"
                    db.errorLabel1.grid_forget()
                    db.errorLabel2.grid_forget()
                    check_label.config(text=message, fg='red')
                    check_label.grid(row=7, column=0, columnspan=3)

                    if file is not None:
                        # if db.var == 1:
                        file.write("Wrong,{}, Time Stamp: {}\n\n".format(submitted, round(time.time() - db.global_start_time, 2)))
                    print(f"Wrong,{submitted},{answer1, answer2},Time Stamp: {round(time.time() - db.global_start_time, 2)}")
                else:
                    message = "Question skipped."
                    db.errorLabel1.grid_forget()
                    db.errorLabel2.grid_forget()
                    check_label.config(text=message, fg='black')
                    check_label.grid(row=7, column=0, columnspan=3)


            else:
                message = f"Correct"
                db.errorLabel1.grid_forget()
                db.errorLabel2.grid_forget()
                check_label.config(text=message, fg='green')
                check_label.grid(row=7, column=0, columnspan=3)


                if file is not None:
                    file.write("Correct,{},Time Stamp: {}\n\n".format(submitted, round(time.time() - db.global_start_time, 2)))
                print(f"Correct,{submitted},Time Stamp: {round(time.time() - db.global_start_time, 2)}")

        answer1, answer2 = question()
        db.nback_frame.after(2000, check_label.grid_forget)

    except Exception as e:
        s.error_handler(db.nback_frame, e, 6, colspan=3)


def start():
    # Step 1: Get all the necessary variables
    global sec_per_trial, num_back, num_trials, answer1, answer2, stop_listening, default_time, start_time, \
        prev_nums

    # Step 2: Implement Error Checking
    try:
        # raise NotImplementedError("The Start function has not been implemented")
        create_record(save=True)  # Create empty save files

        # Step 3: Identify the Difficulty and the Test Types (1-back, 2-back, etc.)
        selected = []
        for value in list(db.grid_boxes.values()):
            selected.append(value.get())
        selected_difficulty = list(db.grid_boxes.keys())[selected.index(1, 0, 3)]
        selected_type = list(db.grid_boxes.keys())[selected.index(1, 3, 6)]

        if selected_difficulty == "7 sec/trial":
            sec_per_trial = 7
        elif selected_difficulty == "5 sec/trial":
            sec_per_trial = 5
        elif selected_difficulty == "3 sec/trial":
            sec_per_trial = 3
        else:
            raise Exception("Please select a difficulty")

        if selected_type == '1-BACK':
            num_back = 1
        elif selected_type == '2-BACK':
            num_back = 2
        elif selected_type == '3-BACK':
            num_back = 3
        else:
            raise Exception("Please select a type")

    except Exception as e:
        s.error_handler(db.nb_setup_frame, e, 6)

    try:
        # Step 4: Get rid of the setup screen and start the test
        db.nb_setup_frame.forget()
        check_label.grid_forget()
        prev_nums = []

        # Step 4b: Add an exit button
        Button(
            master=db.nback_frame,
            text="X",
            command=lambda: end_program(db.nback_frame),
            bg='#a60000',
            fg='white',
            activebackground='#d60000',
            activeforeground='white',
            font=db.DefaultFont
        ).grid(row=0, column=1, sticky=NE)

        num_trials = 0
        answer1, answer2 = question()
        default_time = time.time()
        start_time = round(time.time() - default_time, 2)
        db.timer = start_time

        # Step 5: Start writing test difficulty data to the save files
        if file is not None:
            file.write(selected_difficulty + ' ' + str(selected_type) + '\n')
            file.write("START,     Time Stamp: {}\n".format(start_time))
        print(selected_difficulty, selected_type)
        print("START,      Time Stamp: ", start_time)

        # Step 6: Add a timer
        label_t = Label(db.nback_frame, text='0.0', font=db.HeadingFont)
        label_t.grid(row=1, column=0, columnspan=3, pady=50)

        # Step 7: Start listening through microphone
        with db.microphone as source:
            db.recognizer.adjust_for_ambient_noise(source)

        stop_listening = db.recognizer.listen_in_background(db.microphone, submit)

        # Step 8: Create instructions label and base grid
        Label(db.nback_frame, text="Listening...", font=db.DefaultFont) \
            .grid(row=4, column=0, columnspan=3, pady=35)

        # Step 9: Display it all
        db.nback_frame.pack()

        # Step 10: Endlessly update timer
        while True:
            # put the timer value into the label
            label_t.config(text=str(db.timer))
            # wait for 0.1 seconds
            time.sleep(0.1)
            # needed with time.sleep()
            db.nback_frame.update()
            # update timer
            db.timer = round(time.time() - default_time, 2)

            if db.timer >= sec_per_trial:
                answer1, answer2 = question()

    except Exception as e:
        s.error_handler(db.nback_frame, e, 6, colspan=3, display=False)


def end_program(test_frame):
    global file, stop_listening, label_t
    if file is not None:
        file.close()
    if label_t is not None:
        label_t.destroy()
    s.exit_test(test_frame, callback_fun=stop_listening)


def setup():
    try:
        # Step 1: Add an exit button
        Button(
            master=db.nb_setup_frame,
            text="X",
            command=lambda: end_program(db.nb_setup_frame),
            bg='#a60000',
            fg='white',
            activebackground='#d60000',
            activeforeground='white',
            font=db.DefaultFont,
        ).grid(row=0, column=100, sticky=NE)

        # Step 2: Create Checkboxes for Test Type and Difficulty
        difficulties = ('7 sec/trial', '5 sec/trial', '3 sec/trial')
        types = ('1-BACK', '2-BACK', '3-BACK')
        db.grid_boxes = {}

        for index, name in enumerate(difficulties):
            # print(name, index)
            db.grid_boxes[name] = IntVar()
            Checkbutton(
                master=db.nb_setup_frame,
                text=difficulties[index],
                variable=db.grid_boxes[name],
                font=db.DefaultFont
            ).grid(row=2, column=index, sticky=W)

        for index, name in enumerate(types):
            # print(name, index)
            db.grid_boxes[name] = IntVar()
            Checkbutton(
                master=db.nb_setup_frame,
                text=types[index],
                variable=db.grid_boxes[name],
                font=db.DefaultFont
            ).grid(row=3, column=index, sticky=W)

        # Add some spacing below the checkboxes
        db.nb_setup_frame.grid_rowconfigure(4, weight=1, minsize=150)

        # Step 3: Add a 'Start' Button
        Button(
            master=db.nb_setup_frame,
            text="Start Test",
            command=start,
            activebackground="blue",
            activeforeground="white",
            bg="white",
            fg="black",
            font=db.DefaultFont,
        ).grid(row=4, columnspan=5, ipadx=200, pady=20)

    except Exception as e:
        s.error_handler(db.nb_setup_frame, e, 6)

    db.nb_setup_frame.pack()


if __name__ == '__main__':
    setup()
