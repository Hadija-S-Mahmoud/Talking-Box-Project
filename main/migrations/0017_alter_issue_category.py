# Generated by Django 5.0.6 on 2024-07-16 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_issue_progress_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='category',
            field=models.CharField(choices=[('Health', 'Health'), ('Water & Sanitation', 'Water & Sanitation'), ('Fires', 'Fires'), ('Children & Minors', 'Children & Minors'), ('Electricity & Power', 'Electricity & Power'), ('Criminal Activities', 'Criminal Activities'), ('Roads & Infrastructure', 'Roads & Infrastructure')], max_length=50),
        ),
    ]
