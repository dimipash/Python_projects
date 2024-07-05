from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def chapter_title(self):
        pass

    def chapter_body(self, filepath):
        with open(filepath, "rb") as fh:
            txt = fh.read().decode('latin-1')
        self.set_font("Times", size=12)
        self.multi_cell(0, 5, txt)
        self.ln()
        self.set_font(style="I")
        self.cell(0, 5, "(End of excerpt)")
        

    def print_chapter(self, filepath):
        self.add_page()
        self.chapter_body(filepath)


pdf = PDF()
pdf.print_chapter("para.txt")
pdf.output("sample.pdf")