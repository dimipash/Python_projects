"""
Simple GUI for text input and display.

Creates a Tkinter window with an entry field and a button.
When the button is clicked, the text from the entry field
is printed to the console.
"""

from tkinter import *


def display():
    data = entry.get()
    print(data)


root = Tk()
root.geometry("300x300")

entry = Entry(root)
entry.pack()


button = Button(root, text="Click Here", command=display)
button.pack()
root.mainloop()
