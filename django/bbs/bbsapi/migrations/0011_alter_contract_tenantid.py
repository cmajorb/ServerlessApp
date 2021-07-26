# Generated by Django 3.2.5 on 2021-07-24 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bbsapi', '0010_alter_contract_tenantid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='tenantid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant', to='bbsapi.tenant'),
        ),
    ]