from tkinter import *

window = Tk()
window.title("Invoice Generator")

medicine_label = Label(window, text="Medicine:")
medicine_label.pack()

medicine_listbox = Listbox(window, selectmode=SINGLE)
medicine_listbox.pack()

quantity_label = Label(window, text="Quantity:")
quantity_label.pack()
quantity_entry = Entry(window)
quantity_entry.pack()

add_button = Button(window, text="Add Medicine")
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

invoice_text = Text(window, width=10, height=50)
invoice_text.pack()

window.mainloop()
