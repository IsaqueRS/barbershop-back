# Generated by Django 4.2.3 on 2023-09-21 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_userprofile_owner_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='barbers',
            name='profile_photo',
            field=models.ImageField(blank=True, help_text='(opcional)', null=True, upload_to='', verbose_name='Foto do barbeiro'),
        ),
    ]