# Generated by Django 4.2.7 on 2023-12-20 19:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_remove_taskmodel_employee_comment_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employeemodel",
            name="employee_comment",
        ),
        migrations.AddField(
            model_name="employeetaskmodel",
            name="employee_comment",
            field=models.TextField(null=True, verbose_name="Комментарий работника"),
        ),
    ]
