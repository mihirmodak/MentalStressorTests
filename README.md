# Stress Test GUI Documentation

## Description

This GUI is intended to be used to conduct cognitive stress tests. The GUI contains some cognitive stress tasks designed
 to induce stress in a subject performing that task.

The GUI was developed in Python using the Tkinter library, and was exported to an executable file using the PyInstaller 
tool.

## Installation

There is no installer needed for this program. The executable `.exe` file is located in the `dist` folder. The test data from the GUI is saved in a `saves` folder located within the same `dist` folder. 

To use the program, you can either download the code as a .zip file (using the green button above) or run the following command:
```
git clone https://github.com/mihirmodak/stress_test.git
```
from the command line to copy all the code files to your computer. You will need to have `git` installed for the latter option to work.

#### WARNING:
This GUI was compiled using Python 3.9, which does not support Windows 7. To install on Windows 7, download all the code in this repository and run `convert.bat` (Windows) or `convert.sh` (Linux/MacOS). This will compile the GUI using your local version of Python. It requires the [PyInstaller](https://pypi.org/project/pyinstaller/) package which can be installed using the command

```
pip install pyinstaller 
```
#### MAKE SURE THAT YOU HAVE ALL THE DEPENDENCIES INSTALLED BEFORE RUNNING THE `CONVERT.BAT` FILE. 

## Dependencies:

- Numpy
- Tkinter
- PyAudio
- SpeechRecognition
- More (To Be Updated Later)

## Use

See [DetailedGuide.md](DetailedGuide.md) for an in-depth walkthrough of this program.
