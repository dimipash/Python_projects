"""
Tkinter GUI demonstrating a 3x3 grid of buttons.

Creates a window with a 3x3 grid of frames, each containing a button.
Each button displays its row and column position.
Illustrates nested loops for GUI element creation and grid layout usage.
"""

from tkinter import *

root = Tk()

for x in range(3):
    for y in range(3):
        frame = Frame(root)
        frame.grid(row=x, column=y)
        button = Button(frame, text=f"Rox{x} \n Column{y}")
        button.pack(padx=5, pady=5)


root.mainloop()
