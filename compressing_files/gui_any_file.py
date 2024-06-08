import tkinter as tk
from tkinter import filedialog
from compress_module import compress, decompress

def compression():
    input_file = filedialog.askopenfilename()
    output_file = output_entry.get()
    if input_file and output_file:
        compress(input_file, output_file)

def decompression():
    input_file = filedialog.askopenfilename()
    output_file = output_entry.get()
    if input_file and output_file:
        decompress(input_file, output_file)

window = tk.Tk()
window.title("Compression and Decompression Engine")
window.geometry("600x400")

output_entry = tk.Entry(window)
output_label = tk.Label(window, text="Name of the compressed/decompressed file")

compress_button = tk.Button(window, text="Compress", command=compression)
decompress_button = tk.Button(window, text="Decompress", command=decompression)

output_label.grid(row=0, column=0)
output_entry.grid(row=0, column=1)
compress_button.grid(row=1, column=0)
decompress_button.grid(row=1, column=1)

window.mainloop()