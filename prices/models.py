from django.db import models
from users.models import Barbers


class Prices(models.Model):
    barber = models.ForeignKey(Barbers, verbose_name='Barbeiro', on_delete=models.CASCADE)
    cut_price = models.FloatField('Preço do corte')
    cut_description = models.CharField('Tipo do corte')

    def __str__(self):
        return str(f'{self.barber} - {self.cut_price}')

    class Meta:
        verbose_name = 'Preço do corte'
        verbose_name_plural = 'Preços dos cortes'
