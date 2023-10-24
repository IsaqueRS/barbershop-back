from django.contrib import admin
from .models import Prices


class PricesAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações sobre o corte', {'fields': ('cut_price', 'cut_description', 'cut_photo')}),
    )
    list_display = ['id', 'cut_price', 'cut_description']
    list_display_links = ['id', 'cut_price']
    search_fields = ['cut_description']


admin.site.register(Prices, PricesAdmin)
