# Generated by Django 3.1.1 on 2020-09-25 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_job_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
