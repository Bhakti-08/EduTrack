# Generated by Django 4.2.1 on 2023-05-21 10:37

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_semester1_deletion_date_college_semester1_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionbank',
            name='created_at',
            field=models.DateTimeField(default=main.models.default_created_at),
        ),
        migrations.AddField(
            model_name='testdetails',
            name='created_at',
            field=models.DateTimeField(default=main.models.default_created_at),
        ),
    ]