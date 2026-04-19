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
    path('eliminar_item/<int:item_id>/', eliminar_item, name='eliminar_item'),
    path('actualizar_item/<int:producto_id>/', actualizar_item_carrito, name='actualizar_item_carrito'),
    path('eliminar_item_carrito/<int:producto_id>/', eliminar_item_carrito, name='eliminar_item_carrito'),
    path('finalizar_compra/', finalizar_compra, name='finalizar_compra'),
]