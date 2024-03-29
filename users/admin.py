from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Barbers
from prices.models import Prices
from django import forms
from django.contrib.auth.forms import UserChangeForm


class PricesInline(admin.StackedInline):
    model = Prices
    fields = ['barber', 'cut_price', 'cut_description', 'cut_photo']


class FormUser(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(FormUser, self).__init__(*args, **kwargs)

        request = self.Meta.formfield_callback.keywords['request']

        if request.user.type == 'dono':
            self.fields['type'].disabled = False
        else:
            self.fields['type'].disabled = True

        if request.user.type == 'cliente':
            self.fields['type'].disabled = True
            self.fields['is_owner'].disabled = True
            self.fields['owner_company'].disabled = True


class UserProfileAdmin(UserAdmin):
    ordering = ['id']
    fieldsets = ('Informações do Usuário', {'fields': ('username', 'type', 'is_owner', 'owner_company', 'password',
                                                       'full_name', 'email', 'description', 'image')}),
    form = FormUser
    search_fields = ['email', 'full_name', 'username']
    list_display = ['id', 'email', 'full_name', 'username']
    list_display_links = ['id', 'email']


class FormBarber(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(FormBarber, self).__init__(*args, **kwargs)

        request = self.Meta.formfield_callback.keywords['request']

        if request.user.type != 'dono':
            self.fields['company'].disabled = True
            self.fields['barber'].disabled = True
            self.fields['password'].disabled = True
            self.fields['email_barber'].disabled = True
            self.fields['profile_photo'].disabled = True


class BarbersAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações do barbeiro', {'fields': ('company', 'barber', 'password', 'email_barber', 'profile_photo')}),
    )
    list_display = ['id', 'company', 'barber', 'email_barber']
    list_filter = ['company']
    list_display_links = ['company', 'barber']
    search_fields = ['barber__username']
    form = FormBarber

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'barber':
            kwargs['queryset'] = UserProfile.objects.filter(type='barbeiro')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Barbers, BarbersAdmin)
