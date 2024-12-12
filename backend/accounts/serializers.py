from rest_framework import serializers
from .models import User
from .models import ProjectProposal,Project
from .models import *

from rest_framework.parsers import MultiPartParser, FormParser



from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()



class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def validate_role(self, value):
        """Ensure role is valid."""
        if value not in dict(User.ROLES).keys():
            raise serializers.ValidationError("Invalid role selected.")
        return value

    def create(self, validated_data):
        """Create a new user."""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user

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


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'name', 'description', 'file', 'project', 'created_at']



class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'name', 'description', 'reply', 'project_id', 'feedback_image', 'investigator']




class FundRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundRequisition
        fields = [
            'id',
            'project',
            'total_approved_cost',
            'total_fund_received_as_on',
            'interest_earned',
            'expenditure_incurred_till_date',
            'balance_fund_available_as_on_date',
            'fund_provision_in_corresponding_year',
            'fund_required_for_year_period',
        ]





class ExpenditureQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenditureQuestion
        fields = ['id', 'indicator', 'question']

class ExpenditureStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenditureStatement
        fields = [
            'id',
            'project',
            'project_code',
            'company_institute_name',
            'quarter_ending',
            'total_approved_cost',
            'sanctioned_provision_in_year',
            'expenditure_incurred_previous_year',
            'expenditure_up_to_previous_quarter',
            'expenditure_in_present_quarter',
            'progressive_expenditure_till_date',
        ]





class QuarterlyExpenditureStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterlyExpenditureStatement
        fields = [
            'id',
            'project',
            'project_code',
            'company_institute_name',
            'quarter_ending',
            'equipment_name',
            'supplier_name',
            'number_of_units',
            'unit_value',
            'total_value',
            'total_approved_cost',
            'progressive_capital_expenditure',
            'building_or_land_area',
            'associate_finance_officer_name',
            'associate_finance_officer_designation',
            'associate_finance_officer_signature',
            'project_leader_name',
            'project_leader_designation',
            'project_leader_signature',
        ]





# class ProjectCompletionReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectCompletionReport
#         fields = [
#             'id',
#             'project',
#             'title',
#             'project_code',
#             'date_of_commencement',
#             'approved_completion_date',
#             'actual_completion_date',
#             'objectives',
#             'work_programme',
#             'details_of_work_done',
#             'objectives_fulfilled',
#             'reasons_for_incomplete_scope',
#             'need_for_further_study',
#             'conclusions_and_recommendations',
#             'scope_of_application',
#             'associated_persons',
#             'final_expenditure_statement',
#         ]



class FinanceAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceAnalysis
        fields = [
            'id',
            'project',
            'total_approved_cost',
            'total_fund_received',
            'total_used_cost',
            'interest_earned',
            'balance_available',
            'cost_used_last_year',
            'cost_used_previous_quarter',
            'cost_used_till_present_quarter_end',
            'overall_expenditure',
            'number_of_units',
            'unit_values',
            'total_value',
            'created_at',
            'updated_at',
        ]




class IncrementRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncrementRequest
        fields = [
            'id',
            'project',
            'increment_type',
            'increment_value',
            'feedback_message',
            'feedback_image',
            'requested_by',
            'created_at',
            'updated_at',
            'status',
        ]


# class ProjectCompletionReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectCompletionReport
#         fields = "__all__"
        


from rest_framework import serializers
from .models import ProjectRevision

class ProjectRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRevision
        fields = "__all__"



from rest_framework import serializers
from .models import Project, Item

from rest_framework import serializers
from .models import ProjectFund, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['project']  # Exclude `project` as it will be handled programmatically


class ProjectFundSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = ProjectFund
        fields = "__all__"

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("The 'items' field cannot be empty.")
        return value

    def create(self, validated_data):
        # Extract `items` data and create the project
        items_data = validated_data.pop('items', [])
        project = ProjectFund.objects.create(**validated_data)

        # Create associated items
        for item_data in items_data:
            Item.objects.create(project=project, **item_data)
        return project

    def update(self, instance, validated_data):
        # Update the project
        items_data = validated_data.pop('items', [])
        instance.projectid = validated_data.get('projectid', instance.projectid)
        instance.projectName = validated_data.get('projectName', instance.projectName)
        instance.projectCode = validated_data.get('projectCode', instance.projectCode)
        instance.companyName = validated_data.get('companyName', instance.companyName)
        instance.statementPeriod = validated_data.get('statementPeriod', instance.statementPeriod)
        instance.save()

        # Update associated items
        instance.items.all().delete()  # Remove old items
        for item_data in items_data:
            Item.objects.create(project=instance, **item_data)
        return instance





from rest_framework import serializers
from .models import EndorsementForm

class EndorsementFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndorsementForm
        fields = "__all__"



from rest_framework import serializers
from .models import QuarterlyStatusReport

class QuarterlyStatusReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterlyStatusReport
        fields = "__all__"



from rest_framework import serializers
from .models import ProjectCompletionReport2

class ProjectCompletionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCompletionReport2
        fields = "__all__"

from rest_framework import serializers
from .models import Fund

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'


class TimelineTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineTask
        fields = '__all__'

        
from rest_framework import serializers
from .models import ProjectExtensionReport

class ProjectExtensionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectExtensionReport
        fields = "__all__"




from rest_framework import serializers
from .models import ProjectRevisionTwo

class ProjectRevisionTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRevisionTwo
        fields = "__all__"




from rest_framework import serializers
from .models import ProjectEquipment, EquipmentDetail

class EquipmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentDetail
        exclude = ('project',)  # Exclude the 'project' field from being required
class ProjectEquipmentSerializer(serializers.ModelSerializer):
    equipmentDetails = EquipmentDetailSerializer(many=True)

    class Meta:
        model = ProjectEquipment
        fields = "__all__"

    def create(self, validated_data):
        equipment_data = validated_data.pop('equipmentDetails')  # Extract equipment details
        project = ProjectEquipment.objects.create(**validated_data)  # Create the main project
        for equipment in equipment_data:
            EquipmentDetail.objects.create(project=project, **equipment)  # Link each equipment to the project
        return project
    


from rest_framework import serializers
from .models import ProjectManpower, ManpowerDetail

class ManpowerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManpowerDetail
        # fields = '__all__'
        exclude = ('project',)

class ProjectManpowerSerializer(serializers.ModelSerializer):
    manpowerDetails = ManpowerDetailSerializer(many=True)

    class Meta:
        model = ProjectManpower
        fields = '__all__'

    def create(self, validated_data):
        manpower_details_data = validated_data.pop('manpowerDetails', [])
        project = ProjectManpower.objects.create(**validated_data)
        for detail_data in manpower_details_data:
            ManpowerDetail.objects.create(project=project, **detail_data)
        return project





from rest_framework import serializers
from .models import ProjectTravel, TravelDetail

class TravelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelDetail
        # fields = '__all__'
        exclude = ('project',)


class ProjectTravelSerializer(serializers.ModelSerializer):
    travelDetails = TravelDetailSerializer(many=True)

    class Meta:
        model = ProjectTravel
        fields = '__all__'

    def create(self, validated_data):
        travel_details_data = validated_data.pop('travelDetails', [])
        project = ProjectTravel.objects.create(**validated_data)
        for travel_data in travel_details_data:
            TravelDetail.objects.create(project=project, **travel_data)
        return project
