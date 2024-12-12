# Generated by Django 4.2.7 on 2024-12-11 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_projectcompletionreport2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectExtensionReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectid', models.IntegerField()),
                ('projectName', models.CharField(max_length=255)),
                ('projectCode', models.CharField(max_length=255)),
                ('implementingAgency', models.CharField(max_length=255)),
                ('projectLeader', models.CharField(max_length=255)),
                ('startDate', models.DateField()),
                ('scheduledCompletionDate', models.DateField()),
                ('approvedObjectives', models.TextField()),
                ('approvedWorkProgram', models.TextField()),
                ('workDetails', models.TextField()),
                ('revisedBarChart', models.FileField(blank=True, null=True, upload_to='bar_charts/')),
                ('extensionReason', models.TextField()),
                ('projectCost', models.TextField()),
                ('actualExpenditure', models.TextField()),
                ('formIII', models.FileField(blank=True, null=True, upload_to='forms/')),
                ('formIV', models.FileField(blank=True, null=True, upload_to='forms/')),
                ('formV', models.FileField(blank=True, null=True, upload_to='forms/')),
            ],
        ),
    ]