#!/usr/bin/env python3

"""calculator-tk.py at https://github.com/wilsonmar/python-samples/blob/main/calculator-tk.py
Provides a calculator created using the Tk library for Python.

gas "v003 + try :calculator-tk.py"
STATUS: Not working. Output env: python3\r: No such file or directory
   
Before running, in CLI run pip install tkinter
"""
import tkinter as tk

# Create Window
window = tk.Tk()
window.title("My First Calculator")
window.geometry("450x550")

# Holds the value for the input window
current_text = tk.StringVar(window)
current_text.set("0")


# Will contain properties and logic for calculation only
class Calculator:
    def __init__(self):
        self.last_number = 0
        self.current_operation = ""
        self.current_number = 0

    def set_operation(self, operation):
        self.current_operation = operation
        self.last_number = self.current_number
        self.current_number = 0

    def clear_all(self, text_box):
        self.current_operation = ""
        self.last_number = 0
        self.current_number = 0
        text_box.set("0")

    def set_number(self, num, text_box):
        new_num = str(self.current_number) + str(num)
        self.current_number = int(new_num)
        text_box.set(self.current_number)

    def calculate(self, text_box):
        match self.current_operation:
            case "+":
                self.last_number = self.last_number + self.current_number
            case "-":
                self.last_number = self.last_number - self.current_number
            case _:
                text_box.set("Error operation not found!")
                return

        text_box.set(self.last_number)


# We must instantiate a version of the class above
# in order to have our own usable copy of the class
calc = Calculator()

#Input window and Title
display_frame = tk.Frame(window)
tk.Label(display_frame, text="Python Calculator", font=("Georgia", 25), anchor=tk.CENTER).pack()
output = tk.Entry(display_frame, justify=tk.RIGHT, width=45, font=16, state="disabled", textvariable=current_text)
output.pack(pady=20)
display_frame.pack()

button_frame = tk.Frame(window)


# Function avoid duplicating the style information
def create_button(text, command=None):
    return tk.Button(button_frame, text=text, height=4, width=10, font=20, command=command)


# begin button grid
create_button("CE", command=lambda: calc.clear_all(current_text)).grid(row=0, column=2)
# create_button("/").grid(row=0, column=3)

# Second Row
create_button(7, command=lambda: calc.set_number(7, current_text)).grid(row=1, column=0)
create_button(8, command=lambda: calc.set_number(8, current_text)).grid(row=1, column=1)
create_button(9, command=lambda: calc.set_number(9, current_text)).grid(row=1, column=2)
# create_button("X").grid(row=1, column=3)

# Third Row
create_button(4, command=lambda: calc.set_number(4, current_text)).grid(row=2, column=0)
create_button(5, command=lambda: calc.set_number(5, current_text)).grid(row=2, column=1)
create_button(6, command=lambda: calc.set_number(6, current_text)).grid(row=2, column=2)
create_button("-", command=lambda: calc.set_operation("-"))\
    .grid(row=2, column=3)

# Fourth Row
create_button(1, command=lambda: calc.set_number(1, current_text)).grid(row=3, column=0)
create_button(2, command=lambda: calc.set_number(2, current_text)).grid(row=3, column=1)
create_button(3, command=lambda: calc.set_number(3, current_text)).grid(row=3, column=2)
create_button("+", command=lambda: calc.set_operation("+"))\
    .grid(row=3, column=3)

# Fifth Row
# create_button("+/-").grid(row=4, column=0)
create_button(0, command=lambda: calc.set_number(0, current_text)).grid(row=4, column=1)
# create_button(".").grid(row=4, column=2)
create_button("=", command=lambda: calc.calculate(current_text)).grid(row=4, column=3)

button_frame.pack()

# main loop to run tkInter GUI
tk.mainloop()
