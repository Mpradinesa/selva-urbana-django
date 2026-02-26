from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Producto, Pedido, DetallePedido
from .cart import Cart
from .forms import RegistroForm
from django.contrib import messages

# --- VISTAS DE CATÁLOGO ---

def home(request):
    plantas = Producto.objects.all()
    return render(request, 'catalog/home.html', {'plantas': plantas})

# --- LÓGICA DEL CARRITO ---

@login_required(login_url='login')
def add_to_cart(request, producto_id):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=producto_id)
    
    id_producto = str(producto.id)
    cantidad_en_carrito = cart.cart.get(id_producto, {}).get('cantidad', 0)

    # Validación de stock inicial
    if cantidad_en_carrito + 1 > producto.stock:
        messages.error(request, f"Lo sentimos, la cantidad supera el stock disponible ({producto.stock} unidades).")
        return redirect('home')
    
    cart.add(producto)
    messages.success(request, f"¡{producto.nombre} se agregó al carrito!")
    return redirect('home')

def add_unit(request, producto_id):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=producto_id)
    
    id_prod = str(producto.id)
    cantidad_actual = cart.cart.get(id_prod, {}).get('cantidad', 0)
    
    if cantidad_actual + 1 > producto.stock:
        messages.error(request, f"No hay más stock disponible de {producto.nombre}.")
    else:
        cart.add(producto)
    return redirect('cart_detail')

def remove_unit(request, producto_id):
    cart = Cart(request)
    producto_id = str(producto_id)
    if producto_id in cart.cart:
        if cart.cart[producto_id]['cantidad'] > 1:
            cart.cart[producto_id]['cantidad'] -= 1
            cart.cart[producto_id]['total'] = str(float(cart.cart[producto_id]['precio']) * cart.cart[producto_id]['cantidad'])
        else:
            del cart.cart[producto_id]
        cart.save()
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'catalog/cart_detail.html', {'cart': cart})

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Carrito vaciado.")
    return redirect('cart_detail')

# --- AUTENTICACIÓN DE USUARIOS ---

def registro_usuario(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Registro exitoso! Bienvenida a Selva Urbana, {user.username}.")
            return redirect("home")
    else:
        form = RegistroForm()
    return render(request, "catalog/registro.html", {"form": form})

def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect("home")

# --- FINALIZAR COMPRA (CHECKOUT) ---

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('home')
        
    # 1. Crear el Pedido en la base de datos
    pedido = Pedido.objects.create(
        usuario=request.user,
        total=cart.get_total_price()
    )
    
    # 2. Procesar productos y descontar stock (Corregido: una sola vez)
    for item in cart.cart.values():
        producto = Producto.objects.get(id=item['producto_id'])
        
        # Restar stock real
        producto.stock -= int(item['cantidad'])
        producto.save()
        
        # Crear detalle del pedido
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item['cantidad'],
            precio=item['precio']
        )
    
    # 3. Vaciar carrito y mostrar éxito
    cart.clear()
    messages.success(request, "¡Tu compra se ha realizado con éxito!")
    return redirect('success_page', pedido_id=pedido.id)

def success_page(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'catalog/success.html', {'pedido': pedido})