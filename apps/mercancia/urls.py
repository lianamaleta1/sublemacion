from .views import *
from django.urls import path

urlpatterns = [
    path('listar/',listarProductos,name='listar_productos'),
    path('tazas/',vistaTazas,name='vistaTazas'),
    path('pullover/',vistaPullover,name='vistaPullover'),
    path("carrito/agregar/<int:producto_id>/", agregar_carrito, name="agregar_carrito"),
    path('verCarrito/',verCarrito,name='verCarrito'),
    path("ajax/agregar-carrito/", agregar_carrito_ajax, name="agregar_carrito_ajax"),
    path('vistaBasecarrito/',vistaBasecarrito,name='vistaBasecarrito'),
]