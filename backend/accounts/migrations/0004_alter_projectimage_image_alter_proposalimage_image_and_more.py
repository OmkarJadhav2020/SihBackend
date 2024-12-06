# Generated by Django 4.2.7 on 2024-12-06 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_projectimage_image_alter_proposalimage_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimage',
            name='image',
            field=models.ImageField(upload_to='projects/'),
        ),
        migrations.AlterField(
            model_name='proposalimage',
            name='image',
            field=models.ImageField(upload_to='proposals/'),
        ),
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(upload_to='reports/'),
        ),
    ]