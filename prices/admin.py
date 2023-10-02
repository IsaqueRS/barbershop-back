from django.contrib import admin
from .models import Prices

class PricesAdmin(admin.ModelAdmin):
    list_display = ['id', 'barber', 'cut_price']

admin.site.register(Prices, PricesAdmin)
