from fpdf import FPDF
import datetime

class CustomPDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 14)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, "FORM X - DETAILS OF EQUIPMENT PROCURED UNDER S&T SCHEME", border=1, ln=1, align="C", fill=True)
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
        self.set_font("Times", "B", 12)
        self.cell(0, 10, title, ln=1, border=0)
        self.set_font("Times", size=11)
        self.multi_cell(0, 10, content)
        self.ln(5)

    def add_table(self, headers, data):
        self.set_font("Times", "B", 11)
        col_widths = [15, 40, 20, 40, 30, 40, 30, 30]  # Adjusted column widths

        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, border=1, align="C")
        self.ln()
        self.set_font("Times", size=10)

        for row in data:
            for i, item in enumerate(row):
                self.cell(col_widths[i], 10, str(item), border=1, align="C")
            self.ln()
        self.ln(5)

    def add_signature_section(self):
        self.ln(15)
        self.set_font("Times", "B", 12)
        self.cell(0, 10, "Authorized Signatories:", ln=1)
        self.ln(10)
        self.cell(90, 10, "Signature of Project Leader", border=0)
        self.cell(90, 10, "Signature of Project Coordinator", border=0, ln=1)
        self.cell(90, 10, "Name: ____________________", border=0)
        self.cell(90, 10, "Name: ____________________", border=0, ln=1)
        self.cell(90, 10, "Designation: _______________", border=0)
        self.cell(90, 10, "Designation: _______________", border=0, ln=1)

    def add_page_with_border(self):
        self.add_page()
        self.set_draw_color(200, 200, 200)
        self.rect(5, 5, 200, 287)

# Data for FORM X - Details of Equipment Procured
equipment_data = {
    "project_title": "Advanced Coal Mining Techniques",
    "project_code": "ACMT-2026",
    "principal_agency": "National Coal Agency",
    "sub_agency": "Regional Mining Development Unit",
    "equipment_details": [
        ["Excavator", "2", "CAT 320", "2020", "Sustainable Mining Project", "Operational", "Efficient"],
        ["Drill Machine", "5", "Atlas Copco DM45", "2021", "Eco-Friendly Drilling", "Under Maintenance", "Spare parts required"],
        ["Conveyor Belt", "1", "Siemens CB100", "2019", "Material Transport System", "Operational", "None"],
    ]
}

# Create PDF
pdf = CustomPDF()
pdf.add_page_with_border()

# Add content to the report
pdf.add_section("Name of the Project", equipment_data['project_title'])
pdf.add_section("Project Code", equipment_data['project_code'])
pdf.add_section("Principal Implementing Agency(s)", equipment_data['principal_agency'])
pdf.add_section("Sub Implementing Agency(s)", equipment_data['sub_agency'])

# Add table for equipment details
headers = ["Sl. No.", "Details of Equipment", "No. of Sets", "Make & Model", "Year of Procurement", "Name of the S&T/R&D Project", "Status of Equipment", "Remarks"]
data_with_sl_no = [[i + 1] + row for i, row in enumerate(equipment_data['equipment_details'])]
pdf.add_section("Details of Equipment Procured:", "Below is the list of equipment procured under the S&T Scheme.")
pdf.add_table(headers, data_with_sl_no)

# Add signature section
pdf.add_signature_section()

# Save the PDF
output_path = "form_x_equipment_report.pdf"
pdf.output(output_path)

print(f"Report generated successfully: {output_path}")
