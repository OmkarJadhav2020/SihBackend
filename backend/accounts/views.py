from .serializers import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from fpdf import FPDF
import matplotlib.pyplot as plt
from datetime import datetime


# from   datetime import date
class CustomPDF(FPDF):
    """
    A custom PDF class for creating structured reports.
    """

    def header(self):
        self.set_font("Times", "B", 16)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, "Project Proposal Report",
                  border=1, ln=1, align="C", fill=True)
        self.set_font("Times", "I", 12)
        self.cell(0, 10, f"Generated on: {
                  datetime.today().strftime('%B %d, %Y')}", ln=1, align="C")
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
                self.multi_cell(column_widths[i], 6, str(
                    cell), border=1, align="C")  # Adjusted line height
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


class CustomPDF1(FPDF):
    def header(self):
        self.set_font("Times", "B", 16)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, "Quarterly Status Report (FORM-V)",
                  border=1, ln=1, align="C", fill=True)
        self.set_font("Times", "I", 12)
        self.cell(0, 10, f"Generated on: {
                  datetime.today().strftime('%B %d, %Y')}", ln=1, align="C")
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
        # Placeholder rectangle for the bar chart
        self.rect(10, self.get_y(), 190, 50)
        self.ln(55)

    def add_page_with_border(self):
        self.add_page()
        self.set_draw_color(200, 200, 200)
        self.rect(5, 5, 200, 287)


class SignupView(APIView):
    """
    API View for User Signup with Role
    """

    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful', 'role': user.role, 'token': token.key, "id": user.id}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserInfoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        print(serializer.data)
        return Response(serializer.data)


class GetList(APIView):
    def get(self, request):
        investigators = User.objects.filter(
            role="investigator").values("id", "username")
        return Response({"data": investigators}, status=status.HTTP_200_OK)


