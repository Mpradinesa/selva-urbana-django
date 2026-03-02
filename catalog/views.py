from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Producto, Pedido, DetallePedido, Categoria, Contacto # Unifiqué los imports
from .cart import Cart
from .forms import RegistroForm, ContactoForm # Unifiqué los imports de formularios
from django.contrib import messages

def home(request):
    # 1. Traemos TODOS los productos inicialmente
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    # 2. Filtro por Categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # 3. Filtro por precio (Orden)
    orden = request.GET.get('orden')
    if orden == 'barato':
        productos = productos.order_by('precio')
    elif orden == 'caro':
        productos = productos.order_by('-precio')

    # 4. Calcular total del carrito para el icono del navbar
    # Usamos el método de tu clase Cart si está disponible, o la sesión directamente
    cart = request.session.get('cart', {})
    total_items = sum(item['cantidad'] for item in cart.values()) if isinstance(cart, dict) else 0

    return render(request, 'catalog/home.html', {
        'plantas': productos, # Enviamos 'productos' pero el HTML lo recibe como 'plantas'
        'categorias': categorias,
        'cart_total_quantity': total_items,
        'categoria_actual': categoria_id, 
        'orden_actual': orden            
    })

# --- Las demás funciones se mantienen igual pero revisadas ---

@login_required(login_url='login')
def add_to_cart(request, producto_id):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=producto_id)
    id_producto = str(producto.id)
    
    # Verificamos stock antes de agregar
    cantidad_en_carrito = cart.cart.get(id_producto, {}).get('cantidad', 0)
    if cantidad_en_carrito + 1 > producto.stock:
        messages.error(request, f"Lo sentimos, solo quedan {producto.stock} unidades.")
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
        messages.error(request, f"No hay más stock disponible.")
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

def registro_usuario(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Bienvenida a Selva Urbana, {user.username}!")
            return redirect("home")
    else:
        form = RegistroForm()
    return render(request, "catalog/registro.html", {"form": form})

def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect("home")

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('home')
        
    pedido = Pedido.objects.create(
        usuario=request.user,
        total=cart.get_total_price()
    )
    
    for item in cart.cart.values():
        producto = Producto.objects.get(id=item['producto_id'])
        producto.stock -= int(item['cantidad'])
        producto.save()
        
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item['cantidad'],
            precio=item['precio']
        )
    
    cart.clear()
    messages.success(request, "¡Tu compra se ha realizado con éxito!")
    return redirect('success_page', pedido_id=pedido.id)

def success_page(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'catalog/success.html', {'pedido': pedido})

def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Gracias! Tu mensaje ha sido enviado con éxito.')
            return redirect('home')
    else:
        form = ContactoForm()
    return render(request, 'catalog/contacto.html', {'form': form})