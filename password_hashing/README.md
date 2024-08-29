# Password Hashing Project

This project demonstrates the implementation of password hashing using bcrypt in Python. It includes both a command-line interface and a graphical user interface for password validation.

## Project Structure

The project consists of two main Python files:

1. `demo.py`: A command-line interface for password hashing and validation.
2. `gui.py`: A graphical user interface for password validation using Tkinter.

## Requirements

- Python 3.x
- bcrypt library
- Tkinter (usually comes pre-installed with Python)

To install the required bcrypt library, run:

```
pip install bcrypt
```

## Usage

### Command-line Interface (demo.py)

1. Run the script:
   ```
   python demo.py
   ```
2. The script will generate a hashed password and prompt you to enter a password for validation.
3. Enter the password when prompted.
4. The script will display whether the login was successful or failed.

### Graphical User Interface (gui.py)

1. Run the script:
   ```
   python gui.py
   ```
2. A window will appear with a text entry field and a "validate" button.
3. Enter a password in the text field.
4. Click the "validate" button.
5. The result of the validation will be printed to the console.

## Security Note

This project is for demonstration purposes only. In a real-world application, you should never store hashed passwords in your code. Instead, store them securely in a database and retrieve them when needed for validation.
