# Generated by Django 4.2.3 on 2023-08-01 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barber_shop', '0015_remove_days_end_days_end_time_alter_days_pause_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='days',
            name='end_pause_time',
            field=models.TimeField(blank=True, help_text='(opcional)', null=True, verbose_name='Fim da pause'),
        ),
    ]
