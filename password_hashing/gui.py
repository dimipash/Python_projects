"""
Password Validation GUI with Bcrypt

This Python script creates a simple graphical user interface (GUI) using the Tkinter library. It allows the user to enter a password, and validates it against a pre-defined hashed password using the bcrypt library.

Features:
- GUI window with an entry field for password input
- "Validate" button to initiate password validation
- Prints "Login Successful" or "Login Failed" based on the validation result

Usage:
1. Run the script.
2. Enter the password in the provided entry field.
3. Click the "Validate" button.
4. The script will print the validation result in the console.

"""

from tkinter import *
import bcrypt

def validate(password):
    hash = b'$2b$12$KnephikAS89GXFe74SvMReT9GLZYKVhPC2CiS3xyxPWdLzff/2gLm'
    password = bytes(password, encoding='utf-8')
    if bcrypt.checkpw(password, hash):
        print('Login Successful')
    else:
        print('Login Failed')


root = Tk()
root.geometry("300x300")

password_entry = Entry(root)
password_entry.pack()

button = Button(text="validate", command=lambda: validate(password_entry.get()))
button.pack()
root.mainloop()