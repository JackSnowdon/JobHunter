# Generated by Django 3.1.1 on 2020-09-25 17:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_profile_current_save'),
        ('portal', '0008_auto_20200925_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('date', models.DateField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connects', to='accounts.profile')),
            ],
        ),
    ]
