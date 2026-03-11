from django.contrib import admin
# IMPORTANTE: Aquí incluimos ProductoImagen para que el código lo reconozca
from .models import Producto, Categoria, ProductoImagen 

# 1. Definimos el Inline PRIMERO (esto permite subir fotos dentro del producto)
class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 3  # Te dará 3 espacios listos para subir fotos adicionales

# 2. Configuración del Producto (Usa el Inline definido arriba)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # El Inline debe ir aquí dentro
    inlines = [ProductoImagenInline]
    
    # Columnas que verás en la lista de productos
    list_display = ('nombre', 'precio', 'stock', 'categoria', 'nivel_cuidado')
    
    # Filtros laterales para que encuentres tus plantas rápido
    list_filter = ('categoria', 'nivel_cuidado', 'ambiente')
    
    # Buscador por nombre
    search_fields = ('nombre',)
    
    # Ordenar por stock (las que tienen menos aparecen primero)
    ordering = ('stock',)

# 3. Registro de Categorías
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
