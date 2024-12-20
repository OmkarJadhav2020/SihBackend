# Generated by Django 4.2.7 on 2024-12-09 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='budget',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(upload_to='reports/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='accounts.project')),
            ],
        ),
    ]
