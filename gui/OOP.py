"""
Tkinter GUI demonstrating object-oriented programming.

Creates a window with two buttons:
1. 'Click Here': Prints a message to the console when clicked.
2. 'Exit': Closes the application.

Uses a class-based approach to organize GUI elements and their functionalities.
"""

from tkinter import *


class Demo:
    def __init__(self, rootone):
        frame = Frame(rootone)
        frame.pack()

        self.printbutton = Button(frame, text="Click Here", command=self.printmessage)
        self.printbutton.pack()

        self.quitbutton = Button(frame, text="Exit", command=frame.quit)
        self.quitbutton.pack()

    def printmessage(self):
        print("Button Clicked")


root = Tk()
b = Demo(root)
root.mainloop()
