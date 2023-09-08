from django.contrib import admin
from .models import AbousUs, TermsOfUse


class AboutUsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações', {'fields': ('name', 'developed_by', 'description')}),
        ('Contato', {'fields': ('email', 'phone')})
    )


class TermsOfUseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Adicionar termos de uso', {'fields': ('title', 'terms_of_use')}),
    )
    list_display = ['title', 'terms_of_use']


admin.site.register(AbousUs, AboutUsAdmin)
admin.site.register(TermsOfUse, TermsOfUseAdmin)
