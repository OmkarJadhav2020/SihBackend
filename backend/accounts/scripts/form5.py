from fpdf import FPDF
import datetime

class CustomPDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 16)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, "Quarterly Status Report (FORM-V)", border=1, ln=1, align="C", fill=True)
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

    def add_bar_chart_placeholder(self, description):
        self.set_font("Times", "B", 12)
        self.cell(0, 10, description, ln=1, border=0)
        self.ln(10)
        self.rect(10, self.get_y(), 190, 50)  # Placeholder rectangle for the bar chart
        self.ln(55)

    def add_page_with_border(self):
        self.add_page()
        self.set_draw_color(200, 200, 200)
        self.rect(5, 5, 200, 287)

# Data for FORM-V
form_v_data = {
    "project_name": "Development of Advanced Coal Mining Techniques",
    "project_code": "ACM-2025",
    "progress_quarter": "Q3 2025",
    "principal_implementing_agencies": "National Energy Institute",
    "sub_implementing_agencies": "GreenTech Solutions Pvt. Ltd.",
    "project_coordinator": "Dr. John Smith",
    "start_date": "2025-01-01",
    "approved_completion_date": "2026-12-31",
    "activities_status": "Bar chart placeholder with activities and their current status.",
    "work_done": "Research completed on advanced coal separation techniques. Field trials conducted successfully in three major sites.",
    "slippage_reasons": "Delay in acquiring specialized equipment due to supply chain issues. Estimated resolution by next quarter.",
    "corrective_actions": "Expedited procurement processes and reallocation of existing resources to critical tasks.",
    "work_next_quarter": "Begin full-scale implementation at designated mining locations. Complete final safety evaluations.",
    "expenditure_forms": "Expenditure details provided in Forms-III and IV."
}

# Create PDF
pdf = CustomPDF()
pdf.add_page_with_border()

# Add form content
pdf.add_section("1. Name of the Project with Project Code", f"{form_v_data['project_name']} ({form_v_data['project_code']})")
pdf.add_section("2. Progress for the Quarter Ending", form_v_data['progress_quarter'])
pdf.add_section("3. Principal Implementing Agency(s)", form_v_data['principal_implementing_agencies'])
pdf.add_section("4. Sub-Implementing Agency(s)", form_v_data['sub_implementing_agencies'])
pdf.add_section("5. Project Co-ordinator/Leader / Principal Investigator", form_v_data['project_coordinator'])
pdf.add_section("6. Date of Commencement", form_v_data['start_date'])
pdf.add_section("7. Approved Date of Completion", form_v_data['approved_completion_date'])

# Bar chart placeholder
pdf.add_bar_chart_placeholder("8. Bar Chart of Activities as Approved by SSRC (With Latest Status)")

pdf.add_section("9. Details of Work Done During the Quarter", form_v_data['work_done'])
pdf.add_section("10. Slippage, if any, and Reasons Thereof", form_v_data['slippage_reasons'])
pdf.add_section("11. Corrective Actions Taken and To Be Taken to Overcome Slippage", form_v_data['corrective_actions'])
pdf.add_section("12. Work Expected to Be Done in Next Quarter", form_v_data['work_next_quarter'])
pdf.add_section("13. Quarterly Expenditure Statements in Forms-III & IV", form_v_data['expenditure_forms'])

# Save the PDF
output_path = "form_v_report.pdf"
pdf.output(output_path)

print(f"Report generated successfully: {output_path}")
