# Generated by Django 4.2.3 on 2023-10-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_learning_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_id',
            field=models.CharField(max_length=100),
        ),
    ]
