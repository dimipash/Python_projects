import os
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import PyPDF2
import anthropic
import json
from dotenv import load_dotenv


class ClaudePDFSummarizer:
    def __init__(self):
        self.pdf_path = None
        self.text = ""
        self.summary = ""
        self.summary_ratio = 0.25

        load_dotenv()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-sonnet-20240229"

    def extract_text(self, progress_callback=None):
        if not self.pdf_path or not os.path.exists(self.pdf_path):
            raise ValueError("Please select a valid PDF file")

        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)

                if num_pages == 0:
                    raise ValueError("The PDF file is empty")

                text = ""
                for i, page in enumerate(reader.pages):
                    text += page.extract_text() + "\n"
                    if progress_callback:
                        progress_callback(int((i + 1) / num_pages * 50))

                text = re.sub(r'\s+', ' ', text).strip()
                self.text = text
                return text

        except PyPDF2.errors.PdfReadError:
            raise ValueError("The file is not a valid PDF")
        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")

    def generate_summary(self, progress_callback=None):
        if not self.text:
            raise ValueError("No text to summarize")

        if progress_callback:
            progress_callback(51)

        if len(self.text.split()) < 100:
            self.summary = self.text
            if progress_callback:
                progress_callback(100)
            return self.text

        approx_word_count = len(self.text.split())
        target_length = int(approx_word_count * self.summary_ratio)

        prompt = f"""
        I need you to create a clear and concise summary of the following text. 
        The summary should:
        - Capture the main ideas and key points
        - Use simple, accessible language
        - Maintain logical flow
        - Be approximately {target_length} words (about 25% of the original)
        - Break down complex concepts into digestible chunks

        Here is the text to summarize:

        {self.text}
        """

        try:
            if progress_callback:
                progress_callback(55)

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.0,
                system="You are a helpful assistant that creates clear, concise summaries.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            summary = response.content[0].text
            self.summary = summary

            if progress_callback:
                progress_callback(100)

            return summary

        except Exception as e:
            raise ValueError(f"Error generating summary with Claude API: {str(e)}")

    def save_summary(self, output_path=None):
        if not self.summary:
            raise ValueError("No summary to save")

        if not output_path:
            pdf_name = os.path.basename(self.pdf_path)
            pdf_name_without_ext = os.path.splitext(pdf_name)[0]
            output_path = f"{pdf_name_without_ext}_summary.txt"

        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(self.summary)
            return output_path
        except Exception as e:
            raise ValueError(f"Error saving summary: {str(e)}")


class SummarizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Claude PDF Summarizer")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        self.configure_theme()

        try:
            self.summarizer = ClaudePDFSummarizer()
            self.setup_ui()
        except ValueError as e:
            messagebox.showerror("Initialization Error", str(e))
            self.root.destroy()

    def configure_theme(self):
        self.root.configure(bg="#0d1117")

        style = ttk.Style()
        style.theme_use('default')

        style.configure('TFrame', background='#0d1117')
        style.configure('TLabelframe', background='#0d1117', foreground='#c9d1d9')
        style.configure('TLabelframe.Label', background='#0d1117', foreground='#c9d1d9')

        style.configure('TButton', background='#21262d', foreground='#c9d1d9', borderwidth=1,
                        focusthickness=0, focuscolor='none')
        style.map('TButton', background=[('active', '#30363d')],
                  foreground=[('active', '#ffffff')])

        style.configure('TLabel', background='#0d1117', foreground='#c9d1d9')
        style.configure('TEntry', fieldbackground='#0d1117', foreground='#c9d1d9',
                        bordercolor='#30363d', lightcolor='#30363d', darkcolor='#30363d')

        style.configure('TProgressbar', background='#2ea043', troughcolor='#21262d',
                        bordercolor='#21262d', lightcolor='#21262d', darkcolor='#21262d')

        style.configure('TScrollbar', background='#21262d', arrowcolor='#c9d1d9',
                        bordercolor='#30363d', troughcolor='#0d1117',
                        lightcolor='#21262d', darkcolor='#21262d')
        style.map('TScrollbar', background=[('active', '#30363d')])

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        file_frame = ttk.LabelFrame(main_frame, text="PDF File", padding="10")
        file_frame.pack(fill=tk.X, pady=5)

        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        file_entry.configure(background='#0d1117', foreground='#c9d1d9')

        ttk.Button(file_frame, text="Browse", command=self.select_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Summarize", command=self.start_summarization).pack(side=tk.LEFT, padx=5)

        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, side=tk.LEFT, expand=True)

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var, width=20)
        status_label.pack(side=tk.RIGHT, padx=5)

        summary_frame = ttk.LabelFrame(main_frame, text="Summary", padding="10")
        summary_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.summary_text = tk.Text(summary_frame, wrap=tk.WORD, bg='#0d1117', fg='#c9d1d9',
                                    insertbackground='#c9d1d9', borderwidth=1,
                                    highlightbackground='#30363d', highlightcolor='#58a6ff',
                                    selectbackground='#264f78', selectforeground='#ffffff')
        scrollbar = ttk.Scrollbar(summary_frame, command=self.summary_text.yview)
        self.summary_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="Save Summary", command=self.save_summary).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_summary).pack(side=tk.RIGHT, padx=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )

        if file_path:
            self.file_path_var.set(file_path)
            self.summarizer.pdf_path = file_path
            self.summary_text.delete(1.0, tk.END)

    def update_progress(self, value):
        self.progress_var.set(value)

        if value < 50:
            self.status_var.set(f"Extracting text: {value * 2}%")
        elif value < 100:
            self.status_var.set("Generating summary...")
        else:
            self.status_var.set("Complete")

        self.root.update_idletimes()

    def start_summarization(self):
        if not self.file_path_var.get():
            messagebox.showerror("Error", "Please select a PDF file")
            return

        self.summarizer.pdf_path = self.file_path_var.get()

        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button) and child['text'] == "Summarize":
                        child.configure(state=tk.DISABLED)

        self.progress_var.set(0)
        self.status_var.set("Starting...")

        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, "Processing PDF... Please wait.")

        threading.Thread(target=self.process_pdf, daemon=True).start()

    def process_pdf(self):
        try:
            self.summarizer.extract_text(progress_callback=self.update_progress)
            summary = self.summarizer.generate_summary(progress_callback=self.update_progress)
            self.root.after(0, self.update_summary_text, summary)

        except ValueError as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}"))
        finally:
            self.root.after(0, self.enable_summarize_button)

    def update_summary_text(self, summary):
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

    def enable_summarize_button(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button) and child['text'] == "Summarize":
                        child.configure(state=tk.NORMAL)

    def save_summary(self):
        if not self.summarizer.summary:
            messagebox.showinfo("Info", "No summary to save")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Summary",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile=os.path.splitext(os.path.basename(self.summarizer.pdf_path))[0] + "_summary.txt"
        )

        if file_path:
            try:
                saved_path = self.summarizer.save_summary(file_path)
                messagebox.showinfo("Success", f"Summary saved to {saved_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save summary: {str(e)}")

    def clear_summary(self):
        self.summary_text.delete(1.0, tk.END)


def main():
    root = tk.Tk()
    app = SummarizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()