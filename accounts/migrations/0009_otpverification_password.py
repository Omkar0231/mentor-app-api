# Generated by Django 5.1.7 on 2025-03-19 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_customuser_age_remove_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpverification',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
