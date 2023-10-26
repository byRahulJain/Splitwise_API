# views.py

from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Expense, UserProfile
from .serializers import ExpenseSerializer, UserBalanceSerializer
from .services import ExpenseService


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

