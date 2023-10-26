# services.py

from django.db import transaction
from .models import UserProfile, Expense, ExpenseParticipant  
from .serializers import ExpenseSerializer

class ExpenseService:

    @transaction.atomic
    def create_expense(self, data):
        
        paid_by = UserProfile.objects.get(user__username=data['paid_by']) 
        data['paid_by'] = paid_by.pk
        paid_by_user= paid_by.user
        
        serializer = ExpenseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data  
        
        expense = Expense.objects.create(
            amount=data['amount'],
            type=data['type'],
            paid_by=paid_by
        )
        
        self._create_split(data['type'], paid_by_user, expense, data)
        return expense
    
    
    def _create_split(self, type, paid_by, expense, data):
        if type == 'Ex':
            for participant in data['participants']:
                if participant['username']==paid_by.username:
                    continue
                username = participant['username']
                amount = participant.get('amount')
                user = UserProfile.objects.get(user__username=username)
                ExpenseParticipant.objects.create(expense=expense,user=user,amount=amount)

        elif type == 'Per':
            for participant in data['participants']:
                if participant['username']==paid_by.username:
                    continue
                username = participant['username']
                percent = participant['amount']
                user = UserProfile.objects.get(user__username=username)
                amount = (percent / 100) * data['amount']
                ExpenseParticipant.objects.create(expense=expense,user=user,amount=amount)

        elif type == 'Eq':
            total = data['amount']
            participants = [participant['username'] for participant in data['participants']]
            no_of_users = len(participants)
            if paid_by.username in participants:
                participants.remove(paid_by.username)
            per_user = total / no_of_users
            for username in participants:
                user = UserProfile.objects.get(user__username=username)
                ExpenseParticipant.objects.create(expense=expense, user=user,amount=per_user)


class SimplifiedBalanceService:
    
    def simplify(self,balances):

        transactions = []
        positives = [user for user, balance in balances.items() if balance > 0]
        negatives = [user for user, balance in balances.items() if balance < 0]

        while positives and negatives:
            payer = positives[0]
            payee = negatives[0]
            amount = min(balances[payer], -balances[payee])
            transactions.append((payer, payee, amount))
            balances[payer] -= amount
            balances[payee] += amount

            if balances[payer] == 0:
                positives.pop(0)
            if balances[payee] == 0:
                negatives.pop(0)

        return transactions