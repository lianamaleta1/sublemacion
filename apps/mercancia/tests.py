from django.test import TestCase
from mercancia.models import Producto
# Create your tests here.
def vistaTazas(request):
    tazas=Producto.objects.filter(categoria='Jarra')

    print(tazas)