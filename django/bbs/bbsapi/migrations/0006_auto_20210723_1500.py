# Generated by Django 3.2.5 on 2021-07-23 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbsapi', '0005_auto_20210723_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='address',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='owner',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
