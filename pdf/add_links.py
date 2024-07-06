"""
PDF Generator with Links and HTML

This script creates a PDF document using FPDF library with the following features:
- Adds text with an internal link
- Embeds an image with an external link
- Incorporates HTML content

Requirements:
- fpdf library
- logo.png file in the same directory

Output: link.pdf
"""

from fpdf import FPDF

pdf = FPDF()

pdf.add_page()
pdf.set_font("helvetica", size=20)
pdf.write(5, "To find out what's new in tutorial, click ")
pdf.set_font(style="U")
link = pdf.add_link(page=2)
pdf.write(5, "here", link)

pdf.add_page()
pdf.image("logo.png", 10, 10, 50, 0, "", "https://www.google.com")
pdf.set_left_margin(60)
pdf.set_font_size(18)
pdf.write_html(""" You can add any html code here <b>This is some bold text</b>
               <h1>This is a heading</h1>
               <a href="http://www.google.com">Click here to go to Google</a> 
                """)

pdf.output('link.pdf')