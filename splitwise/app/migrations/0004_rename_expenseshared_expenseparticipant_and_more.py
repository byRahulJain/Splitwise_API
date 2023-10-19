# Generated by Django 4.2.6 on 2023-10-19 19:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_alter_expenseshared_amount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExpenseShared',
            new_name='ExpenseParticipant',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='balance',
        ),
    ]