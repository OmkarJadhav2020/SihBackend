from rest_framework import serializers
from .models import User
from .models import ProjectProposal,Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role','password']


class ProjectProposalSerializer(serializers.ModelSerializer):
    coordinator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    co_investigator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)  # Optional field

    class Meta:
        model = ProjectProposal
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    proposal = serializers.PrimaryKeyRelatedField(queryset=ProjectProposal.objects.all())
    assigned_investigators = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at']