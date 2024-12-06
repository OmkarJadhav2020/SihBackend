from django.contrib.auth import authenticate, login ,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from .models import Proposal, ProposalImage, Project, ProjectImage, Report, Request, AuditTrail, Feedback
from .serializers import (
    ProposalSerializer, ProposalImageSerializer,
    ProjectSerializer, ProjectImageSerializer,
    ReportSerializer, RequestSerializer,
    AuditTrailSerializer, FeedbackSerializer
)
from django.http import JsonResponse

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        print(username,password)
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful', 'role': user.role,'token' : token.key,"id":user.id}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserInfoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        print(serializer.data)
        return Response(serializer.data)



class ProposalViewSet(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Proposal.objects.all()
        serializer = ProposalSerializer(queryset, many=True)  
        return JsonResponse(serializer.data, safe=False)  

    def post(self,request):
        print(request.data)
        # serializer = ProposalSerializer(data=request.data)
        # if serializer.is_valid():
        #     # Save the proposal data
        #     proposal = serializer.save()

        #     # Handle the image file upload
        #     if 'image' in request.FILES:
        #         image_file = request.FILES['image']
        #         ProposalImage.objects.create(proposal=proposal, image=image_file)

        #     return Response({
        #         "message": "Proposal created successfully.",
        #         "proposal": serializer.data
        #     }, status=status.HTTP_201_CREATED)

        # return Response({
        #     "message": "Invalid data.",
        #     "errors": serializer.errors
        # }, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

        


class ProposalImageViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProposalImage.objects.all()
    serializer_class = ProposalImageSerializer


class ProjectViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)  
        return JsonResponse(serializer.data, safe=False)  
        


class ProjectImageViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer


class ReportViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Report.objects.all()
        serializer = ReportSerializer(queryset, many=True)  
        return JsonResponse(serializer.data, safe=False)  


class RequestViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Request.objects.all()
        serializer = RequestSerializer(queryset, many=True)  
        return JsonResponse(serializer.data, safe=False)  


class AuditTrailViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = AuditTrail.objects.all()
        serializer = AuditTrailSerializer(queryset, many=True)  
        return JsonResponse(serializer.data, safe=False)  


class FeedbackViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Feedback.objects.all()
        serializer = FeedbackSerializer(queryset, many=True)  
        return JsonResponse(serializer.data, safe=False)  
