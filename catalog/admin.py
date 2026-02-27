from django.contrib import admin
from .models import Categoria, Producto, Resena, Pedido, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0 
    readonly_fields = ('producto', 'cantidad', 'precio') 

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'total', 'pagado')
    list_filter = ('fecha', 'pagado')
    inlines = [DetallePedidoInline] 

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria', 'nivel_cuidado')
    list_filter = ('categoria', 'nivel_cuidado', 'ambiente')
    search_fields = ('nombre',)

admin.site.register(Categoria)
