# Generated by Django 3.0.6 on 2020-05-27 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveysAdmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='choice_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='question',
            name='survey_id',
            field=models.CharField(max_length=20),
        ),
    ]