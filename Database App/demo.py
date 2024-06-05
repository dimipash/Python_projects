import psycopg2

def create_table():
    con = psycopg2.connect(dbname="studentdb", user="postgres", password="parolata22", host="localhost", port="5432")
    cur = con.cursor()
    cur.execute("create table students(student_id serial primary key, name text, address text, age int, number text);")
    print("Student table created")
    con.commit()
    con.close()

def insert_data():
    name = input("Enter name: ")
    address = input("Enter address: ")
    age = input("Enter age: ")
    number = input("Enter number: ")
    con = psycopg2.connect(dbname="studentdb", user="postgres", password="parolata22", host="localhost", port="5432")
    cur = con.cursor()
    cur.execute("insert into students(name, address, age, number) values (%s, %s, %s, %s)", (name, address, age, number))
    print("data added in student table")
    con.commit()
    con.close()

def delete_data():
    student_id = input("Enter the id of the student to be deleted: ")
    con = psycopg2.connect(dbname="studentdb", user="postgres", password="parolata22", host="localhost", port="5432")
    cur = con.cursor()
    
    cur.execute("select * from students where student_id=%s", (student_id,))
    student = cur.fetchone()

    if student:
        print(f"Student to be deleted: ID: {student[0]}, Name: {student[1]}, Address: {student[2]}, Age: {student[3]}")
        choice = input("Are you sure you want to delete the student? (yes/no)")
        if choice.lower() == "yes":
            cur.execute("delete from students where student_id=%s", (student_id,))
            print("Student deleted successfully")
        else:
            print("Student not deleted")
    else:
        print("Student not found")

    con.commit()
    con.close()

def update_data():
    student_id = input("Enter the id of the student to be updated: ")
    con = psycopg2.connect(dbname="studentdb", user="postgres", password="parolata22", host="localhost", port="5432")
    cur = con.cursor()
    fields = {
        "1": ("name", "Enter the new name"),
        "2": ("address", "Enter the new address"),
        "3": ("age", "Enter the new age"),
        "4": ("number", "Enter the new number")
    }
    print("Which field you like to update?")
    for key in fields:
        print(f"{key}: {fields[key][0]}")   
    field_choice = input("Enter the number of the field you want to update: ")

    if field_choice in fields:
        field_name, promt = fields[field_choice]        
        new_value = input(promt)
        sql = f"update students set {field_name}= %s where student_id=%s"
        cur.execute(sql, (new_value, student_id))
        print(f"{field_name} updated successfully")
    else:
        print("Invalid choice")


    
    
    con.commit()
    con.close()

def read_data():
    con = psycopg2.connect(dbname="studentdb", user="postgres", password="parolata22", host="localhost", port="5432")
    cur = con.cursor()
    cur.execute("select * from students;")
    students = cur.fetchall()    
    for student in students:
        print(f"ID: {student[0]}, Name: {student[1]}, Address: {student[2]}, Age: {student[3]}, Number: {student[4]}")    
    con.close()


while True:
    print("\n Welcome to the student database management system")
    print("1. Create Table")
    print("2. Insert Data")
    print("3. Read Data")
    print("4. Update Data")
    print("5. Delete Data")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ")
    if choice == "1":
        create_table()
    elif choice == "2":
        insert_data()
    elif choice == "3":
        read_data()
    elif choice == "4":
        update_data()
    elif choice == "5":
        delete_data()
    elif choice == "6":
        break
    else:
        print("Invalid choice")
