# Generated by Django 4.2.3 on 2023-09-17 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barber_shop', '0028_company_owner_is_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Logo da barbearia'),
        ),
    ]
