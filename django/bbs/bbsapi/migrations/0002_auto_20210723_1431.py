# Generated by Django 3.2.5 on 2021-07-23 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbsapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='expdate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='contract',
            name='increasedate',
            field=models.DateField(),
        ),
    ]
