# Generated by Django 3.1 on 2021-01-27 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learningapp', '0006_studyplan_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='daflearned',
            name='created_on',
            field=models.DateField(blank=True, null=True),
        ),
    ]
