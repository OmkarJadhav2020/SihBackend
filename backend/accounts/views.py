from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProjectProposalSerializer, ProjectSerializer,ReportSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from .models import ProjectProposal,Report
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User,Project
from django.http import QueryDict
import json
from rest_framework.parsers import MultiPartParser, FormParser




class LoginView(APIView):
    def post(self, request):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        print(username,password)
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
            data = {"title" : proposal.objective,"description" : proposal.issue_definition,"proposal":proposal.id,"start_date" : proposal.start_date,"end_date" : proposal.end_date ,"progress_status" :"initial","duration":(proposal.end_date- proposal.start_date).days,"assigned_investigators" : [proposal.coordinator.id,proposal.co_investigator.id]}
            print(data)
            serializer = ProjectSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                proposal.save()  # Save the changes
                return Response({'message': 'Project Added Successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ProjectProposal.DoesNotExist:
            return Response({'error': 'Proposal not found!'}, status=status.HTTP_404_NOT_FOUND)


class ProjectViewSet(APIView):
    def get(self,request,id):
        if id == 0:
            projects = Project.objects.all().values()
            return Response({"data":projects})
        else:
            projects = Project.objects.filter(assigned_investigators__id=id).values()
            return Response({"data":projects})
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Project Added Successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProjectInfo(APIView):
    def post(self,request):
        projectid = request.data["id"]
        print(projectid)
        project = Project.objects.filter(id = projectid).values()
        if project:
            return Response(project[0])
        return Response({"msg" : "data doesn't exist"})
    


class ReportView(APIView):
    queryset = Report.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def post(self,request):
        if request.method == "POST":
            name = request.data.get('name', None)
            description = request.data.get('description', None)
            project = request.data.get('project', None)
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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FundRequisition
from .serializers import FundRequisitionSerializer

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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FundRequisition
from .serializers import FundRequisitionSerializer

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
from rest_framework.response import Response
from rest_framework import status
from .models import FundRequisition
from .serializers import FundRequisitionSerializer

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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FundRequisition
from .serializers import FundRequisitionSerializer

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
        serializer = FundRequisitionSerializer(fund_requisition, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



from .models import ExpenditureQuestion, ExpenditureStatement
from .serializers import ExpenditureQuestionSerializer, ExpenditureStatementSerializer

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






from .models import QuarterlyExpenditureStatement
from .serializers import QuarterlyExpenditureStatementSerializer

# List and Create (POST and GET All)
class QuarterlyExpenditureStatementListCreateView(APIView):
    def get(self, request):
        expenditures = QuarterlyExpenditureStatement.objects.all()
        serializer = QuarterlyExpenditureStatementSerializer(expenditures, many=True)
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
    





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProjectCompletionReport
from .serializers import ProjectCompletionReportSerializer

# List and Create View
class ProjectCompletionReportListCreateView(APIView):
    def get(self, request):
        reports = ProjectCompletionReport.objects.all()
        serializer = ProjectCompletionReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectCompletionReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve View (GET by ID)
class ProjectCompletionReportDetailView(APIView):
    def get_object(self, pk):
        try:
            return ProjectCompletionReport.objects.get(pk=pk)
        except ProjectCompletionReport.DoesNotExist:
            return None

    def get(self, request, pk):
        report = self.get_object(pk)
        if not report:
            return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectCompletionReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FinanceAnalysis
from .serializers import FinanceAnalysisSerializer

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
        serializer = FinanceAnalysisSerializer(analysis, data=request.data, partial=True)
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




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import IncrementRequest
from .serializers import IncrementRequestSerializer

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


