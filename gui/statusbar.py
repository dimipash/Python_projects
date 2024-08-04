"""
Tkinter GUI with menu bar and status bar.

Creates a window with:
1. A menu bar containing a 'File' menu with 'Project' and 'Save' options.
2. A status bar at the bottom of the window.

The menu options trigger a simple print statement when selected.
Demonstrates basic menu creation and status bar implementation.
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

status = Label(root, text="This is the current status", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

root.mainloop()
