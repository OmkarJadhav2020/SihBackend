# Generated by Django 4.2.7 on 2024-12-07 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_projectproposal_remove_feedback_project_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectproposal',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
