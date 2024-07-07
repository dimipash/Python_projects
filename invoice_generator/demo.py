from tkinter import *

window = Tk()
window.title("Invoice Generator")

medicines = {"Aspirin": 15, "Ibuprofen": 20, "Paracetamol": 5, "Acetaminophen": 10}

invoice_items = []


def add_medicine():
    selected_medicine = medicine_listbox.get(ANCHOR)
    quantity = int(quantity_entry.get())
    price = medicines[selected_medicine]
    item_total = price * quantity
    invoice_items.append((selected_medicine, quantity, item_total))    
    update_invoice_text()

def update_invoice_text():
    invoice_text.delete(1.0, END)
    for item in invoice_items:
        invoice_text.insert(END, f"Medicine: {item[0]}, Quantity: {item[1]}, Total: {item[2]}\n")

medicine_label = Label(window, text="Medicine:")
medicine_label.pack()

medicine_listbox = Listbox(window, selectmode=SINGLE)
for medicine in medicines:
    medicine_listbox.insert(END, medicine)
medicine_listbox.pack()

quantity_label = Label(window, text="Quantity:")
quantity_label.pack()
quantity_entry = Entry(window)
quantity_entry.pack()

add_button = Button(window, text="Add Medicine", command=add_medicine)
add_button.pack()

total_amount_label = Label(window, text="Total Amount")
total_amount_label.pack()

total_amount_entry = Entry(window)
total_amount_entry.pack()

customer_label = Label(window, text="Customer Name:")
customer_label.pack()

customer_entry = Entry(window)
customer_entry.pack()

generate_button = Button(window, text="Generate Invoice")
generate_button.pack()

invoice_text = Text(window, width=40, height=40)
invoice_text.pack()

window.mainloop()
