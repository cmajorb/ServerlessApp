# Generated by Django 3.2.5 on 2021-07-24 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbsapi', '0013_alter_contract_tenantid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tenant',
            old_name='tenantname',
            new_name='name',
        ),
    ]