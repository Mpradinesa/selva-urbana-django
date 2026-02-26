from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('agregar/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('vaciar/', views.clear_cart, name='clear_cart'),
    
    # Rutas de usuario
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='catalog/login.html'), name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    
    # Ruta de compra final
    path('finalizar/', views.checkout, name='checkout'),
    path('carrito/sumar/<int:producto_id>/', views.add_unit, name='add_unit'),
    path('carrito/restar/<int:producto_id>/', views.remove_unit, name='remove_unit'),
    path('exito/<int:pedido_id>/', views.success_page, name='success_page'), # Para el mensaje de éxito

]