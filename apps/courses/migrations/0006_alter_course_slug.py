# Generated by Django 4.2.3 on 2023-10-23 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_slug_alter_course_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
