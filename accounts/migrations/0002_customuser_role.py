# Generated by Django 5.1.7 on 2025-03-18 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('metor', 'Mentor'), ('user', 'User')], default='user', max_length=10),
        ),
    ]
