from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
import os

# Create your models here.
class Usuario(AbstractUser):
    foto_perfil = models.ImageField(upload_to='uploads/avatars/', default='uploads/avatars/default_A.svg')
    biografia = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
    
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, default='Producto')
    descripcion = models.CharField(max_length=400 ,default='Descripcion')
    precio = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    cantidad = models.IntegerField(default=0)
    imagen1 = models.ImageField(upload_to='uploads/', blank=True, null=True, default='uploads/default_P.png')
    imagen2 = models.ImageField(upload_to='uploads/', blank=True, null=True, default='uploads/default_P.png')
    imagen3 = models.ImageField(upload_to='uploads/', blank=True, null=True, default='uploads/default_P.png')
    imagen4 = models.ImageField(upload_to='uploads/', blank=True, null=True, default='uploads/default_P.png')
    imagen5 = models.ImageField(upload_to='uploads/', blank=True, null=True, default='uploads/default_P.png')
    especificaciones = models.CharField(max_length=300 ,default='Especificaciones')

    def __str__(self):
        return self.nombre
    
    def delete(self, *args, **kwargs):
        default_image_name = 'default_P.png'

        imagenes = [self.imagen1, self.imagen2, self.imagen3, self.imagen4, self.imagen5]

        for imagen in imagenes:
            if imagen:
                imagen_name = os.path.basename(imagen.path)
                if imagen_name != default_image_name and os.path.isfile(imagen.path):
                    os.remove(imagen.path)

        super().delete(*args, **kwargs)


class Carrito(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    productos = models.ManyToManyField(Producto, through='CarritoProducto') 

    def __str__(self):
        return f"Carrito de {self.user.username}"

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE) 
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    cantidad = models.IntegerField(default=1) 

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"

class Pedido(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido de {self.user.username} - {self.fecha}"

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"
