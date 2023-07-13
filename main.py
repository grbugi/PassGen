# import neccessery Python Modules
import configparser
import clipboard
import errno
import os
import random
import re
import string
import subprocess
import sys
from configparser import ConfigParser
from random import choice
from time import strftime
from tkinter import *
from tkinter import messagebox
from tktooltip import ToolTip

StartTime = strftime('%d %b %Y %H-%M-%S')
version = '1.5'
Progname = 'Password Genegator v' + version
Bottomline = Progname + ' by grBUGi'

LogFileName = 'Password Generator/Log ' + StartTime + '.txt'
configpath = 'Password Generator/Configuration.ini'

bitmapico = "bitmap.ico"
#if not hasattr(sys, "frozen"):  # not packed
#    bitmapico = os.path.join(os.path.dirname(__file__), bitmapico)
#else:
#    bitmapico = os.path.join(sys.prefix, bitmapico)

if not os.path.exists(os.path.dirname(LogFileName)):
    try:
        os.makedirs(os.path.dirname(LogFileName))
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

with open(LogFileName, "a+") as f:
    LogFile = open(LogFileName, "a+")
    LogFile.write("\nProgram start at\t" + StartTime + '\n\n')
    LogFile.close()

root = Tk()
root.resizable(False, False)
root.title(Progname)
root.iconbitmap(bitmapico)

#root.iconbitmap(default=bitmapico)

# Variables
password = StringVar()
GeneratedPassword = StringVar()
N = StringVar()
LettersLow = BooleanVar()
LettersUp = BooleanVar()
Numbers = BooleanVar()
Symbols = BooleanVar()
ExclSame = BooleanVar()
ExclDots = BooleanVar()
ExclBrk = BooleanVar()
LastChar = StringVar()
LastCharSw = BooleanVar()
LastCharCal = IntVar()
charsLow = StringVar()
charsUp = StringVar()
charsNum = StringVar()
charsSym = StringVar()


# Create config file
def createConfig(configpath):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "Number", "8")
    config.set("Settings", "Lower case letters", "True")
    config.set("Settings", "Upper case letters", "True")
    config.set("Settings", "Numbers", "True")
    config.set("Settings", "Symbols", "True")
    config.set("Settings", "Exclude Similar", "True")
    config.set("Settings", "Exclude Dots", "True")
    config.set("Settings", "Exclude Brackets", "True")
    config.set("Settings", "Last Charter is Letter", "True")
    with open(configpath, "w") as config_file:
        config.write(config_file)


# Load config file
def loadConfig(configpath):
    if not os.path.exists(configpath):
        createConfig(configpath)
    config: ConfigParser = configparser.ConfigParser()
    config.read(configpath)
    N.set(config.get("Settings", "Number"))
    LettersLow.set(bool(config.get("Settings", "Lower case letters")))
    LettersUp.set(bool(config.get("Settings", "Upper case letters")))
    Numbers.set(bool(config.get("Settings", "Numbers")))
    Symbols.set(bool(config.get("Settings", "Symbols")))
    ExclSame.set(bool(config.get("Settings", "Exclude Similar")))
    ExclDots.set(bool(config.get("Settings", "Exclude Dots")))
    ExclBrk.set(bool(config.get("Settings", "Exclude Brackets")))
    LastCharSw.set(bool(config.get("Settings", "Last Charter is Letter")))

#Check config file and if exist, than auto load
if __name__ == "__main__":
    loadConfig(configpath)


#Autosave config
def saveConfig(configpath):
    config = configparser.ConfigParser()
    config.read(configpath)
    config.set("Settings", "Number", N.get())
    config.set("Settings", "Lower case letters", str(LettersLow.get()))
    config.set("Settings", "Upper case letters", str(LettersUp.get()))
    config.set("Settings", "Numbers", str(Numbers.get()))
    config.set("Settings", "Symbols", str(Symbols.get()))
    config.set("Settings", "Exclude Similar", str(ExclSame.get()))
    config.set("Settings", "Exclude Dots", str(ExclDots.get()))
    config.set("Settings", "Exclude Brackets", str(ExclBrk.get()))
    config.set("Settings", "Last Charter is Letter", str(LastCharSw.get()))

    with open(configpath, "w") as config_file: config.write(config_file)


