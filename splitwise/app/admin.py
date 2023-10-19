from django.contrib import admin
from .models import UserProfile,ExpenseParticipant, Expense
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Expense)
admin.site.register(ExpenseParticipant)