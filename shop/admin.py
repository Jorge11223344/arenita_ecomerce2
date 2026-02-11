from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}
    list_display = ('nombre',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nombre','sku','peso_kg','categoria','precio','activo')
    list_filter = ('categoria','activo')
    search_fields = ('nombre','sku')
    prepopulated_fields = {'slug': ('nombre',)}