def generate(*args):
    global password

    # Check and correct N

    if GeneratedPassword.get() != password.get(): N.set(len(password.get()))

    try:
        N.set(N.get()[0:3])
        if int(N.get()) > 128: N.set(256)
        if int(N.get()) < 1: N.set(1)
    except ValueError:
        N.set(len(N.get()))

    Number = int(N.get())

    # Set arrays of chars
    charsLow = ""
    charsUp = ""
    charsNum = ""
    charsSym = ""
    LastChar = ""

    # Checking reqirements
    if LettersLow.get() == 1:
        charsLow = charsLow + string.ascii_lowercase
        LastChar = LastChar + string.ascii_lowercase

    if LettersUp.get() == 1:
        charsUp = charsUp + string.ascii_uppercase
        LastChar = LastChar + string.ascii_uppercase

    if Numbers.get() == 1:
        charsNum = charsNum + string.digits

    if Symbols.get() == 1:
        charsSym = charsSym + string.punctuation

    if ExclSame.get() == 1:
        charsLow = re.sub('[oO0lI|]', "", charsLow)
        charsUp = re.sub('[oO0lI|]', "", charsUp)
        charsNum = re.sub('[oO0lI|]', "", charsNum)
        charsSym = re.sub('[oO0lI|]', "", charsSym)
        LastChar = re.sub('[oOlI]', '', LastChar)

    if ExclDots.get() == 1:
        charsSym = re.sub('[.,:;`_? ]', "", charsSym)
    if ExclBrk.get() == 1:
        charsSym = re.sub('[/[\]{}()\|<>]', "", charsSym)

    if LastCharSw.get() == 1:
        LastCharCal = int(1)
        LastChar = choice(LastChar)
    else:
        LastCharCal = int(0)
        LastChar = ""

    Number = Number - LastCharCal

    # Set lists of parts of password
    passwordLow = []
    passwordUp = []
    passwordNum = []
    passwordSym = []
    passwordSUM1 = []
    passwordSUM2 = []

    # Password generation
    for i in range(Number):
        passwordSUM1 = []
        if len(charsLow) > 0:
            passwordLow.extend(choice(charsLow))
            passwordSUM1.extend([passwordLow[i]])
        if len(charsUp) > 0:
            passwordUp.extend(choice(charsUp))
            passwordSUM1.extend([passwordUp[i]])
        if len(charsNum) > 0:
            passwordNum.extend(choice(charsNum))
            passwordSUM1.extend([passwordNum[i]])
        if len(charsSym) > 0:
            passwordSym.extend(choice(charsSym))
            passwordSUM1.extend([passwordSym[i]])

        random.SystemRandom().shuffle(passwordSUM1)
        passwordSUM2.extend(passwordSUM1)

    password.set("".join(passwordSUM2[0:Number]) + LastChar)

    LogFile = open(LogFileName, "a+")
    LogFile.write(strftime('%H:%M:%S') + "\t\t" + password.get() + '\n')
    LogFile.close()
    clipboard.copy(password.get())
    GeneratedPassword.set(password.get())
    saveConfig(configpath)

#Copy to clipboard
def copypass(*args):
    clipboard.copy(password.get())
    if GeneratedPassword.get() != password.get():
        N.set(len(password.get()))
        LogFile = open(LogFileName, "a+")
        LogFile.write(strftime('%H:%M:%S') + "\t\t" + password.get() + '\n')
        LogFile.close()

#Open Log file
def openlogfile(*args):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', LogFileName))
    elif os.name == 'nt':  # For Windows
        os.startfile(LogFileName)
    elif os.name == 'posix':  # For Linux, Mac, etc.
        subprocess.call(('gnome-open', LogFileName))

#"About" window
def about(*args):
    messagebox.showinfo(
        'About Password Generator',
        'Enter number of characters.'
        '\nSelect the required options for include or exlude the characters:'
        '\n\ta..z\t- Lowercase letters'
        '\n\tA..Z\t- Uppercase Letters'
        '\n\t0..9\t- Numbers'
        '\n\t!@#$\t- Symbols'
        '\n\toO0lI1|\t- Similar characters'
        '\n\t.,_:;\'\"`?\t- Dots-like symbols and ?'
        '\n\t\/()[]{}<>|\t- Brackets'
        '\n\tExcel\t- Replace last character for letter (for slove Excel\'s issues)'
        '\n\nClick on "Generate" button or hit "Enter" or "Return" on your keyboard.'
        '\nAfter generation, the password will be automatically copied to your clipboard.'
        '\nYou can edit generated password and copy it with "Copy" button or with Ctrl+C. PassGen will count the numer of charters in your password. Take a note, Password Generator copying whole password everytime.'
        '\nThe Password Generator keeps logs. You can open the log file by clicking on the appropriate button or with Ctrl+L.'
        ' You can find the log files and configuration file in "Password Generator" folder near executable file of the application')

# GUI Programming
EmptyLineLabel = Label(root, text="",font='Courier 12')

