import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern Calculator")
        self.geometry("300x450")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.entry = ctk.CTkEntry(self.frame, height=50, font=("Arial", 20), justify="right")
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            ctk.CTkButton(self.frame, text=button, command=cmd, width=50, height=50, font=("Arial", 18)).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

        ctk.CTkButton(self.frame, text="Clear", command=self.clear, width=230, height=50, font=("Arial", 18)).grid(row=row, column=0, columnspan=4, padx=5, pady=5)

    def click(self, key):
        if key == '=':
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except:
                messagebox.showerror("Error", "Invalid Input")
                self.entry.delete(0, tk.END)
        else:
            self.entry.insert(tk.END, key)

    def clear(self):
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()