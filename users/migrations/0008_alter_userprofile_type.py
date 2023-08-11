# Generated by Django 4.2.3 on 2023-08-04 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_userprofile_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(choices=[('cliente', 'Cliente'), ('barbeiro', 'Barbeiro'), ('desenvolvedor_dono', 'Desenvolvedor dono')], default='cliente', max_length=50, verbose_name='Tipo do usuário'),
        ),
    ]