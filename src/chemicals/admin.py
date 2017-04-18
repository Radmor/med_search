from django.contrib import admin
from .models import Chemical


@admin.register(Chemical)
class ChemicalAdmin(admin.ModelAdmin):
    list_display = ('idx', 'uid', 'name')