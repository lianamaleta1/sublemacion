from django.shortcuts import render, redirect,get_object_or_404
from .models import Producto, Pedido, PedidoItem
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def listarProductos(request):

    productos = Producto.objects.all()
    pedido = Pedido.objects.filter(
        #usuario=request.user,
        estado="R"
    ).first()

    carrito = {}
    total_items = 0

    if pedido:
        for item in pedido.items.all():
            carrito[item.producto.id] = item.cantidad

        total_items = pedido.items.count()


    return render(request,'mercancia/list_product.html',{'productos':productos, 'carrito':json.dumps(carrito), 'total_items':total_items})

def vistaBasecarrito(request):
    pedido = Pedido.objects.filter(
        usuario=request.user,
        estado="R"
    ).first()

    total_items = 0

    if pedido:
        total_items = sum(item.cantidad for item in pedido.items.all())
    

    return JsonResponse({
            "success": True,
            "total_items": total_items
        })

def vistaTazas(request):
    tazas=Producto.objects.filter(categoria='J')

    return render(request,'mercancia/tazas.html',{'tazas':tazas})


def vistaPullover(request):
    pullover=Producto.objects.filter(categoria='P')

    return render(request,'mercancia/pullover.html',{'pullover':pullover})

def agregar_carrito(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    pedido, creado = Pedido.objects.get_or_create(
        usuario=request.user,
        estado="R"
    )

    item, creado = PedidoItem.objects.get_or_create(
        pedido=pedido,
        producto=producto
    )

    if not creado:
        item.cantidad += 1
        item.save()

    return redirect("listar_productos")

def verCarrito(request):
    pedido= Pedido.objects.filter(estado="R").first()
    items=pedido.items.all() if pedido else []
    total=sum(item.subtotal() for item in items)

    return render(request, "mercancia/carrito.html",{"items":items,"total":total})


import json
  
def agregar_carrito_ajax(request):
    if request.method == "POST":
        producto_id = request.POST.get("producto_id")

        pedido, _ = Pedido.objects.get_or_create(
            usuario=request.user,
            estado="R"
        )

        item, creado = PedidoItem.objects.get_or_create(
            pedido=pedido,
            producto_id=producto_id
        )

        if not creado:
            item.cantidad += 1
        else:
            item.cantidad = 1

        item.save()

        # 🔥 calcular total actualizado
        total_items = sum(i.cantidad for i in pedido.items.all())

        return JsonResponse({
            "success": True,
            "total_items": total_items
        })
   