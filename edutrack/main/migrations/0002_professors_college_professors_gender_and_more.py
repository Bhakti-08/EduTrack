# Generated by Django 4.1.7 on 2023-04-29 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='professors',
            name='college',
            field=models.CharField(default='SGGS', max_length=100),
        ),
        migrations.AddField(
            model_name='professors',
            name='gender',
            field=models.CharField(default='male', max_length=10),
        ),
        migrations.AddField(
            model_name='students',
            name='college',
            field=models.CharField(default='SGGS', max_length=100),
        ),
        migrations.AddField(
            model_name='students',
            name='gender',
            field=models.CharField(default='female', max_length=10),
        ),
    ]
