from fpdf import FPDF
import datetime

class CustomPDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 16)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, "Project Proposal Report", border=1, ln=1, align="C", fill=True)
        self.set_font("Times", "I", 12)
        self.cell(0, 10, f"Generated on: {datetime.date.today().strftime('%B %d, %Y')}", ln=1, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 10)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_section(self, title, content):
        self.set_font("Times", "B", 14)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 10, title, ln=1, fill=True, border=1)
        self.set_font("Times", size=12)
        self.multi_cell(0, 10, content)
        self.ln(5)

    def add_table(self, data, font_size=10):
        self.set_font("Times", size=font_size)
        column_widths = self.calculate_column_widths(data)
        for row in data:
            for i, cell in enumerate(row):
                x, y = self.get_x(), self.get_y()
                self.multi_cell(column_widths[i], 10, str(cell), border=1, align="C")
                self.set_xy(x + column_widths[i], y)  # Move to the next cell
            self.ln()  # Move to the next row
        self.ln(5)

    def calculate_column_widths(self, data):
        table_width = 190  # Total table width
        num_columns = len(data[0])
        base_width = table_width // num_columns
        return [base_width] * num_columns  # Equal widths for columns

    def add_page_with_border(self):
        self.add_page()
        self.set_draw_color(200, 200, 200)
        self.rect(5, 5, 200, 287)

# Example data
data = {
    "title": "Project Name Example",
    "objectives": [
        "Develop a sustainable methodology for coal mining.",
        "Improve safety standards using modern technology.",
        "Minimize environmental impact."
    ],
    "budget": [
        ["Item", "Approved", "Received", "Interest", "Expenditure", "Balance", "Provision", "Remaining"],
        ["Land & Building", "50.00", "25.00", "1.00", "20.00", "6.00", "30.00", "2.00"],
        ["Capital Equipment", "75.00", "35.00", "2.00", "30.00", "7.00", "40.00", "3.00"],
        ["Manpower", "60.00", "30.00", "1.50", "25.00", "6.50", "35.00", "2.50"],
        ["Consumables", "15.00", "10.00", "0.50", "8.00", "2.50", "12.00", "2.00"],
        ["Travel", "10.00", "5.00", "0.20", "4.00", "1.20", "6.00", "1.00"],
        ["Contingencies", "5.00", "2.50", "0.10", "1.50", "1.10", "3.00", "1.00"],
        ["Workshops", "20.00", "10.00", "0.50", "8.00", "2.50", "12.00", "2.00"],
    ]
}

# Create the PDF
pdf = CustomPDF()
pdf.add_page_with_border()

pdf.add_section("Project Title", data["title"])
pdf.add_section("Objectives", "\n".join(data["objectives"]))
pdf.add_section("Budget Details", "Below is the detailed budget allocation:")
pdf.add_table(data["budget"], font_size=9)

output_path = "project_proposal.pdf"
pdf.output(output_path)

print(f"Report generated successfully: {output_path}")
