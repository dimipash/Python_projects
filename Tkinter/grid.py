from tkinter import *
root = Tk()

for x in range(3):
    for y in range(3):
        frame = Frame(root)
        frame.grid(row=x, column=y)
        button = Button(frame, text=f"Rox{x} \n Column{y}")
        button.pack(padx=5, pady=5)


root.mainloop()