class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, producto):
        id = str(producto.id)
        if id not in self.cart:
            self.cart[id] = {
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'cantidad': 1,
            }
        else:
            self.cart[id]['cantidad'] += 1
            self.cart[id]['total'] = str(float(self.cart[id]['precio']) * self.cart[id]['cantidad'])
            
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, producto):
        id = str(producto.id)
        if id in self.cart:
            del self.cart[id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()
        
        
    def get_total_price(self):
        return sum(float(item['precio']) * item['cantidad'] for item in self.cart.values())