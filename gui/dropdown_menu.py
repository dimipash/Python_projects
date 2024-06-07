from tkinter import *


def function1():
    print("Menu Item Clicked")


root = Tk()
mymenu = Menu(root)

root.config(menu=mymenu)

submenu = Menu(mymenu)
mymenu.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Project", command=function1)
submenu.add_command(label="Save", command=function1)

root.mainloop()
