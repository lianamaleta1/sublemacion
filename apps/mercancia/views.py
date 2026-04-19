from django.shortcuts import render, redirect,get_object_or_404
from .models import Producto, Pedido, PedidoItem
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
# Create your views here.

logger=logging.getLogger('mercancia')
MAX_CANTIDAD_POR_PRODUCTO = 10

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
        if item.cantidad < MAX_CANTIDAD_POR_PRODUCTO:
            item.cantidad += 1
        item.save()

    return redirect("listar_productos")

def verCarrito(request):
    pedido= _obtener_pedido_activo(request)
    items=pedido.items.all() if pedido else []
    total=sum(item.subtotal() for item in items)

    return render(request, "mercancia/carrito.html",{"items":items,"total":total})


import json
  
def agregar_carrito_ajax(request):
    if request.method == "POST":

       
        if (request.content_type or "").startswith("application/json"):
            payload = json.loads(request.body or "{}")
            producto_id = payload.get("producto_id")
            cantidad_raw = payload.get("cantidad", 1)
        else:
            producto_id = request.POST.get("producto_id")
            cantidad_raw = request.POST.get("cantidad", 1)

        if not producto_id:
            return JsonResponse(
                {"success": False, "error": "producto_id requerido"},
                status=400
            )
        
        try:
            cantidad = int(cantidad_raw)
        except (TypeError, ValueError):
            return JsonResponse({"success": False, "error": "cantidad inválida"}, status=400)


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
        
        #se va a registrar un log con este texto en un arhivo txt llamado debug.log
        logger.info(f"El usuario {request.user} hizo un pedido {item}" )


        cantidad_actual = 0 if creado else item.cantidad
        nueva_cantidad = cantidad_actual + cantidad

        logger.info(f"El usuario tiene una nueva cantidad {nueva_cantidad}" )

        if nueva_cantidad > MAX_CANTIDAD_POR_PRODUCTO:
            return JsonResponse({
                "success": False,
                "error": f"Máximo {MAX_CANTIDAD_POR_PRODUCTO} unidades por producto",
                "cantidad_actual": cantidad_actual,
                "maximo_permitido": MAX_CANTIDAD_POR_PRODUCTO
            }, status=400)


        if nueva_cantidad <= 0:
            item.delete()
        else:
            item.cantidad = nueva_cantidad
            item.save()

        total_items = sum(i.cantidad for i in pedido.items.all())

        return JsonResponse({
            "success": True,
            "total_items": total_items
        })

    return JsonResponse(
        {"success": False, "error": "Método no permitido"},
        status=405
    )

def eliminar_item(request, item_id):
    item = get_object_or_404(PedidoItem, id=item_id)
    item.delete()
    return redirect('verCarrito')


def actualizar_item_carrito(request, producto_id):
    if request.method != "POST":
        return redirect("verCarrito")

    pedido = _obtener_pedido_activo(request)
    if not pedido:
        return redirect("verCarrito")

    item = get_object_or_404(PedidoItem, pedido=pedido, producto_id=producto_id)
    accion = request.POST.get("accion")

    if accion == "sumar":
        if item.cantidad < MAX_CANTIDAD_POR_PRODUCTO:
            item.cantidad += 1
            item.save()
    elif accion == "restar":
        item.cantidad -= 1
        if item.cantidad <= 0:
            item.delete()
        else:
            item.save()

    return redirect("verCarrito")

def eliminar_item_carrito(request, producto_id):
    if request.method != "POST":
        return redirect("verCarrito")

    pedido = _obtener_pedido_activo(request)
    if pedido:
        PedidoItem.objects.filter(pedido=pedido, producto_id=producto_id).delete()

    return redirect("verCarrito")

def finalizar_compra(request):
    pedido = _obtener_pedido_activo(request)
    if not pedido:
        return redirect("verCarrito")

    items = pedido.items.all()
    total = sum(item.subtotal() for item in items)

    if request.method == "POST":
        pedido.metodo_pago = request.POST.get("metodo_pago", "")
        pedido.estado = "P"
        pedido.save()
        return redirect("listar_productos")

    return render(request, "mercancia/pago.html", {"total": total, "items": items})