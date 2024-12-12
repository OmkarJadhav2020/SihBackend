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

    def add_table(self, data, column_widths):
        self.set_font("Times", size=10)
        for row in data:
            max_line_count = 1
            cell_heights = []

            for i, cell in enumerate(row):
                self.set_font_size(10)
                lines = self.multi_cell(column_widths[i], 10, str(cell), border=0, align="C", split_only=True)
                cell_heights.append(len(lines))

            max_line_count = max(cell_heights)

            for i, cell in enumerate(row):
                x, y = self.get_x(), self.get_y()
                self.multi_cell(column_widths[i], 10, str(cell), border=1, align="C")
                self.set_xy(x + column_widths[i], y)

            self.ln(10 * max_line_count)
        self.ln(5)

    def add_page_with_border(self):
        self.add_page()
        self.set_draw_color(200, 200, 200)
        self.rect(5, 5, 200, 287)

# Data for FORM-IV
project_details = {
    "project_code": "CEP-2025",
    "company_name": "National Energy Research Institute",
    "statement_period": "2025-2026",
}

data_table = [
    ["Item", "Approved", "Received", "Interest", "Expenditure", "Balance", "Provision", "Remaining"],
    ["Land & Building", "60.00", "30.00", "1.50", "25.00", "5.50", "35.00", "3.00"],
    ["Capital Equipment", "80.00", "40.00", "2.50", "35.00", "7.50", "45.00", "4.00"],
    ["Manpower", "70.00", "35.00", "1.80", "30.00", "5.20", "40.00", "3.50"],
    ["Consumables", "20.00", "12.00", "0.80", "10.00", "2.00", "15.00", "1.50"],
    ["Travel", "15.00", "7.50", "0.30", "6.00", "1.20", "8.00", "1.00"],
    ["Contingencies", "8.00", "4.00", "0.20", "3.00", "1.00", "5.00", "0.80"],
    ["Workshops", "25.00", "12.50", "0.70", "10.00", "2.80", "15.00", "2.00"],
]

# Create PDF
pdf = CustomPDF()
pdf.add_page_with_border()

# Add project details
pdf.set_font("Times", "B", 12)
pdf.cell(0, 10, f"Project Code: {project_details['project_code']}", ln=1, border=0)
pdf.cell(0, 10, f"Company Name: {project_details['company_name']}", ln=1, border=0)
pdf.cell(0, 10, f"Statement Period: {project_details['statement_period']}", ln=1, border=0)
pdf.ln(10)

# Add table
column_widths = [30, 20, 20, 20, 20, 20, 20, 20]  # Adjusted column widths
pdf.add_table(data_table, column_widths)

# Save the PDF
output_path = "form_iv_report.pdf"
pdf.output(output_path)

print(f"Report generated successfully: {output_path}")
