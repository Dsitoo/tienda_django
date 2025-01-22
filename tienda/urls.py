from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),  
    path('logout/', views.cerrar_se, name='cerrar_se'),
    path('register/', views.register, name='register'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('aggproducto/', views.aggproducto, name='aggproducto'),
    path('producto/<int:id_producto>/', views.detalle_producto, name='detalle_producto'),
    path('lista_productos/', views.lista_productos, name='lista_productos'),
    path('producto/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('producto/<int:producto_id>/agregar/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/<int:item_id>/eliminar/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'), 
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'), 
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
