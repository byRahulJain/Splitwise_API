from rest_framework import serializers
from .models import Expense, UserProfile

class ParticipantSerializer(serializers.Serializer):
    username = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class ExpenseSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, required=False)

    class Meta:
        model = Expense
        fields = ('id','type', 'amount', 'paid_by','participants')

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

class UserBalanceSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    owes_to = serializers.ReadOnlyField()
    gets_from = serializers.ReadOnlyField()
    net_balance = serializers.ReadOnlyField()

    class Meta:
         model = UserProfile
         fields = ['user', 'owes_to', 'gets_from','net_balance']

