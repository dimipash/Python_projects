from tkinter import *
import tkinter.messagebox
root = Tk()

response = tkinter.messagebox.askquestion("Question1", "Do you like coffee?")
if response == 'yes':
    print("Here is a coffee for you")
else:
    print("No")

root.mainloop()