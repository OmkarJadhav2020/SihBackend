from rest_framework import serializers
from .models import User
from .models import ProjectProposal

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
