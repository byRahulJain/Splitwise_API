from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet,ExpenseParticipantViewSet

router = DefaultRouter()
router.register('expenses', ExpenseViewSet)
router.register('shares', ExpenseParticipantViewSet)

urlpatterns = [
    path('balances/<str:username>',views.user_balances,name='show-balances'),
    path('balances/',views.all_user_balances,name='show-all-balances'),
    path('', include(router.urls))
]
