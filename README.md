#  Proyecto: Selva Urbana - Tienda de Plantas

Bienvenido a mi proyecto final para el Módulo 8.
 Es una tienda online funcional donde podrá encontrar un catálogo de plantas,  un carrito de compras y el control del inventario.



### 1. Descargar el proyecto
Primero, debe clonar mi código desde GitHub abriendo una terminal y escribiendo:

```bash
git clone [https://github.com/Mpradinesa/selva-urbana-django.git](https://github.com/Mpradinesa/selva-urbana-django.git)
cd selva-urbana-django
```

### 2. Preparar el entorno

Para crear entorno de trabajo colocar en terminal los siguientes comandos en este orden :

* python -m venv venv
* .\venv\Scripts\activate

Instalar Django :

* pip install -r requirements.txt

Preparar la base de datos:

* python manage.py migrate

Poner a andar el servido local:

* python manage.py runserver

Para administrar la tienda :

* python manage.py createsuperuser   y seguir las instrucciones de terminal

Si hace algun cambio en el codigo despues de guardar los cambios usar los siguiente comandos:

* python manage.py makemigrations
* python manage.py migrate

Para evaluar las funciones de la tienda, use las siguientes cuentas:

* **Administrador:**
    * Usuario: `administrador`
    * Contraseña: `dasko123`
* **Cliente:**
    * Usuario: `Claudia`
    * Contraseña: `caser123`

Se puede ver: Solo en esa computadora entrando a http://127.0.0.1:8000/

Luego entrar a http://127.0.0.1:8000/admin para ver el modulo de administracion