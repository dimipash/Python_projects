"""
Simple Tkinter GUI demonstrating a message box.

Creates a window that immediately displays a yes/no message box
asking if the user likes coffee. Prints a response to the console
based on the user's selection.
"""

from tkinter import *
import tkinter.messagebox

root = Tk()

response = tkinter.messagebox.askquestion("Question1", "Do you like coffee?")
if response == "yes":
    print("Here is a coffee for you")
else:
    print("No")

root.mainloop()
