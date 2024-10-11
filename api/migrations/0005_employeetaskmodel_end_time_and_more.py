# Generated by Django 4.2.7 on 2023-12-24 20:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_remove_employeemodel_employee_comment_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeetaskmodel",
            name="end_time",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Время окончания"
            ),
        ),
        migrations.AddField(
            model_name="employeetaskmodel",
            name="start_time",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Время начала"
            ),
        ),
    ]
