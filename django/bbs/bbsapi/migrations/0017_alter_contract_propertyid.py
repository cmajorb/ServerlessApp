# Generated by Django 3.2.5 on 2021-07-25 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbsapi', '0016_alter_contract_propertyid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='propertyid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
