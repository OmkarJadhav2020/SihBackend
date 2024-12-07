from django.contrib.auth import authenticate, login ,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer,ProjectProposalSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from .models import ProjectProposal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User

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

class GetList(APIView):
    def get(self,request):
        investigators = User.objects.filter(role="investigator").values("id","username")
        return Response({"data":investigators},status=status.HTTP_200_OK)



class ProposalViewSet(APIView):
    def get(self,request):
        return Response({"msg":"this is working"})
    
    def post(self,request):
        serializer = ProjectProposalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Project Proposal Submitted Successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

