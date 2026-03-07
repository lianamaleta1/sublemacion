from .views import listarProductos
from django.urls import path

urlpatterns = [
    path('listar/',listarProductos,name='listar_productos'),
]