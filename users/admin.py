from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Barbers
from django import forms


class FormUser(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormUser, self).__init__(*args, **kwargs)

        request = self.Meta.formfield_callback.keywords['request']

        if request.user.type == 'desenvolvedor_dono':
            self.fields['type'].disabled = False
        else:
            self.fields['type'].disabled = True


class UserProfileAdmin(UserAdmin):
    ordering = ['id']
    fieldsets = ('Informações do Usuário', {'fields': ('username', 'type', 'owner', 'password', 'full_name', 'email',
                                                       'description', 'image')}),
    form = FormUser
    search_fields = ['email', 'full_name', 'username']
    list_display = ['id', 'email', 'full_name', 'username']
    list_display_links = ['id', 'email']


class BarbersAdmin(admin.ModelAdmin):
    list_display = ['company', 'barber', 'email_barber']
    list_filter = ['company']
    search_fields = ['barber__username']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'barber':
            kwargs['queryset'] = UserProfile.objects.filter(type='barbeiro')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Barbers, BarbersAdmin)
