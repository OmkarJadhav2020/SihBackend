# Generated by Django 4.2.7 on 2024-12-11 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_projectfund_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectfund',
            name='projectid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.project'),
        ),
    ]
