from tkinter import *

root = Tk()
frame = Frame(root, highlightthickness=1, highlightbackground="black", padx="20", pady="20")
frame.pack()

frame2 = Frame(root)
frame2.pack(side=BOTTOM)

button = Button(frame, text="Button1")
button2 = Button(frame2, text="Button2")

button.pack()
button2.pack()

root.geometry("300x300")


root.mainloop()