from fpdf import FPDF


name = 'Keith'

#width and height of the page
WIDTH = 210
HEIGHT = 297

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 0, f'Hello my name is {name}!')

pdf.image("plots.png", x=0, y=100, w=WIDTH-5)

pdf.output('tutorial.pdf', 'F')