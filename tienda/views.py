from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto, Usuario, Carrito, CarritoProducto, Pedido, PedidoProducto
from .forms import Login, Register, Product, PerfilForm, UserChangeForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

def es_administrador(user):
    return user.is_staff

# Create your views here.
def index(request):
    producto = Producto.objects.all()
    return render(request, 'index.html', {
        'productos': producto
    })

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contraseña = form.cleaned_data['contraseña']
            
            try:
                user = Usuario.objects.get(email=correo)
            except Usuario.DoesNotExist:
                user = None

            if user and user.check_password(contraseña):  
                login(request, user) 
                messages.success(request, '¡Has iniciado sesión exitosamente!')
                return redirect('catalogo') 
            else:
                messages.error(request, 'Correo o contraseña incorrectos.')
                return redirect('login')  

    else:
        form = Login()
    
    return render(request, 'login_register.html', {'form_L': form})



def cerrar_se(request):
    logout(request)
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            correo = form.cleaned_data['correo']
            contraseña = form.cleaned_data['contraseña']
            contraseña2 = form.cleaned_data['contraseña2']
            
            if contraseña == contraseña2:
                user = Usuario.objects.create_user(username=username, email=correo, password=contraseña)
                user.save()
                messages.success(request, '¡Te has registrado exitosamente!')
                return redirect('login')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
    
    else:
        form = Register()

    return render(request, 'register.html', {'form_R': form})

@login_required(login_url= 'login')
def catalogo(request):
    productos = Producto.objects.all()
    usuario = Usuario.objects.all()
    return render(request, 'catalogo.html', {
        'productos': productos, 'usuario': usuario
    })

@login_required(login_url='login')
@user_passes_test(es_administrador)
def aggproducto(request):
    if request.method == 'GET':
        return render(request, 'admin/aggproductos.html', {
            'form_P': Product()
        })
    else:
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        especificaciones = request.POST.get('especificaciones')
        
        imagen1 = request.FILES.get('imagen1')
        imagen2 = request.FILES.get('imagen2')
        imagen3 = request.FILES.get('imagen3')
        imagen4 = request.FILES.get('imagen4')
        imagen5 = request.FILES.get('imagen5')

        default_image_path = 'uploads/default_P.png'
        
        if not imagen1:
            imagen1 = default_storage.open(default_image_path).name
        if not imagen2:
            imagen2 = default_storage.open(default_image_path).name
        if not imagen3:
            imagen3 = default_storage.open(default_image_path).name
        if not imagen4:
            imagen4 = default_storage.open(default_image_path).name
        if not imagen5:
            imagen5 = default_storage.open(default_image_path).name

        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad=cantidad,
            especificaciones=especificaciones,
            imagen1=imagen1,
            imagen2=imagen2,
            imagen3=imagen3,
            imagen4=imagen4,
            imagen5=imagen5,
        )

        producto.save()

        return redirect('aggproducto')

@login_required(login_url='login')
def detalle_producto(request, id_producto):
    producto = get_object_or_404(Producto, pk=id_producto)
    imagenes = [producto.imagen1, producto.imagen2, producto.imagen3, producto.imagen4, producto.imagen5]
    return render(request, 'productos.html', {'producto': producto, 'imagenes' : imagenes})

@login_required(login_url='login')
@user_passes_test(es_administrador)
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'admin/lista_productos.html', {'productos': productos})

@login_required(login_url='login')
@user_passes_test(es_administrador)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)

    if request.method == 'POST':
        form = Product(request.POST, request.FILES, instance=producto)
        
        if form.is_valid():
            form.save() 
            return redirect('catalogo')  
    else:
        form = Product(instance=producto)

    return render(request, 'admin/editar_producto.html', {'form': form, 'producto': producto})

@login_required(login_url='login')
@user_passes_test(es_administrador)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    producto.delete()
    return redirect('lista_productos')

@login_required(login_url='login')
def editar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('editar_perfil')
    else:
        form = PerfilForm(instance=request.user)

    return render(request, 'editar_perfil.html', {'form': form})

@login_required(login_url='login')
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    productos_en_carrito = carrito.carritoproducto_set.all()
    total_carrito = 0

    if request.method == 'POST' and 'comprar' in request.POST:
        pedido = Pedido.objects.create(user=request.user)
        for item in productos_en_carrito:
            item.producto.cantidad -= item.cantidad
            item.producto.save()
            PedidoProducto.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad
            )
        productos_en_carrito.delete()  # Limpiar el carrito después de la compra
        messages.success(request, 'Compra realizada con éxito.')
        return redirect('mis_pedidos')
    
    if request.method == 'POST':
        for item in productos_en_carrito:
            cantidad_nueva = int(request.POST.get(f'cantidad_{item.id}'))
            if cantidad_nueva <= item.producto.cantidad:
                item.cantidad = cantidad_nueva
                item.total = item.cantidad * item.producto.precio
                item.save()
    
        return redirect('carrito')

    for item in productos_en_carrito:
        item.total = item.cantidad * item.producto.precio
        total_carrito += item.total
        item.save()

    return render(request, 'carrito.html', {
        'productos_en_carrito': productos_en_carrito,
        'total_carrito': total_carrito,
    })


    for item in productos_en_carrito:
        item.total = item.cantidad * item.producto.precio
        total_carrito += item.total
        item.save()

    return render(request, 'carrito.html', {
        'productos_en_carrito': productos_en_carrito,
        'total_carrito': total_carrito,
    })




@login_required(login_url='login')
def agregar_al_carrito(request, producto_id):
    producto = Producto.objects.get(id_producto=producto_id)
    
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    
    cantidad = int(request.POST.get('cantidad', 1)) 

    carrito_producto, created = CarritoProducto.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 0}
    )
    
    carrito_producto.cantidad += cantidad
    carrito_producto.total = carrito_producto.cantidad * carrito_producto.producto.precio
    carrito_producto.save()

    return redirect('carrito')

@login_required(login_url='login')
def eliminar_del_carrito(request, item_id):
    carrito = Carrito.objects.get(user=request.user)
    try:
        item = CarritoProducto.objects.get(id=item_id, carrito=carrito)
        item.delete()
    except CarritoProducto.DoesNotExist:
        pass 

    return redirect('carrito')


@login_required(login_url='login')
@user_passes_test(es_administrador)
def lista_usuarios(request):
    Usuario = get_user_model()  # Obtiene el modelo de usuario personalizado
    usuarios = Usuario.objects.all()
    return render(request, 'admin/lista_usuarios.html', {'usuarios': usuarios})


@login_required(login_url='login')
@user_passes_test(es_administrador)
def editar_usuario(request, usuario_id):
    Usuario = get_user_model()  # Obtiene el modelo de usuario personalizado
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = UserChangeForm(request.POST, request.FILES, instance=usuario)
        
        if form.is_valid():
            form.save() 
            return redirect('lista_usuarios')
    else:
        form = UserChangeForm(instance=usuario)

    return render(request, 'admin/editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required(login_url='login')
@user_passes_test(es_administrador)
def eliminar_usuario(request, usuario_id):
    Usuario = get_user_model()  # Obtiene el modelo de usuario personalizado
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('lista_usuarios')

@login_required(login_url='login')
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user).order_by('-fecha')
    
    # Calculamos el total de cada pedido
    for pedido in pedidos:
        total_pedido = 0
        for pedido_producto in pedido.pedidoproducto_set.all():
            total_pedido += pedido_producto.cantidad * pedido_producto.producto.precio
        pedido.total = total_pedido  # Añadimos el total calculado al pedido
        
    return render(request, 'mis_pedidos.html', {'pedidos': pedidos})
