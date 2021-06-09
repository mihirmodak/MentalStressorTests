from tkinter import *
from tkinter import ttk
import variables as db
import settings as s
import speech_recognition as sr

db.calibration_frame = Frame(db.root)
db.calibration_setup = Frame(db.root)
# vals_to_record = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'red', 'green', 'yellow', 'blue', 'skip']
# vals_to_record = ['skip']
vals_to_record = []
stop_listening = None
prompt, heard, status = None, None, None

def question():
    global vals_to_record, prompt

    print(db.pronounce)

    db.errorLabel1.grid_forget()
    db.errorLabel2.grid_forget()

    key = vals_to_record[0]

    if prompt is None:
        prompt = Label(db.calibration_frame, text=f'{key}', font=db.HeadingFont)
    else:
        prompt.config(text=f"{key}")
    prompt.grid(row=2, column=0)
    vals_to_record.remove(key)

def submit(recognizer, audio):
    global heard, stop_listening
    try:
        try:
            heard.grid_forget()
        except:
            pass
        status.config(text = f"Thinking...")

        submitted = recognizer.recognize_google(audio, language=f'{db.set_lang}')

        if heard == None:
            heard = Label(db.calibration_frame, text=f"Recorded", font=db.DefaultFont)
        else:
            heard.config(text = f"Recorded")

        heard.grid(row=3, column=0)

        db.pronounce[prompt.cget('text')] = submitted
        print(f"{prompt.cget('text')} : {submitted}")

        if prompt.cget("text") == "skip":
            db.skip_keyword = submitted
            print(f"skip_keyword: {db.skip_keyword}")

        if not len(vals_to_record) == 0:
            question()
        else:
            s.exit_test(db.calibration_frame, stop_listening)

        # question()
    except Exception as e:
        s.error_handler(db.calibration_frame, e, 3)




def start():
    global stop_listening, status, vals_to_record

    # Step 1: Get the types of inputs to calibrate
    if db.calib_checks['NUMBERS'].get() == 1:
        vals_to_record += [i for i in range(10)]
    if db.calib_checks['COLORS'].get() == 1:
        vals_to_record += ['orange', 'yellow', 'blue', 'green']
    if db.calib_checks['SKIP'].get() == 1:
        vals_to_record.append('skip')

    # Step 2: Get the language
    print(f"Selected Language: {db.set_lang.get()}")
    print(f"Values: {vals_to_record}")
    #Step 3: Forget the setup frame
    db.calibration_setup.forget()

    #step 4: Start the calibration
    Button(
        master=db.calibration_frame,
        text="X",
        command=lambda: s.exit_test(db.calibration_frame, stop_listening),
        bg='#a60000',
        fg='white',
        activebackground='#d60000',
        activeforeground='white',
        font=db.SmallFont
    ).grid(row=0, column=1, sticky=N)
    Label(db.calibration_frame, text='Pronounce the following as clearly as possible:',
                         font=db.HeadingFont).grid(row=1)


    with db.microphone as source:
        db.recognizer.adjust_for_ambient_noise(source)

    stop_listening = db.recognizer.listen_in_background(source, submit)

    question()

    if status is None:
        status = Label(db.calibration_frame, text="Listening...", font=db.DefaultFont)
    else:
        status.config(text="Listening")
    status.grid(row=3, column=0)

    db.calibration_frame.pack()

def setup():
    try:
        Button(
            master=db.calibration_setup,
            text="X",
            command=lambda: s.exit_test(db.calibration_setup, None),
            bg='#a60000',
            fg='white',
            activebackground='#d60000',
            activeforeground='white',
            font=db.SmallFont
        ).grid(row=0, column=4, sticky=N)

        types = ('NUMBERS', 'COLORS', 'SKIP')
        db.calib_checks = {}
        for index, name in enumerate(types):
            # print(name, index)
            db.calib_checks[name] = IntVar()
            Checkbutton(
                master=db.calibration_setup,
                text=types[index],
                variable=db.calib_checks[name],
                font=db.DefaultFont
            ).grid(row=1, column=index, sticky=W)

        db.set_lang = StringVar()
        db.set_lang.set('English(US) - default')

        lang_options = list(db.languages.keys())

        lang = ttk.Combobox(master=db.calibration_setup, textvariable=db.set_lang,
                            values=lang_options, font=db.DefaultFont)
        lang.grid(row=2, columnspan=3, ipadx=200, pady=50)


        # Add some spacing below the exit button
        db.calibration_setup.grid_rowconfigure(3, weight=1, minsize=150)

        # Step 3: Add a 'Start' Button
        Button(
            master=db.calibration_setup,
            text="Start Test",
            command=start,
            activebackground="blue",
            activeforeground="white",
            bg="white",
            fg="black",
            font=db.DefaultFont,
        ).grid(row=4, columnspan=3, ipadx=200, pady=20)

    except Exception as e:
        s.error_handler(db.calibration_setup, e, 5)

    db.calibration_setup.pack()
