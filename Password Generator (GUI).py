import random
from tkinter import *
from tkinter import messagebox
import pyperclip

available_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
password = ""
n = 0

# generates the password
def generate_password():
    global n, password
    password_length = int(input_box.get())
    output_box.delete(0, END)
    while n < password_length:
        password += random.choice(available_char)
        n += 1
    output_box.insert(10, password)

# check for conditions
def check_conditions():
    output = True
    if len(input_box.get()) > 2 or input_box.get() == '':
        output = False
    else:
        for char in input_box.get():
            if char.isdigit() == 0:
                output = False
                break
            else:
                output = True
    if output:
        generate_password()
    else:
        input_box.delete(0, END)
        messagebox.showerror(title="Error!", message="Not an acceptable value.\nPlease input an integer < 100.")

# clears input/output
def clear():
    input_box.delete(0, END)
    output_box.delete(0, END)

# copies output
def copy():
    if output_box.get() == '':
        messagebox.showerror(title="warning!", message="no output!")
    else:
        pyperclip.copy(output_box.get())


'''GUI elements'''

# create window
window = Tk()
window.title("Password Generator V1")
window.geometry("420x420")
window.resizable(False, False)

# containers (frames)
container_in = Frame(window)
container_in.place(x=134, y=180)
container_out = Frame(window)
container_out.place(x=134, y=210)
container_buttons = Frame(window)
container_buttons.place(x=134, y=245)

# text prompt
text = Label(window, text="Please enter password length: ")
text.place(x=135, y=150)

# input box and text
text = Label(container_in, text="Input: ")
text.pack(side=LEFT)
input_box = Entry(container_in, width=22)
input_box.pack(side=RIGHT)

# output box and text
text = Label(container_out, text="Output: ")
text.pack(side=LEFT)
output_box = Entry(container_out)
output_box.pack(side=RIGHT)

# buttons
submit_button = Button(container_buttons, text='submit', command=check_conditions)
submit_button.pack(side=LEFT)

copy_button = Button(container_buttons, text='copy', command=copy)
copy_button.pack(side=RIGHT)

clear_button = Button(container_buttons, text='clear', command=clear)
clear_button.pack()

window.mainloop()





