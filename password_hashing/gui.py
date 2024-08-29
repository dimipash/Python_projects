from tkinter import *
import bcrypt


def validate(password):
    hash = b"$2b$12$KnephikAS89GXFe74SvMReT9GLZYKVhPC2CiS3xyxPWdLzff/2gLm"
    password = bytes(password, encoding="utf-8")
    if bcrypt.checkpw(password, hash):
        print("Login Successful")
    else:
        print("Login Failed")


root = Tk()
root.geometry("300x300")

password_entry = Entry(root)
password_entry.pack()

button = Button(text="validate", command=lambda: validate(password_entry.get()))
button.pack()
root.mainloop()
