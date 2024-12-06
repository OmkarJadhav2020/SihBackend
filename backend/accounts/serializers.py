from rest_framework import serializers
from .models import User,Proposal, ProposalImage, Project, ProjectImage, Report, Request, AuditTrail, Feedback

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role','password']



class ProposalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalImage
        fields = ['id', 'image']


class ProposalSerializer(serializers.ModelSerializer):
    images = ProposalImageSerializer(many=True, read_only=True)

    class Meta:
        model = Proposal
        fields = '__all__'


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    progress = serializers.FloatField(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