class ProposalViewSet(APIView):

    def get(self, request):
        proposals = ProjectProposal.objects.filter(approved=False).values()
        return Response({"data": proposals})

    def post(self, request):
        print(request.data)
        serializer = ProjectProposalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Project Proposal Submitted Successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, proposal_id):
        print(request)
        try:
            proposal = ProjectProposal.objects.get(id=proposal_id)
            proposal.delete()
            return Response({'message': 'Proposal deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except ProjectProposal.DoesNotExist:
            return Response({'error': 'Proposal not found!'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, proposal_id):
        try:
            proposal = ProjectProposal.objects.get(id=proposal_id)
            proposal.approved = True  # Update the `approved` field
            data = {"title": proposal.objective, "description": proposal.issue_definition, "proposal": proposal.id, "start_date": proposal.start_date, "end_date": proposal.end_date,
                    "progress_status": "initial", "duration": (proposal.end_date - proposal.start_date).days, "assigned_investigators": [proposal.coordinator.id, proposal.co_investigator.id]}
            print(data)
            serializer = ProjectSerializer(data=data)
            if serializer.is_valid():
                # serializer.save()
                proposal.save()  # Save the changes
                return Response({'message': 'Project Added Successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ProjectProposal.DoesNotExist:
            return Response({'error': 'Proposal not found!'}, status=status.HTTP_404_NOT_FOUND)


class ProjectViewSet(APIView):
    def get(self, request, id):
        if id == 0:
            projects = Project.objects.all().values()
            return Response({"data": projects})
        else:
            projects = Project.objects.filter(
                assigned_investigators__id=id).values()
            return Response({"data": projects})

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Project Added Successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectInfo(APIView):
    def post(self, request):
        projectid = request.data["id"]
        print(projectid)
        project = Project.objects.filter(id=projectid).values()
        if project:
            return Response(project[0])
        return Response({"msg": "data doesn't exist"})


class ReportListView(APIView):

    def post(self, request):
        queryset = Report.objects.filter(project=request.data["id"]).values()

        return Response({"data": queryset})


class ReportView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if request.method == "POST":
            name = request.data.get('name', None)
            description = request.data.get('description', None)
            project = request.data.get('id', None)
            print(request.FILES)
            file = request.data.get('file', None)
            print(name)
            print(description)
            print(project)
            print(file)
            if not name or not description or not project or not file:
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            try:
                project = Project.objects.get(id=project)
                report = Report.objects.create(
                    name=name,
                    description=description,
                    project=project,
                    file=file
                )
                return JsonResponse({'message': 'Report uploaded successfully!'}, status=201)
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found.'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)


# List and Create View (GET, POST)

class FundRequisitionListCreateView(APIView):
    def get(self, request):
        fund_requisitions = FundRequisition.objects.all()
        serializer = FundRequisitionSerializer(fund_requisitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FundRequisitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, Update (PATCH), and Delete View

# List and Create View (GET, POST)

class FundRequisitionListCreateView(APIView):
    def get(self, request):
        fund_requisitions = FundRequisition.objects.all()
        serializer = FundRequisitionSerializer(fund_requisitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FundRequisitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.views import APIView

# List and Create View (GET, POST)

class FundRequisitionListCreateView(APIView):
    def get(self, request):
        fund_requisitions = FundRequisition.objects.all()
        serializer = FundRequisitionSerializer(fund_requisitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FundRequisitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List and Create View (GET, POST)


class FundRequisitionListCreateView(APIView):
    def get(self, request):
        fund_requisitions = FundRequisition.objects.all()
        serializer = FundRequisitionSerializer(fund_requisitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FundRequisitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update (PATCH), and Delete View


class FundRequisitionDetailView(APIView):
    def get_object(self, pk):
        try:
            return FundRequisition.objects.get(pk=pk)
        except FundRequisition.DoesNotExist:
            return None

    def get(self, request, pk):
        fund_requisition = self.get_object(pk)
        if fund_requisition is None:
            return Response({"error": "Fund Requisition not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FundRequisitionSerializer(fund_requisition)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        fund_requisition = self.get_object(pk)
        if fund_requisition is None:
            return Response({"error": "Fund Requisition not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FundRequisitionSerializer(
            fund_requisition, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenditureQuestionListCreateView(APIView):
    def get(self, request):
        questions = ExpenditureQuestion.objects.all()
        serializer = ExpenditureQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExpenditureQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List and Create (POST and GET All)

class QuarterlyExpenditureStatementListCreateView(APIView):
    def get(self, request):
        expenditures = QuarterlyExpenditureStatement.objects.all()
        serializer = QuarterlyExpenditureStatementSerializer(
            expenditures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuarterlyExpenditureStatementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve (GET by ID)


class QuarterlyExpenditureStatementDetailView(APIView):
    def get_object(self, pk):
        try:
            return QuarterlyExpenditureStatement.objects.get(pk=pk)
        except QuarterlyExpenditureStatement.DoesNotExist:
            return None

    def get(self, request, pk):
        expenditure = self.get_object(pk)
        if not expenditure:
            return Response({"error": "Expenditure Statement not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuarterlyExpenditureStatementSerializer(expenditure)
        return Response(serializer.data, status=status.HTTP_200_OK)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import ProjectCompletionReport
# from .serializers import ProjectCompletionReportSerializer

# List and Create View
# class ProjectCompletionReportListCreateView(APIView):
#     def get(self, request):
#         reports = ProjectCompletionReport.objects.all()
#         serializer = ProjectCompletionReportSerializer(reports, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = ProjectCompletionReportSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Retrieve View (GET by ID)
# class ProjectCompletionReportDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return ProjectCompletionReport.objects.get(pk=pk)
#         except ProjectCompletionReport.DoesNotExist:
#             return None
#     def get(self, request, pk):
#         report = self.get_object(pk)
#         if not report:
#             return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ProjectCompletionReportSerializer(report)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# Create and List View

class FinanceAnalysisListCreateView(APIView):
    def get(self, request):
        analyses = FinanceAnalysis.objects.all()
        serializer = FinanceAnalysisSerializer(analyses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FinanceAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, and Delete View


class FinanceAnalysisDetailView(APIView):
    def get_object(self, pk):
        try:
            return FinanceAnalysis.objects.get(pk=pk)
        except FinanceAnalysis.DoesNotExist:
            return None

    def get(self, request, pk):
        analysis = self.get_object(pk)
        if not analysis:
            return Response({"error": "Finance Analysis not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FinanceAnalysisSerializer(analysis)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        analysis = self.get_object(pk)
        if not analysis:
            return Response({"error": "Finance Analysis not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FinanceAnalysisSerializer(
            analysis, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        analysis = self.get_object(pk)
        if not analysis:
            return Response({"error": "Finance Analysis not found"}, status=status.HTTP_404_NOT_FOUND)
        analysis.delete()
        return Response({"message": "Finance Analysis deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class IncrementRequestListCreateView(APIView):
    def get(self, request):
        requests = IncrementRequest.objects.all()
        serializer = IncrementRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = IncrementRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncrementRequestDetailView(APIView):
    def get_object(self, pk):
        try:
            return IncrementRequest.objects.get(pk=pk)
        except IncrementRequest.DoesNotExist:
            return None

    def get(self, request, pk):
        increment_request = self.get_object(pk)
        if not increment_request:
            return Response({"error": "Increment request not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = IncrementRequestSerializer(increment_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectCompletionReportView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ProjectCompletionReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Project completion report submitted successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectRevisionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProjectRevisionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        revisions = ProjectRevision.objects.all()
        serializer = ProjectRevisionSerializer(revisions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectFundView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            print(f"Incoming Data: {request.data}")
            temp = request.data
            obj = {}
            obj["title"] = temp["projectName"]
            obj["objectives"] = [
                "Develop a sustainable methodology for coal mining.",
                "Improve safety standards using modern technology.",
                "Minimize environmental impact."
            ]
            obj["budget"] = []
            obj["budget"].append(["Item", "Approved", "Received", "Interest",
                                 "Expenditure", "Balance", "Provision", "Remaining"])
            print()
            for i in temp["items"]:
                t = []
                for ele in i:
                    t.append(i[ele])
                obj["budget"].append(t)

            obj["milestones"] = [
                {"name": "Concept Development",
                    "start_date": "2024-01-01", "duration": 30},
                {"name": "Field Trials", "start_date": "2024-02-01", "duration": 60},
                {"name": "Implementation", "start_date": "2024-04-01", "duration": 120}
            ]
            print(obj)
            pdf = CustomPDF()

            pdf.add_page_with_border()

            pdf.add_section("Project Title", obj["title"])
            pdf.add_section("Objectives", "\n".join(obj["objectives"]))
            pdf.add_section("Budget Details",
                            "Below is the detailed budget allocation:")
            pdf.add_table(obj["budget"])
            output_path = "media/project_proposal.pdf"
            pdf.output(output_path)

            serializer = ProjectFundSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f"Validation Errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Server Error: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            projects = ProjectFund.objects.all()
            serializer = ProjectFundSerializer(projects, many=True)
            data = serializer.data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Server Error: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectFinance2(APIView):
    def post(self, request):
        print(request.data)
        projects = ProjectFund.objects.filter(
            projectid=request.data["projectid"]).values()
        totalfundrecived = 0
        totalfundrequired = 0
        totalfundused = 0
        m = {}
        fundwise = {}
        for i in projects:
            # fundwise = 0
            item = Item.objects.filter(project=i["id"]).values()
            for ele in item:

                m[ele["name"]] = m.get(ele["name"], 0) + \
                    ele.get(0, ele["expenditureIncurred"])
                totalfundrecived += ele['fundReceived']
                totalfundrequired += ele['fundRequired']
                totalfundused += ele['expenditureIncurred']
                fundwise[ele["project_id"]] = fundwise.get(
                    ele['project_id'], 0) + ele['fundRequired']
        return Response({"fundDispersed": totalfundrecived, "fundRequired": totalfundrequired, "fundUsed": totalfundused, "piechartdata": m, "fundFormData": fundwise})


class EndorsementFormView(APIView):

    def get(self, request, *args, **kwargs):
        forms = EndorsementForm.objects.all()
        serializer = EndorsementFormSerializer(forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = EndorsementFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuarterlyStatusReportView(APIView):
    def get(self, request, *args, **kwargs):
        reports = QuarterlyStatusReport.objects.all()
        serializer = QuarterlyStatusReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = QuarterlyStatusReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectCompletionReportView(APIView):

    def get(self, request, *args, **kwargs):
        reports = ProjectCompletionReport2.objects.all()
        serializer = ProjectCompletionReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        temp = request.data
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
        form_v_data["project_code"] = temp["projectCode"]
        form_v_data["project_name"] = temp["title"]
        form_v_data["project_coordinator"] = temp["associatedPersons"]
        form_v_data["start_date"] = temp["commencementDate"]
        form_v_data["approved_completion_date"] = temp["approvedCompletionDate"]
        form_v_data["slippage_reasons"] = temp["reasonsForSlippage"]
        form_v_data["work_next_quarter"] = temp["furtherStudiesNeeded"]

        pdf = CustomPDF1()
        pdf.add_page_with_border()

        # Add form content
        pdf.add_section("1. Name of the Project with Project Code", f"{
                        form_v_data['project_name']} ({form_v_data['project_code']})")
        pdf.add_section("2. Progress for the Quarter Ending",
                        form_v_data['progress_quarter'])
        pdf.add_section("3. Principal Implementing Agency(s)",
                        form_v_data['principal_implementing_agencies'])
        pdf.add_section("4. Sub-Implementing Agency(s)",
                        form_v_data['sub_implementing_agencies'])
        pdf.add_section("5. Project Co-ordinator/Leader / Principal Investigator",
                        form_v_data['project_coordinator'])
        pdf.add_section("6. Date of Commencement", form_v_data['start_date'])
        pdf.add_section("7. Approved Date of Completion",
                        form_v_data['approved_completion_date'])

        # Bar chart placeholder
        pdf.add_bar_chart_placeholder(
            "8. Bar Chart of Activities as Approved by SSRC (With Latest Status)")

        pdf.add_section(
            "9. Details of Work Done During the Quarter", form_v_data['work_done'])
        pdf.add_section("10. Slippage, if any, and Reasons Thereof",
                        form_v_data['slippage_reasons'])
        pdf.add_section("11. Corrective Actions Taken and To Be Taken to Overcome Slippage",
                        form_v_data['corrective_actions'])
        pdf.add_section("12. Work Expected to Be Done in Next Quarter",
                        form_v_data['work_next_quarter'])
        pdf.add_section("13. Quarterly Expenditure Statements in Forms-III & IV",
                        form_v_data['expenditure_forms'])

        # Save the PDF
        output_path = "media/form_v_report.pdf"
        pdf.output(output_path)

        print(f"Report generated successfully: {output_path}")

        serializer = ProjectCompletionReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectExtensionReportView(APIView):

    def get(self, request, *args, **kwargs):
        reports = ProjectExtensionReport.objects.all()
        serializer = ProjectExtensionReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProjectExtensionReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectRevisionTwoView(APIView):

    def get(self, request, *args, **kwargs):
        revisions = ProjectRevisionTwo.objects.all()
        serializer = ProjectRevisionTwoSerializer(revisions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProjectRevisionTwoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectEquipmentView(APIView):

    def get(self, request, *args, **kwargs):
        projects = ProjectEquipment.objects.all()
        serializer = ProjectEquipmentSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProjectEquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectManpowerView(APIView):

    def get(self, request):
        projects = ProjectManpower.objects.all()
        serializer = ProjectManpowerSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectManpowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectTravelView(APIView):
    def get(self, request):
        projects = ProjectTravel.objects.all()
        serializer = ProjectTravelSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectTravelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .serializers import TimelineTaskSerializer

class TimelineTaskView(APIView):

    def get(self, request, project_id, *args, **kwargs):
        """
        Get all timeline tasks for a specific project.
        """
        try:
            # project = Project.objects.get(id=project_id)
            tasks = TimelineTask.objects.filter(id=project_id)
            serializer = TimelineTaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        """
        Create one or more timeline tasks for a specific project.
        """
        if isinstance(request.data, list):
            # Adding project to each task if not included
            for task in request.data:
                print(task)
                if 'project' not in task:
                    return Response({"error": "Project ID is required for each task."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = TimelineTaskSerializer(data=request.data, many=True)
        else:
            if 'project' not in request.data:
                return Response({"error": "Project ID is required."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = TimelineTaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, task_id, *args, **kwargs):
        """
        Update an existing timeline task.
        """
        try:
            task = TimelineTask.objects.get(id=task_id)
            serializer = TimelineTaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TimelineTask.DoesNotExist:
            return Response({"error": "Timeline task not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, task_id, *args, **kwargs):
        """
        Delete a timeline task.
        """
        try:
            task = TimelineTask.objects.get(id=task_id)
            task.delete()
            return Response({"message": "Timeline task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except TimelineTask.DoesNotExist:
            return Response({"error": "Timeline task not found."}, status=status.HTTP_404_NOT_FOUND)
# from .models 
class TimelineTaskView1(APIView):
    def post(self,request):
        data = TimelineTask.objects.filter(project_id=request.data["id"])
        return Response({"data":data.values()})

from datetime import datetime
class ProjectCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print("Incoming Data:", data)
        try:
            # Validate investigators
            investigator_ids = list(map(int, data.get('assigned_investigators', [])))
            investigators = User.objects.filter(id__in=investigator_ids)
            if investigators.count() != len(investigator_ids):
                return Response({"error": "One or more assigned investigators do not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Validate and fetch proposal
            proposal_id = data.get('proposal')
            proposal = None
            if proposal_id:
                try:
                    proposal = ProjectProposal.objects.get(id=int(proposal_id))
                except ProjectProposal.DoesNotExist:
                    return Response({"error": f"Proposal with ID {proposal_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Parse dates
            try:
                start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
                end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
            except (ValueError, TypeError):
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

            # Create project
            project = Project.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                proposal=proposal,
                status=data.get('status', 'Processing'),
                start_date=start_date,
                end_date=end_date,
                current_progress_percentage=float(data.get('current_progress_percentage', 0.0)),
                progress_status=data.get('progress_status'),
                duration=data.get('duration', ''),
                budget=float(data.get('budget', 0)),
                funds_used=float(data.get('funds_used', 0)),
            )
            project.assigned_investigators.set(investigators)
            project.save()

            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Error:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Fund, Project, User
from .serializers import FundSerializer

class FundView(APIView):
    def get(self, request):
        funds = Fund.objects.all()
        serializer = FundSerializer(funds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            # Validate the project and investigator
            project = Project.objects.get(id=data['project'])
            investigator = User.objects.get(id=data['investigator'])
        except Project.DoesNotExist:
            return Response({"error": "Invalid Project ID."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid Investigator ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Fund entry
        fund = Fund.objects.create(
            project=project,
            investigator=investigator,
            fund_amount=data['fundAmount'],
            gst_rate=data['gstRate'],
            other_tax_rate=data['otherTaxRate'],
            gst=data['gst'],
            other_taxes=data['otherTaxes'],
            remaining_amount=data['remainingAmount'],
        )

        serializer = FundSerializer(fund)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
