# Generated by Django 4.2.3 on 2023-08-31 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barber_shop', '0024_alter_days_working_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='number',
            field=models.CharField(default=1, verbose_name='Número do endereço'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='street',
            field=models.CharField(max_length=150, verbose_name='Rua'),
        ),
    ]