from rest_framework import serializers
from .models import UserProfile, Expense, ExpenseParticipant
from rest_framework.fields import ChoiceField

# created for list of dictionaries in input
class ParticipantSerializer(serializers.Serializer):
    username = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

class ExpenseSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, required=False)

    class Meta:
        model = Expense
        fields = '__all__'

    #custom validations for amount
    def validate(self,data):
 
        expense_type = data.get('type')
        participants = data.get('participants')

        if expense_type == 'Ex':
            total = sum(participant['amount'] for participant in participants)
            if total != data['amount']:
                raise serializers.ValidationError("Totals do not match")
        elif expense_type == 'Per':
            total_percent = sum(participant['amount'] for participant in participants)
            if total_percent != 100:
                raise serializers.ValidationError('Percentages do not sum to 100%')
        elif expense_type == 'Eq':
            no_of_users = len(participants)
            if no_of_users == 0:
                raise serializers.ValidationError('No participants added')

        return data

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipant
        fields = '__all__'

# To diplay each user balance
class UserBalanceSerializer(serializers.Serializer):
    user = serializers.CharField()
    amount_owed = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount_get = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    