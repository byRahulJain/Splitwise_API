from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# One to One relationship with the User 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contactNo = models.CharField(max_length=12)
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
    added_by = models.ForeignKey(User,on_delete=models.CASCADE)

# expense can have many participants -> One to many with user
# for each participant, expense will have sub-expense -> One to many with expense
class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,validators=[MaxValueValidator(10000000)])

    