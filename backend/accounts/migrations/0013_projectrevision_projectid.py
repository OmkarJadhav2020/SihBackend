# Generated by Django 4.2.7 on 2024-12-11 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_projectrevision_projectcompletionreport_projectid'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectrevision',
            name='projectid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectREvision', to='accounts.project'),
        ),
    ]