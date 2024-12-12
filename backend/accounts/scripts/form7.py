from fpdf import FPDF
import datetime

class CustomPDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 16)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, "FORM VII - EXTENSION OF PROJECT DURATION", border=1, ln=1, align="C", fill=True)
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

    def add_signature_section(self):
        self.ln(15)
        self.set_font("Times", "B", 12)
        self.cell(0, 10, "Signatures:", ln=1)
        self.ln(10)
        self.cell(0, 10, "Signature of Project Leader", ln=1)
        self.cell(0, 10, "Name: ______________________", ln=1)
        self.cell(0, 10, "Designation: _______________", ln=1)
        self.ln(10)
        self.cell(0, 10, "Signature of Project Coordinator", ln=1)
        self.cell(0, 10, "Name: ______________________", ln=1)
        self.cell(0, 10, "Designation: _______________", ln=1)
        self.ln(15)
        self.cell(0, 10, "Seal and Signature", ln=1)
        self.ln(20)

    def add_page_with_border(self):
        self.add_page()
        self.set_draw_color(200, 200, 200)
        self.rect(5, 5, 200, 287)

# Data for FORM VII - Extension of Project Duration
extension_data = {
    "project_title": "Development of Advanced Mining Safety Systems",
    "project_code": "AMS-2025",
    "principal_agency": "National Mining Research Institute",
    "project_leader": "Dr. Alex Johnson",
    "start_date": "2024-01-01",
    "scheduled_completion_date": "2025-12-31",
    "approved_objectives": "Enhance safety protocols and reduce accident rates using advanced AI tools.",
    "approved_work_programme": "Phase 1: AI tool development; Phase 2: Field trials; Phase 3: Implementation.",
    "work_done_details": "AI tools successfully developed. Field trials are in progress but delayed due to unforeseen circumstances.",
    "revised_chart": "Revised Bar Chart/PERT attached with extended timelines for field trials.",
    "time_extension": "12 months (new completion date: 2026-12-31).",
    "reasons_for_extension": "Delays in equipment procurement and unexpected technical challenges.",
    "project_cost": "$2,000,000",
    "actual_expenditure": "$1,750,000"
}

# Create PDF
pdf = CustomPDF()
pdf.add_page_with_border()

# Add content to the report
pdf.add_section("1. Name of the Project with Project Code", f"{extension_data['project_title']} ({extension_data['project_code']})")
pdf.add_section("2. Name of the Principal Implementing/Sub-implementing Agency", extension_data['principal_agency'])
pdf.add_section("3. Name of Project Leader/Coordinator/Principal Investigator", extension_data['project_leader'])
pdf.add_section("4. Date of Start of the Project", extension_data['start_date'])
pdf.add_section("5. Scheduled Date of Completion of the Project", extension_data['scheduled_completion_date'])
pdf.add_section("6. Approved Objectives", extension_data['approved_objectives'])
pdf.add_section("7. Approved Work Programme Along with Schedule", extension_data['approved_work_programme'])
pdf.add_section("8. Details of Work Done Along with Approved Time Schedule of Work Plan", extension_data['work_done_details'])
pdf.add_section("9. Revised Bar Chart / PERT Network of Activities", extension_data['revised_chart'])
pdf.add_section("10. Time Extension Proposed and Reasons for Seeking the Extension", f"{extension_data['time_extension']} - {extension_data['reasons_for_extension']}")
pdf.add_section("11. Total Cost of the Project and Actual Expenditure Incurred", f"Total Cost: {extension_data['project_cost']}\nActual Expenditure: {extension_data['actual_expenditure']}")

# Add signature section
pdf.add_signature_section()

# Save the PDF
output_path = "form_vii_extension_report.pdf"
pdf.output(output_path)

print(f"Report generated successfully: {output_path}")
