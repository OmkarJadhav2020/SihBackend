from fpdf import FPDF
import datetime

class CustomPDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 16)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, "PROJECT COMPLETION REPORT", border=1, ln=1, align="C", fill=True)
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

    def add_page_with_border(self):
        self.add_page()
        self.set_draw_color(200, 200, 200)
        self.rect(5, 5, 200, 287)

# Data for Project Completion Report
completion_report_data = {
    "project_title": "Development of Sustainable Mining Practices",
    "project_code": "SMP-2025",
    "date_of_commencement": "2024-01-01",
    "approved_completion_date": "2025-12-31",
    "actual_completion_date": "2026-01-15",
    "objectives": [
        "To develop sustainable mining techniques.",
        "To improve safety standards in coal mines.",
        "To minimize environmental impact of mining activities."
    ],
    "work_programme": "As per the approved SSRC proposal, the project aimed at conducting field trials, developing safety tools, and implementing pilot projects.",
    "work_done": "Field trials were conducted successfully. Developed prototypes for safety equipment. Implemented pilot projects in three mining sites.",
    "objectives_fulfilled": "Most objectives were fulfilled, including safety enhancements and reduced environmental impact.",
    "areas_not_covered": "Due to budget constraints, environmental monitoring was limited to two sites.",
    "further_studies": "Further studies recommended in geotechnical monitoring and carbon capture techniques.",
    "conclusions_recommendations": "The project has potential to reduce workplace hazards by 30%. Recommended for adoption in all coal mines.",
    "scope_of_application": "Findings can be applied to coal and metal mines for enhanced safety and reduced environmental footprint.",
    "associated_persons": "Dr. Emily Carter (Safety Engineer), Mr. John Doe (Environmental Scientist), Dr. Alice Brown (Project Manager).",
    "final_expenditure": "Expenditure details provided in Forms III & IV, authenticated by finance department."
}

# Create PDF
pdf = CustomPDF()
pdf.add_page_with_border()

# Add content to the report
pdf.add_section("1. Title of the Project", completion_report_data['project_title'])
pdf.add_section("2. Project Code", completion_report_data['project_code'])
pdf.add_section("3. Date of Commencement", completion_report_data['date_of_commencement'])
pdf.add_section("4. Approved Date of Completion (As Approved Originally)", completion_report_data['approved_completion_date'])
pdf.add_section("5. Actual Date of Completion", completion_report_data['actual_completion_date'])
pdf.add_section("6. Objectives as Stated in the Proposal", "\n".join(completion_report_data['objectives']))
pdf.add_section("7. The Work Programme as Proposed and Approved by SSRC", completion_report_data['work_programme'])
pdf.add_section("8. Details of the Work Done During the Project Run", completion_report_data['work_done'])
pdf.add_section("9. The Extent to Which the Objectives as Outlined in the Original Project Proposal Have Been Fulfilled", completion_report_data['objectives_fulfilled'])
pdf.add_section("10. The Reasons for Not Covering All the Areas (if any) of the Scope of the Study", completion_report_data['areas_not_covered'])
pdf.add_section("11. The Need or Otherwise to Take Up Further Studies in the Areas Not Covered Under This Study", completion_report_data['further_studies'])
pdf.add_section("12. Conclusions and Recommendations with Quantification of Benefits to the Industry", completion_report_data['conclusions_recommendations'])
pdf.add_section("13. Scope of Application of Findings of the Study in the Coal Industry", completion_report_data['scope_of_application'])
pdf.add_section("14. Name of Persons Associated with Project and Type of Expertise Developed by Them", completion_report_data['associated_persons'])
pdf.add_section("15. The Final Expenditure Statement in Form III & IV and Duly Authenticated by Associated Finance of the Company", completion_report_data['final_expenditure'])

# Save the PDF
output_path = "project_completion_report.pdf"
pdf.output(output_path)

print(f"Report generated successfully: {output_path}")
