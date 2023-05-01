import os.path
from tkinter import *
from tkinter import filedialog, colorchooser, font
import time

''' work in progress'''
def Help():
    try:
        file = open('\\help.txt')

    except:
        print("an error has occurred.")

def save_file():
    file = filedialog.asksaveasfile(initialdir='C:\\Users\\Lyric\\OneDrive\\Documents\\Python Program Text Files',
                             filetypes=[('text file', '*.txt'),('HTML file', '*.html')],
                             defaultextension='.txt')
    file_contents = text.get(1.0, END)
    file.write(file_contents)

def open_file():
    file = filedialog.askopenfilename(initialdir='C:\\Users\\Lyric\\OneDrive\\Documents\\Python Program Text Files',
                               filetypes=[("text files", "*.txt"),('HTML file', '*.html')])
    try:
        window.title(os.path.basename(file))
        with open(file) as file_contents:
            text.delete(1.0, END)
            text.insert(1.0, file_contents.read())
    except:
        pass

def Quit():
    print("program closed.")
    quit()

def change_font(*args):
    text.config(font=(font_style.get(),font_size.get()))

def open_font():
    global new_window

    # initialize new window
    new_window = Toplevel()
    new_window.geometry('200x150')

    Label(new_window, text='Customize your font: ').grid(row=0, column=0, columnspan=2)

    # Opens option menu for font styles
    Label(new_window, text='Font Style').grid(row=1, column=0, padx=5)

    font_selection = OptionMenu(new_window, font_style, *font.families(), command=change_font)
    font_selection.grid(row=1, column=1)

    # Creates selection box for font size
    Label(new_window, text='Font Size').grid(row=2, column=0)

    size_box = Spinbox(new_window, from_=1, to=100, textvariable=font_size, command=change_font, width=10)
    size_box.grid(row=2, column=1)

    Save_changes = Button(new_window, text='Save Changes', command=confirm_changes)
    Save_changes.grid(row=3, column=1)

    new_window.mainloop()

def confirm_changes():
    global label
    label = Label(new_window, text='Your changes have been saved!')
    label.grid(row=4, column=0, columnspan=2, pady=10)

def Change_Color():
    global new_window1, TextColor

    # initialize new window
    new_window1 = Toplevel()
    new_window1.geometry('300x100')
    new_window1.resizable(False, False)

    Label(new_window1, text='Customize your text and background color! ').grid(row=0, column=0, columnspan=3)

    # Text Color
    TextColor_Button = Button(new_window1, text="Text Color", command=Change_TextColor)
    TextColor_Button.grid(row=1, column=0)

    # Bg Color
    BGColor_Button = Button(new_window1, text="Background Color", command=Change_BGColor)
    BGColor_Button.grid(row=1, column=1)

    new_window1.mainloop()

def Change_TextColor():
    color = colorchooser.askcolor(title='pick a color!')
    text.config(fg=color[1])

def Change_BGColor():
    color = colorchooser.askcolor(title='pick a color!')
    text.config(bg=color[1])

''' Configurations '''

window = Tk()
window.geometry('420x420')
window.title('Notepad Program')
window.resizable(False, False)

# Temp Grid
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# creates menubar and attaches to window
menubar = Menu(window)
window.config(menu=menubar)

""" File menu """

# Adds file menu dropdown
File_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=File_menu)

SAVE = File_menu.add_command(label='Save', command=save_file)
OPEN = File_menu.add_command(label='Open', command=open_file)
QUIT = File_menu.add_command(label='Quit', command=Quit)

""" Customize menu """

# Adds customize menu dropdown
Customize_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Customize', menu=Customize_menu)

# Menu buttons
CHANGEFONT = Customize_menu.add_command(label='Font', command=open_font)
CHANGECOLOR = Customize_menu.add_command(label='Color', command=Change_Color)

''' Font '''

# font style variable
font_style = StringVar(window)
font_style.set("Arial")

# font size variable
font_size = IntVar(window)
font_size.set(12)

""" Help Menu """
Help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Info', menu=Help_menu)

HELP = Help_menu.add_command(label='Help', command=Help)

''' Scroll bar '''

pad_x = 10
pad_y = 10

text = Text(window, font=("Arial", 12), padx=pad_x, pady=pad_y)
text.grid(row=0, column=0, sticky=EW)

scroll_bar = Scrollbar(window, orient=VERTICAL, command=text.yview)
scroll_bar.grid(row=0, column=1, sticky=NS)

text['yscrollcommand'] = scroll_bar.set

window.mainloop()