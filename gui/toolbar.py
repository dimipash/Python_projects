from tkinter import *


def function1():
    print("Menu Item Clicked")


root = Tk()
mymenu = Menu(root)

root.config(menu=mymenu)

submenu = Menu(mymenu)

submenu.add_command(label="Project", command=function1)
submenu.add_command(label="Save", command=function1)

status = Label(root, text="This is the current status", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

toolbar = Frame(root, bg='green')
insertbutton = Button(toolbar, text="Insert Files", command=function1)
deletebutton = Button(toolbar, text="Delete Files", command=function1)

insertbutton.pack(side=LEFT, padx=2, pady=3)
deletebutton.pack(side=LEFT, padx=2, pady=3)

toolbar.pack()

root.mainloop()
