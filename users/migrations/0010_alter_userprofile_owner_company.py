# Generated by Django 4.2.3 on 2023-09-14 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barber_shop', '0028_company_owner_is_employee'),
        ('users', '0009_alter_userprofile_type_barbers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='owner_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_owner', to='barber_shop.company', verbose_name='Gerente de'),
        ),
    ]