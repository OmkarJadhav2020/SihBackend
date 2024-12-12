# Generated by Django 4.2.7 on 2024-12-11 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_rename_actual_completion_date_projectcompletionreport_actualcompletiondate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRevision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
                ('project_code', models.CharField(max_length=100)),
                ('principal_agency', models.CharField(max_length=255)),
                ('project_leader', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('completion_date', models.DateField()),
                ('approved_objective', models.TextField()),
                ('approved_work_programme', models.TextField()),
                ('work_done_details', models.TextField()),
                ('total_approved_cost', models.DecimalField(decimal_places=2, max_digits=15)),
                ('revised_time_schedule', models.TextField(blank=True, null=True)),
                ('actual_expenditure', models.DecimalField(decimal_places=2, max_digits=15)),
                ('revised_cost_and_justification', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='projectcompletionreport',
            name='projectid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='completionprojects', to='accounts.project'),
        ),
    ]
