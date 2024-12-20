# Generated by Django 4.2.7 on 2024-12-11 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_projectmanpower_manpowerdetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTravel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectid', models.IntegerField()),
                ('projectName', models.CharField(max_length=255)),
                ('projectCode', models.CharField(max_length=255)),
                ('principalAgency', models.CharField(max_length=255)),
                ('subAgency', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TravelDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=255)),
                ('fromPlace', models.CharField(max_length=255)),
                ('toPlace', models.CharField(max_length=255)),
                ('distance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('modeFare', models.DecimalField(decimal_places=2, max_digits=10)),
                ('noOfTrips', models.IntegerField()),
                ('travelExpense', models.DecimalField(decimal_places=2, max_digits=10)),
                ('noOfDays', models.IntegerField()),
                ('daRate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('totalDA', models.DecimalField(decimal_places=2, max_digits=10)),
                ('totalTADA', models.DecimalField(decimal_places=2, max_digits=10)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travelDetails', to='accounts.projecttravel')),
            ],
        ),
    ]
