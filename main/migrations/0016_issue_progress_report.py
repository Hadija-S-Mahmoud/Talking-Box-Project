# Generated by Django 5.0.6 on 2024-07-15 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_issue_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='progress_report',
            field=models.TextField(blank=True, null=True),
        ),
    ]