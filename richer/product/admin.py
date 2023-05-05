from django.contrib import admin

# Register your models here.
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'color', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'color', 'gender')
    list_editable = ('is_published',)
    list_filter = ('cat_id', 'is_published')
    prepopulated_fields = {"slug": ("title", "color")}

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name", )}

class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')
    list_display_links = ('id', 'product')
    search_fields = ('product',)



admin.site.register(Product, ProductAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Picture, PictureAdmin)
