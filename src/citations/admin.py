from django.contrib import admin
from .models import (Citation, Abstract, Database, Descriptor, Identifier, 
                     Keyword, PublicationType)


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ('pmid', 'status', )


@admin.register(Abstract)
class AbstractAdmin(admin.ModelAdmin):
    list_display = ('pmid', 'source')


@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('pmid', 'name')


@admin.register(Descriptor)
class DescriptorAdmin(admin.ModelAdmin):
    list_display = ('pmid', 'num')


@admin.register(Identifier)
class IdentifierAdmin(admin.ModelAdmin):
    list_display = ('pmid', 'namespace')


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('pmid', 'owner')


@admin.register(PublicationType)
class PublicationTypeAdmin(admin.ModelAdmin):
    list_display = ('pmid', 'value')