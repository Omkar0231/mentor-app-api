# Generated by Django 5.1.7 on 2025-03-19 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_otpverification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]
