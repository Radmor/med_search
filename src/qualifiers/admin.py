from django.contrib import admin

from .models import Qualifier


@admin.register(Qualifier)
class QualifierAdmin(admin.ModelAdmin):
    list_display = ('num', 'sub')
