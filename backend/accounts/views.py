from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProjectProposalSerializer, ProjectSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from .models import ProjectProposal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User,Project


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
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