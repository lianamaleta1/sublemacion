from django.shortcuts import render, redirect,get_object_or_404
from .models import Producto, Pedido, PedidoItem
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def _obtener_pedido_activo(request):
    filtros = {"estado": "R"}
    if request.user.is_authenticated:
        filtros["usuario"] = request.user
    else:
        filtros["usuario__isnull"] = True
    return Pedido.objects.filter(**filtros).first()

def listarProductos(request):

    productos = Producto.objects.all()
    pedido = _obtener_pedido_activo(request)

    carrito = {}
    total_items = 0

    if pedido:
        for item in pedido.items.all():
            carrito[item.producto.id] = item.cantidad

        total_items = sum(item.cantidad for item in pedido.items.all())


    return render(request,'mercancia/list_product.html',{'productos':productos, 'carrito':json.dumps(carrito), 'total_items':total_items})

def vistaBasecarrito(request):
    pedido = _obtener_pedido_activo(request)

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
        if request.content_type == "application/json":
            payload = json.loads(request.body or "{}")
            producto_id = payload.get("producto_id")
            cantidad = int(payload.get("cantidad", 1))
        else:
            producto_id = request.POST.get("producto_id")
            cantidad = int(request.POST.get("cantidad", 1))

        if not producto_id:
            return JsonResponse({"success": False, "error": "producto_id requerido"}, status=400)

        cantidad = max(cantidad, -1000)

        filtros_pedido = {"estado": "R"}
        if request.user.is_authenticated:
            filtros_pedido["usuario"] = request.user
        else:
            filtros_pedido["usuario"] = None

        pedido, _ = Pedido.objects.get_or_create(**filtros_pedido)


        item, creado = PedidoItem.objects.get_or_create(
            pedido=pedido,
            producto_id=producto_id
        )


        nueva_cantidad = (0 if creado else item.cantidad) + cantidad
        if nueva_cantidad <= 0:
            item.delete()
        else:
            item.cantidad = nueva_cantidad
            item.save()


        # 🔥calcular total actualizado
        total_items = sum(i.cantidad for i in pedido.items.all())

        return JsonResponse({
            "success": True,
            "total_items": total_items
        })
   