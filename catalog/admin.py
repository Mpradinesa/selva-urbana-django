from django.contrib import admin
from .models import Categoria, Producto, Resena

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'nivel_cuidado', 'ambiente')
    list_filter = ('categoria', 'nivel_cuidado', 'ambiente')

admin.site.register(Categoria)
admin.site.register(Resena)