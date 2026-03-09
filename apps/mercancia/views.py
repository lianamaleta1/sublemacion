from django.shortcuts import render
from .models import *
# Create your views here.

def listarProductos(request):

    productos= Producto.objects.all()
    hello='acabado sencillo'

    return render(request,'mercancia/list_product.html',{'productos':productos,'hello':hello})