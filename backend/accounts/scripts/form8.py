from fpdf import FPDF
import datetime

class CustomPDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, "FORM VIII - REVISION OF THE COST OF THE PROJECT/RE-APPROPRIATION OF FUNDS", border=1, ln=1, align="C", fill=True)
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
        self.cell(0, 10, "Authorized Signatory:", ln=1)
        self.ln(10)
        self.cell(0, 10, "Seal and Signature", ln=1)
        self.ln(20)
        
    def add_signature_section_projectleader(self):
        self.ln(15)
        self.set_font("Times", "B", 12)
        self.cell(0, 10, "Signature of project leader:", ln=1)
        self.ln(10)
        self.cell(0, 10, "Seal and Signature", ln=1)
        self.ln(20)

    def add_page_with_border(self):
        self.add_page()
        self.set_draw_color(200, 200, 200)
        self.rect(5, 5, 200, 287)

# Data for FORM VIII - Revision of the Cost of the Project/Re-Appropriation of Funds
revision_data = {
    "project_title": "Development of Sustainable Mining Practices",
    "project_code": "SMP-2025",
    "principal_agency": "National Mining Agency",
    "project_leader": "Dr. John Doe",
    "date_of_commencement": "2024-01-01",
    "scheduled_completion_date": "2025-12-31",
    "approved_objectives": "Develop sustainable mining methodologies with reduced environmental impact.",
    "approved_work_programme": "Initial surveys, field trials, and implementation of eco-friendly techniques.",
    "details_of_work_done": "Completed initial surveys and phase 1 trials as per the approved schedule.",
    "total_approved_cost": "$2,000,000",
    "revised_time_schedule": "Extension by 12 months to accommodate additional trials.",
    "actual_expenditure": "$1,200,000",
    "revised_cost": "$2,500,000",
    "justification": "Increased costs due to inflation, additional trials, and procurement delays."
}

# Create PDF
pdf = CustomPDF()
pdf.add_page_with_border()

# Add content to the report
pdf.add_section("1. Name of the Project with Project Code", f"{revision_data['project_title']} ({revision_data['project_code']})")
pdf.add_section("2. Name of the Principal Implementing/Sub-Implementing Agency", revision_data['principal_agency'])
pdf.add_section("3. Name of Project Leader/Coordinator/Principal Investigator", revision_data['project_leader'])
pdf.add_section("4. Date of Start of the Project", revision_data['date_of_commencement'])
pdf.add_section("5. Scheduled Date of Completion of the Project", revision_data['scheduled_completion_date'])
pdf.add_section("6. Approved Objective(s)", revision_data['approved_objectives'])
pdf.add_section("7. Approved Work Programme Along with Schedule", revision_data['approved_work_programme'])
pdf.add_section("8. Details of Work Done Along with Actual Time Schedule (Bar Chart)", revision_data['details_of_work_done'])
pdf.add_section("9. Total Approved Cost Along with Its Break-Up", revision_data['total_approved_cost'])
pdf.add_section("10. Revised Time Schedule, If Applicable", revision_data['revised_time_schedule'])
pdf.add_section("11. Actual Expenditure Till Last Quarter (Form III & IV)", revision_data['actual_expenditure'])
pdf.add_section("12. Revised Cost of the Project vis-a-vis the Approved Cost and Reasons & Justification for the Revision/Re-Appropriation Sought", revision_data['justification'])

# Add signature section
pdf.add_signature_section()

# Add signature section
pdf.add_signature_section_projectleader()

# Save the PDF
output_path = "form_viii_revision_report.pdf"
pdf.output(output_path)

print(f"Report generated successfully: {output_path}")
