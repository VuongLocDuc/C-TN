from fpdf import FPDF
from tkinter import filedialog
class PDF(FPDF):
    # Page header
    def Header(self):
        # Logo
        self.Image('logo.png', 10, 6, 30)
        # Arial bold 15
        self.SetFont('Arial', 'B', 15)
        # Move to the right
        self.Cell(80)
        # Title
        self.Cell(30, 10, 'Title', 1, 0, 'C')
        # Line break
        self.Ln(20)

    # Page footer
    def Footer(self):
        # Position at 1.5 cm from bottom
        self.SetY(-15)
        # Arial italic 8
        self.SetFont('Arial', 'I', 8)
        # Page number
        self.Cell(0, 10, 'Page ' + str(self.PageNo()) + '/{nb}', 0, 0, 'C')

# Instanciation of inherited class
pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
print(pdf.h)
# pdf.set_font('Times', '', 12)
# for i in range(1, 41):
#     pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
# filename = filedialog.asksaveasfilename(defaultextension='.pdf')
# if filename:
#     pdf.output(filename, 'F')
