from django.contrib import admin
from .models import Company, Schedules, Days
from django import forms


class Daysinline(admin.TabularInline):
    model = Days
    fields = ['day', 'hours_business']


class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
         ('Informações de Contato', {'fields': ('owner', 'employees', 'name', 'phone', 'instagram_link', 'facebook_link')}),
         ('Informações de Endereço', {'fields': ('cep', 'state', 'city', 'neighborhood', 'street')}),
                 )
    inlines = [Daysinline]
    filter_horizontal = ['owner', 'employees']


class FormSchedules(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSchedules, self).__init__(*args, **kwargs)

        request = self.Meta.formfield_callback.keywords['request']
        user = request.user
        if user.type == 'barbeiro' or user.type == 'desenvolvedor_dono':
            self.fields['confirmed_by_barber'].disabled = False
        else:
            self.fields['confirmed_by_barber'].disabled = True


class SchedulesAdmin(admin.ModelAdmin):
    list_display = ['client', 'chosen_barber', 'date', 'confirmed_by_barber']
    list_filter = ['confirmed_by_barber']
    form = FormSchedules


admin.site.register(Company, CompanyAdmin)
admin.site.register(Schedules, SchedulesAdmin)
