"""
A Student Management System application with a graphical user interface (GUI) built using Tkinter.

This application allows users to manage student records in a PostgreSQL database. It provides an intuitive GUI with various functionalities such as creating a table, inserting new student data, updating existing data, deleting records, and displaying all student records in a treeview.

Features:
- Create a table in the PostgreSQL database for storing student data
- Insert new student records with name, address, age, and phone number
- Update existing student records by selecting a record from the treeview
- Delete student records by selecting a record from the treeview
- Display all student records in a treeview with scrolling functionality
- User-friendly interface with input fields and buttons for CRUD operations
- Error handling and messaging for database operations

Requirements:
- Python
- Tkinter (Python's standard GUI library)
- psycopg2 (PostgreSQL database adapter for Python)
- A running instance of PostgreSQL database server

Note: This application requires the 'psycopg2' library to be installed for interacting with the PostgreSQL database.
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

def run_query(query, parameters=()):
    con = psycopg2.connect(dbname="studentdb", user="postgres", password="parolata22", host="localhost", port="5432")
    cur = con.cursor()
    query_result = None
    try:
        cur.execute(query, parameters)
        if query.lower().startswith("select"):
            query_result = cur.fetchall()
        con.commit()
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        cur.close()
        con.close()
    return query_result

def refresh_treeview():
    for item in tree.get_children():
        tree.delete(item)
    records = run_query("select * from students;")
    for record in records:
        tree.insert('', END, values=record)


def insert_data():
    query = "insert into students(name, address, age, number) values (%s, %s, %s, %s)"
    parameters = (name_entry.get(), address_entry.get(), age_entry.get(), phone_entry.get())
    run_query(query, parameters)
    messagebox.showinfo("Information", "Data inserted ")
    refresh_treeview()

def delete_data():
    selected_item = tree.selection()[0]    
    student_id = tree.item(selected_item)['values'][0]
    query = "delete from students where student_id=%s"
    parameters = (student_id,)
    run_query(query, parameters)
    messagebox.showinfo("Information", "Data deleted successfully")
    refresh_treeview()

def update_data():
    selected_item = tree.selection()[0]    
    student_id = tree.item(selected_item)['values'][0]
    query = "update students set name=%s, address=%s, age=%s, number=%s where student_id=%s"
    parameters = (name_entry.get(), address_entry.get(), age_entry.get(), phone_entry.get(), student_id)
    run_query(query, parameters)
    messagebox.showinfo("Information", "Data updated successfully")
    refresh_treeview()

def create_table():
    query = "create table if not exists students(student_id serial primary key, name text, address text, age int, number text);"
    run_query(query)
    messagebox.showinfo("Information", "Table created successfully")
    refresh_treeview()

root = Tk()
root.title("Student management system")

frame = LabelFrame(root, text="Student Data")
frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")


Label(frame, text="Name: ").grid(row=0, column=0, padx=2, sticky="w")
name_entry = Entry(frame)
name_entry.grid(row=0, column=1, pady=2, sticky="ew")

Label(frame, text="Address: ").grid(row=1, column=0, padx=2, sticky="w")
address_entry = Entry(frame)
address_entry.grid(row=1, column=1, pady=2, sticky="ew")

Label(frame, text="Age: ").grid(row=2, column=0, padx=2, sticky="w")
age_entry = Entry(frame)
age_entry.grid(row=2, column=1, pady=2, sticky="ew")

Label(frame, text="Phone Number: ").grid(row=3, column=0, padx=2, sticky="w")
phone_entry = Entry(frame)
phone_entry.grid(row=3, column=1, pady=2, sticky="ew")


button_frame = Frame(root)
button_frame.grid(row=1, column=0, pady=5, sticky="ew")

Button(button_frame, text="Create Table", command=create_table).grid(row=0, column=0, padx=5)
Button(button_frame, text="Add Data", command=insert_data).grid(row=0, column=1, padx=5)
Button(button_frame, text="Update Data", command=update_data).grid(row=0, column=2, padx=5)
Button(button_frame, text="Delete Data", command=delete_data).grid(row=0, column=3, padx=5)


tree_frame = Frame(root)
tree_frame.grid(row=2, column=0, padx=10, sticky="nsew")

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
tree.pack()
tree_scroll.config(command=tree.yview)

tree['columns'] = ("student_id", "name", "address", "age", "number")
tree.column("#0", width=0, stretch=NO)
tree.column('student_id', anchor=CENTER, width=80)
tree.column('name', anchor=CENTER, width=120)
tree.column('address', anchor=CENTER, width=120)
tree.column('age', anchor=CENTER, width=50)
tree.column('number', anchor=CENTER, width=120)

tree.heading("student_id", text="ID", anchor=CENTER)
tree.heading("name", text="name", anchor=CENTER)
tree.heading("address", text="address", anchor=CENTER)
tree.heading("age", text="age", anchor=CENTER)
tree.heading("number", text="number", anchor=CENTER)


refresh_treeview()

root.mainloop()