from django.contrib import admin

# Register your models here.
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'color', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'color', 'gender')
    list_editable = ('is_published',)
    list_filter = ('cat_id', 'is_published')

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Catalog, CatalogAdmin)
