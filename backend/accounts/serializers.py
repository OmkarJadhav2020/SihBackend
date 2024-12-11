from rest_framework import serializers
from .models import User
from .models import ProjectProposal,Project
from .models import *

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





class ProjectCompletionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCompletionReport
        fields = [
            'id',
            'project',
            'title',
            'project_code',
            'date_of_commencement',
            'approved_completion_date',
            'actual_completion_date',
            'objectives',
            'work_programme',
            'details_of_work_done',
            'objectives_fulfilled',
            'reasons_for_incomplete_scope',
            'need_for_further_study',
            'conclusions_and_recommendations',
            'scope_of_application',
            'associated_persons',
            'final_expenditure_statement',
        ]



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
