![Student Database Management System](https://github.com/dimipash/Python_projects/blob/main/database_app/screenshot.jpg)

# Student Management System

## Description

This Student Management System is a Python-based application designed to manage student records in a PostgreSQL database. It provides both a graphical user interface (GUI) and a command-line interface (CLI) for interacting with the student database.

## Features

- Create a new student table in the database
- Insert new student records
- View all student records
- Update existing student information
- Delete student records
- User-friendly GUI built with Tkinter
- Command-line interface for quick operations

## Requirements

- Python 3.x
- PostgreSQL
- psycopg2 library
- Tkinter (usually comes pre-installed with Python)

## Installation

1. Clone this repository
2. Install the required Python library:
   ```
   pip install psycopg2
   ```
3. Ensure you have PostgreSQL installed and running on your system.

## Configuration

Before running the application, you need to set up your database connection. Modify the following lines in both `students_gui.py` and `students_menu.py`:

```python
dbname="studentdb",
user="postgres",
password="your_password",
host="localhost",
port="5432"
```

Replace `"your_password"` with your actual PostgreSQL password.

## Usage

### GUI Version

To run the graphical user interface:

```
python students_gui.py
```

The GUI provides buttons for all CRUD operations and displays student records in a table view.

### CLI Version

To run the command-line interface:

```
python students_menu.py
```

Follow the on-screen prompts to perform various operations on the student database.

## File Structure

- `students_gui.py`: Contains the graphical user interface implementation
- `students_menu.py`: Implements the command-line interface
