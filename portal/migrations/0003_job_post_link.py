# Generated by Django 3.1.1 on 2020-09-25 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_job_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='post_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
