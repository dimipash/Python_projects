from tkinter import *


def selected():
    label.config(text=check_value.get())


root = Tk()
root.geometry("300x300")
check_value = BooleanVar()
checkbutton = Checkbutton(root, text="Accept terms", variable=check_value, command=selected)
checkbutton.pack()

label = Label(root)
label.pack()

root.mainloop()
