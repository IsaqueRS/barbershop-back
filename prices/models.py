from django.db import models
# from users.models import Barbers


class Prices(models.Model):
    barber = models.ForeignKey('users.Barbers', verbose_name='Barbeiro', on_delete=models.CASCADE, null=True, blank=True)
    cut_price = models.FloatField('Preço do corte')
    cut_description = models.CharField('Tipo do corte')
    cut_photo = models.ImageField('Foto do corte', default='')

    def __str__(self):
        return str(f'{self.cut_description} - {self.cut_price}')

    class Meta:
        verbose_name = 'Preço do corte'
        verbose_name_plural = 'Preços dos cortes'
