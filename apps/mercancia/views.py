from django.shortcuts import render
from .models import Producto
from django.core.paginator import Paginator
# Create your views here.

def listarProductos(request):

    productos= Producto.objects.all()

    paginator = Paginator(productos, 12)

    page_number = request.GET.get("page")#que hace esta linea 

    productos = paginator.get_page(page_number)


    return render(request,'mercancia/list_product.html',{'productos':productos,})

def vistaTazas(request):
    tazas=Producto.objects.filter(categoria='J')

    return render(request,'mercancia/tazas.html',{'tazas':tazas})


def vistaPullover(request):
    pullover=Producto.objects.filter(categoria='P')

    return render(request,'mercancia/pullover.html',{'pullover':pullover})
