# Generated by Django 4.0.4 on 2022-05-03 18:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quiz_company_name_alter_question_answerd_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answerd_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 3, 20, 29, 46, 770796)),
        ),
        migrations.AlterField(
            model_name='reportresult',
            name='on_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 3, 20, 29, 46, 771762)),
        ),
    ]