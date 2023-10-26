from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db.models import Sum

# One to One relationship with the User 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contactNo = models.CharField(max_length=12)

    @property
    def total_gets(self):
        return self.expenses_paid.aggregate(total=Sum('expenseparticipant__amount'))['total'] or 0

    @property
    def total_owes(self):
       return self.expenses_owed.aggregate(total=Sum('amount'))['total'] or 0

    @property
    def net_balance(self):
        return self.total_gets-self.total_owes

    @property
    def owes_to(self):
       owes = self.expenses_owed.values('expense__paid_by__user__username').annotate(sum=Sum('amount'))
       return {item['expense__paid_by__user__username']: item['sum'] for item in owes}
       
    @property
    def gets_from(self):
       gets = self.expenses_paid.values('expenseparticipant__user__user__username').annotate(sum=Sum('expenseparticipant__amount'))  
       return {item['expenseparticipant__user__user__username']: item['sum'] for item in gets}

    def __str__(self):
        return self.user.username

# One user many expenses -> One to many with user
class Expense(models.Model):
    TYPE_CHOICES = (
        ('Eq', 'Equal'),
        ('Ex', 'Exact'),
        ('Per', 'Percentage'),
    )
    type = models.CharField(choices=TYPE_CHOICES,max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='expenses_paid')

# expense can have many participants -> One to many with user
# for each participant, expense will have sub-expense -> One to many with expense
class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='expenses_owed')
    amount = models.DecimalField(max_digits=10, decimal_places=2,validators=[MaxValueValidator(10000000)])

    