# Invoice Generator

This is a simple invoice generator application built with Python and Tkinter. It allows users to create invoices for medicine purchases and generate PDF invoices.

## Features

- Select medicines from a predefined list
- Add multiple items to the invoice
- Calculate total amount automatically
- Generate PDF invoices
- Simple and intuitive GUI

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- fpdf library

## Installation

1. Clone this repository.

2. Navigate to the project directory.

3. Install the required packages:
   ```
   pip install fpdf
   ```

## Usage

1. Run the script:

   ```
   python invoice_generator.py
   ```

2. Use the GUI to:

   - Select a medicine from the list
   - Enter the quantity
   - Click "Add Medicine" to add it to the invoice
   - Enter customer name
   - Click "Generate Invoice" to create a PDF invoice

3. The generated PDF will be saved as "invoice.pdf" in the same directory.

## Customization

You can easily customize the list of medicines and their prices by modifying the `medicines` dictionary in the script:

```python
medicines = {"Aspirin": 15, "Ibuprofen": 20, "Paracetamol": 5, "Acetaminophen": 10}
```
