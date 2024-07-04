from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.image("logo.png", 10, 8, 33)
        self.set_font("helvetica", "B", 16)
        self.cell(80)
        self.cell(40, 10, "Hello, world", border=1,align="C")


pdf = PDF()

pdf.add_page()


pdf.output("sample.pdf")