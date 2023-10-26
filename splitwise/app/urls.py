from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet,UserBalanceViewSet

router = DefaultRouter()
router.register('expenses', ExpenseViewSet)
router.register('balances',UserBalanceViewSet)

urlpatterns = [
    path('', include(router.urls))
]
