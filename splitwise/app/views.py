# views.py

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import Expense, UserProfile
from .serializers import ExpenseSerializer, UserBalanceSerializer, SimplifiedBalanceSerializer
from .services import ExpenseService, SimplifiedBalanceService
import numpy as np


class UserBalanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserBalanceSerializer 
    queryset = UserProfile.objects.all()
    lookup_field = "user__username"

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    
    def create(self, request, *args, **kwargs):
        service = ExpenseService()  
        expense = service.create_expense(request.data)
        return Response({"message": "Expense created successfully."}, status=status.HTTP_201_CREATED)


class SimplifiedBalancesView(APIView):

  def get(self, request):
    all_users = UserProfile.objects.all()
    serializer = SimplifiedBalanceSerializer(all_users,many=True)
    
    net_balances = {}
    for balance in serializer.data:
        user = balance['user']
        net_balance = float(balance['net_balance'])
        net_balances[user] = net_balance

    
    service = SimplifiedBalanceService()  
    transactions = service.simplify(net_balances)
    return(Response(transactions))