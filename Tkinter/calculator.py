from tkinter import *

root = Tk()
display = Entry(root)
display.grid(row=1, columnspan=6)

counter =1
for x in range(3):
    for y in range(3):
        button = Button(root, text=counter, width=4, height=2)
        button.grid(row=x+2, column=y)
        counter += 1

button = Button(root, text="0", width=4, height=2)
button.grid(row=5, column=1)
root.mainloop()
