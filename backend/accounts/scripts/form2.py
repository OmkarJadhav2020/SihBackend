from fpdf import FPDF
import matplotlib.pyplot as plt
import datetime
import os

class CustomPDF(FPDF):
    """
    A custom PDF class for creating structured reports.
    """

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
        self.set_font("Times", "B", 12)  # Reduced font size
        self.set_fill_color(220, 220, 220)
        self.cell(0, 10, title, ln=1, fill=True, border=1)
        self.set_font("Times", size=10)  # Reduced font size
        self.multi_cell(0, 8, content)  # Adjusted line height
        self.ln(5)

    def add_table(self, data, font_size=8):
        """
        Add a table to the PDF with reduced column width and font size.
        """
        self.set_font("Times", size=font_size)  # Reduced font size
        column_widths = self.calculate_column_widths(data)
        for row in data:
            for i, cell in enumerate(row):
                x, y = self.get_x(), self.get_y()
                self.multi_cell(column_widths[i], 6, str(cell), border=1, align="C")  # Adjusted line height
                self.set_xy(x + column_widths[i], y)  # Move to the next cell
            self.ln()  # Move to the next row
        self.ln(5)

    def calculate_column_widths(self, data):
        """
        Calculate dynamic column widths based on content length.
        """
        table_width = 190  # Total table width
        num_columns = len(data[0])
        base_width = table_width / num_columns  # Distribute width proportionally
        return [base_width] * num_columns  # Equal column widths

    def add_page_with_border(self):
        self.add_page()
        self.set_draw_color(200, 200, 200)
        self.rect(5, 5, 200, 287)


def create_gantt_chart(milestones):
    """
    Generate a Gantt chart for project milestones.
    """
    task_names = [milestone['name'] for milestone in milestones]
    start_dates = [datetime.datetime.strptime(milestone['start_date'], "%Y-%m-%d") for milestone in milestones]
    durations = [milestone['duration'] for milestone in milestones]

    fig, ax = plt.subplots(figsize=(8, 4))
    for i, (task, start, duration) in enumerate(zip(task_names, start_dates, durations)):
        ax.barh(task, duration, left=start.toordinal(), color="#4CAF50")

    ax.set_xlabel("Timeline")
    ax.set_title("Project Milestones")
    ax.set_xlim(left=min(start_dates).toordinal() - 10, right=max(start_dates).toordinal() + max(durations) + 10)
    plt.tight_layout()
    gantt_path = "gantt_chart.png"
    plt.savefig(gantt_path, bbox_inches="tight")
    plt.close()
    return gantt_path


def create_pie_chart(data, labels, title, colors):
    """
    Generate a pie chart.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(data, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
    ax.set_title(title)
    chart_path = f"{title.replace(' ', '_').lower()}_chart.png"
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()
    return chart_path


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
    ],
    "milestones": [
        {"name": "Concept Development", "start_date": "2024-01-01", "duration": 30},
        {"name": "Field Trials", "start_date": "2024-02-01", "duration": 60},
        {"name": "Implementation", "start_date": "2024-04-01", "duration": 120}
    ],
}

# Generate charts
budget_pie_path = create_pie_chart(
    data=[50, 75, 60, 15, 10, 5, 20],
    labels=["Land & Building", "Capital Equipment", "Manpower", "Consumables", "Travel", "Contingencies", "Workshops"],
    title="Budget Allocation",
    colors=["#4CAF50", "#FFC107", "#2196F3", "#F44336", "#9C27B0", "#FF5722", "#795548"]
)
gantt_chart_path = create_gantt_chart(data["milestones"])

# Create the PDF
pdf = CustomPDF()
pdf.add_page_with_border()

pdf.add_section("Project Title", data["title"])
pdf.add_section("Objectives", "\n".join(data["objectives"]))
pdf.add_section("Budget Details", "Below is the detailed budget allocation:")
pdf.add_table(data["budget"])

# pdf.add_section("Budget Overview", "The chart below illustrates the budget allocation:")
# pdf.image(budget_pie_path, x=30, y=None, w=150)

# pdf.add_section("Project Milestones", "The Gantt chart below shows the project timeline:")
# pdf.image(gantt_chart_path, x=15, y=None, w=180)

output_path = "project_proposal.pdf"
pdf.output(output_path)

# Clean up temporary files
# os.remove(budget_pie_path)
# os.remove(gantt_chart_path)

print(f"Report generated successfully: {output_path}")
