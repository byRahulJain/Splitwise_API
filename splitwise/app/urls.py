from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet,UserBalanceViewSet, SimplifiedBalancesView

router = DefaultRouter()
router.register('expenses', ExpenseViewSet)
router.register('balances',UserBalanceViewSet)

urlpatterns = [
    path('simplified-balances/', SimplifiedBalancesView.as_view(), name='simplified-balances'),
    path('', include(router.urls))
]
