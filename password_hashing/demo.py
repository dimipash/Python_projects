"""
Password Hashing with Bcrypt

This Python script demonstrates how to hash a password using the bcrypt library and how to verify a user-entered password against the hashed password.

Usage:
1. Run the script.
2. Enter the password when prompted.
3. The script will print 'Login Successful' if the entered password matches the hashed password, or 'Login Failed' otherwise.

"""

import bcrypt

password = b"thisismypassword"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed)

entered_password = input('Enter password to login: ')
entered_password = bytes(entered_password, encoding='utf-8')

if bcrypt.checkpw(entered_password, hashed):
    print('Login Successful')
else:
    print('Login Failed')
