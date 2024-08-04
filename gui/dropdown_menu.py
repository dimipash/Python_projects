"""
Basic Tkinter GUI with a menu bar.

Creates a window with a menu bar containing a 'File' menu.
The 'File' menu includes 'Project' and 'Save' options, both
of which trigger a simple print statement when selected.
"""

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
