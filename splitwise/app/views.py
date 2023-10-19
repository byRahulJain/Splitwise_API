# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.models import User

from .models import Expense, ExpenseParticipant
from .serializers import ExpenseSerializer, ExpenseParticipantSerializer, UserBalanceSerializer

# enpoints to create and view expense 

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    
    #custom logic to create expense and expense-participants object which hold detail about each expense
    def perform_create(self, serializer):
        expense = serializer.save()
        data = serializer.validated_data

        added_by = User.objects.get(username=data['added_by'])
        data['added_by'] = added_by.pk

        expense = Expense.objects.create(amount=data['amount'],type=data['type'],added_by=added_by)

        if data['type'] == 'Ex':
            for participant in data['participants']:
                if participant['username']==added_by.username:
                    continue
                username = participant['username']
                amount = participant.get('amount')
                user = User.objects.get(username=username)
                ExpenseParticipant.objects.create(expense=expense,user=user,amount=amount)

        elif data['type'] == 'Per':
            for participant in data['participants']:
                if participant['username']==added_by.username:
                    continue
                username = participant['username']
                percent = participant['amount']
                user = User.objects.get(username=username)
                amount = (percent / 100) * data['amount']
                ExpenseParticipant.objects.create(expense=expense,user=user,amount=amount)

        elif data['type'] == 'Eq':
            total = data['amount']
            participants = [participant['username'] for participant in data['participants']]
            no_of_users = len(participants)

            if added_by.username in participants:
                participants.remove(added_by.username)
            
            per_user = total / no_of_users

            for username in participants:
                user = User.objects.get(username=username)
                ExpenseParticipant.objects.create(expense=expense, user=user,amount=per_user)

# enpoints to view detail about participants share for each expense
class ExpenseParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExpenseParticipantSerializer 
    queryset = ExpenseParticipant.objects.all()

# Function Based Views to display User Balances
  
@api_view(['GET'])
def user_balances(request, username):
    user = User.objects.get(username=username)
    
    #Amount user owes to this user
    get_balances = ExpenseParticipant.objects.filter(expense__added_by=user).values('user','amount')
    gets = {}
    for balance in get_balances:
        from_user = User.objects.get(id=balance['user']).username
        amount = balance['amount']
        gets[from_user] = gets.get(from_user,0)+amount
    
    # Amounts this user owe to others
    owes_balances = ExpenseParticipant.objects.filter(user=user).values('expense__added_by','amount')
    owes = {}
    for balance in owes_balances:
        to_user = User.objects.get(id=balance['expense__added_by']).username
        amount = balance['amount']
        owes[to_user] = owes.get(to_user, 0) + amount

    results = []
    
    for to_user in set(owes) | set(gets):
        amount_owed = owes.get(to_user, 0)
        amount_get = gets.get(to_user, 0)
        
        net_amount = amount_get - amount_owed
        
        obj = {'user': to_user,'amount_owed': amount_owed,'amount_get': amount_get,  'net_amount': net_amount}
        
        results.append(obj)
    serializer = UserBalanceSerializer(results, many=True)
    return Response(serializer.data)

# Function Based Views to display All User Balances

@api_view(['GET'])
def all_user_balances(request):

    shared_expenses = ExpenseParticipant.objects.all()
    
    owes = {}
    gets = {}
    
    for exp in shared_expenses:
        from_user = exp.expense.added_by.username
        to_user = exp.user.username
        amount = exp.amount

        if to_user in owes:
            owes[to_user] += amount 
        else:
            owes[to_user] = amount

        if from_user in gets:
            gets[from_user] += amount
        else:
            gets[from_user] = amount

    results = []
    
    for username in set(owes) | set(gets):
        owed = owes.get(username, 0)
        get = gets.get(username, 0)
        net = get - owed
        data = {'user': username,'amount_owed': owed,'amount_get': get,'net_amount': net}
        results.append(data)
        
    serializer = UserBalanceSerializer(results,many=True)
    return Response(serializer.data)    