EntryNumber = Spinbox(root, from_=1, to=128, justify=CENTER, relief=FLAT, width=4, textvariable=N, font=('Courier 11'))
EntryNumberLabel = Label(root, text='Number of characters:', pady=5, padx=4, font=('Courier 11'))
LettersLowBox = Checkbutton(root, text="a..z", variable=LettersLow, onvalue=True, offvalue=False, font=('Courier 11'))
ToolTip(LettersLowBox, msg='Lowercase letters')
LettersUpBox = Checkbutton(root, text="A..Z", variable=LettersUp, onvalue=True, offvalue=False, font=('Courier 11'))
ToolTip(LettersUpBox, msg='Uppercase Letters')
NumbersBox = Checkbutton(root, text="0..9", variable=Numbers, onvalue=True, offvalue=False, font=('Courier 11'))
ToolTip(NumbersBox, msg='Numbers')
SymbolsBox = Checkbutton(root, text="!@#$", variable=Symbols, onvalue=True, offvalue=False, font=('Courier 11'))
ToolTip(SymbolsBox, msg='Symbols')
ExclSameBox = Checkbutton(root, justify=LEFT, text="oO0lI|", variable=ExclSame, onvalue=False, offvalue=True,
                          font=('Courier 11'))
ToolTip(ExclSameBox, msg='Similar characters')
ExclDotsBox = Checkbutton(root, justify=LEFT, text=".,_:;'\"`?", variable=ExclDots, onvalue=False, offvalue=True,
                          font=('Courier 11'))
ToolTip(ExclDotsBox, msg='Dots-like symbols and ?')
ExclBrkBox = Checkbutton(root, justify=LEFT, text="\/()[]{}<>|", variable=ExclBrk, onvalue=False, offvalue=True,
                         font=('Courier 11'))
ToolTip(ExclBrkBox, msg='Brackets')
LastCharBox = Checkbutton(root, justify=LEFT, text="Excel", variable=LastCharSw, onvalue=True, offvalue=False,
                          font=('Times 11 italic'))
ToolTip(LastCharBox, msg='Replace last character for letter (for slove Excel\'s issues)')
PasswordResult = Entry(root, justify=CENTER, width=34, font=('System 12'), relief=FLAT, text=password.get(), textvariable=password)
GenerateButton = Button(root, text='Generate', width=18, relief=GROOVE, command=generate, font=('bold'), height=2)
CopyButton = Button(root, text='Copy', width=2, relief=GROOVE, command=copypass)
LogButton = Button(root, text='Log...', width=2, relief=GROOVE, command=openlogfile)

AboutButton = Button(root, text='?', width=1, relief=GROOVE, command=about)
CopyrightLabel = Label(root, text=Bottomline, pady=5, padx=4, font='Courier 8')

# Grid layout
toprow = 0
EntryNumberLabel.grid(row=toprow+1, columnspan=2, pady=16)
EntryNumber.grid(row=toprow+1, column=2, sticky=W)
AboutButton.grid(row=toprow+1, column=3, sticky=E)

centerrow = toprow + 2
LettersLowBox.grid(row=centerrow, column=0, columnspan=2, sticky=W)
LettersUpBox.grid(row=centerrow+1, column=0, columnspan=2, sticky=W)
NumbersBox.grid(row=centerrow+2, column=0, columnspan=2, sticky=W)
SymbolsBox.grid(row=centerrow+3, column=0, columnspan=2, sticky=W)
ExclSameBox.grid(row=centerrow, column=2, columnspan=2, sticky=W)
ExclDotsBox.grid(row=centerrow+1, column=2, columnspan=2, sticky=W)
ExclBrkBox.grid(row=centerrow+2, column=2, columnspan=2, sticky=W)
LastCharBox.grid(row=centerrow+3, column=2, columnspan=2, sticky=W)
PasswordResult.grid(row=centerrow+5, columnspan=4, pady=16)

bottomrow =centerrow + 6
GenerateButton.grid(row=bottomrow, column=0, columnspan=3, rowspan=2)
CopyButton.grid(row=bottomrow, column=3, sticky=S)
LogButton.grid(row=bottomrow+1, column=3)


CopyrightLabel.grid(row=14, columnspan=4)
EntryNumber.focus()


def close(event):
    root.withdraw()  # if you want to bring it back
    sys.exit()  # if you want to exit the entire thing


# End
root.bind('<Return>', generate)
root.bind('<Escape>', close)
root.bind('<F1>', about)
root.bind('<Control_L>' + '<l>', openlogfile)
root.bind('<Control_L>' + '<c>', copypass)
root.mainloop()