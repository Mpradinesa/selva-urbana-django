from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    NIVELES = [('Fácil', 'Fácil'), ('Medio', 'Medio'), ('Experto', 'Experto')]
    AMBIENTES = [('Interior', 'Interior'), ('Exterior', 'Exterior'), ('Mixto', 'Interior/Exterior')]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nivel_cuidado = models.CharField(max_length=10, choices=NIVELES, default='Fácil')
    ambiente = models.CharField(max_length=10, choices=AMBIENTES, default='Interior')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Pedido(models.Model):  # <-- Ahora está fuera de Producto, como debe ser
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Resena(models.Model):
    producto = models.ForeignKey(Producto, related_name='resenas', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)