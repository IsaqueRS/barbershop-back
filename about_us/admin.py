from django.contrib import admin
from .models import AbousUs, TermsOfUse


class AboutUsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações', {'fields': ('name', 'developed_by', 'description')}),
        ('Contato', {'fields': ('email', 'phone')})
    )


admin.site.register(AbousUs, AboutUsAdmin)
admin.site.register(TermsOfUse)
