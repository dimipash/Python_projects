from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.image("logo.png", 10, 8, 33)
        self.set_font("helvetica", "B", 16)
        self.cell(80)
        self.cell(40, 10, "Hello, world", border=1,align="C")
        self.ln(40)


pdf = PDF()
pdf.add_page()
pdf.set_font("helvetica", "B", 16)
for i in range(1, 41):
    pdf.cell(0, 10, f"Printing line number {i}", new_x="LMARGIN", new_y="NEXT")


pdf.output("sample.pdf")