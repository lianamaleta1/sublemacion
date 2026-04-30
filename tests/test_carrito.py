import json

import pytest
from django.urls import reverse

from apps.mercancia.models import PedidoItem, Producto, Pedido
from apps.mercancia.views import MAX_CANTIDAD_POR_PRODUCTO


@pytest.fixture
def producto():
    return Producto.objects.create(
        nombre="Taza test",
        precio=100,
        categoria="J",
        tipo="E",
    )


@pytest.mark.django_db
def test_agregar_carrito_ajax_agrega_producto(client, producto):
    url = reverse("agregar_carrito_ajax")
    response = client.post(
        url,
        data=json.dumps({"producto_id": producto.id, "cantidad": 1}),
        content_type="application/json",
    )

    assert response.status_code == 200
    payload = response.json()#lo convierte en un diccionario pq response devuelve un json de HTTP
    assert payload["success"] is True
    assert payload["total_items"] == 1

    item = PedidoItem.objects.get(producto=producto)
    assert item.cantidad == 1

#Cantidad máxima por producto
@pytest.mark.django_db
def test_agregar_producto_cantidad_invalida(client, producto):
    url = reverse("agregar_carrito_ajax")
    # Agregar la cantidad máxima permitida
    response = client.post(
        url,
        data=json.dumps({"producto_id": producto.id, "cantidad": "abc"}),
        content_type="application/json",
    )
    assert response.status_code == 400 # error del cliente (datos inválidos)
    payload = response.json()
    assert payload["success"] is False
    #assert payload["error"] == "cantidad inválida"
    #assert "cantidad inválida" in payload["error"]
    assert payload["error"] == "cantidad inválida", f"Error inesperado: {payload}"
    

import json
import pytest
from django.urls import reverse
from apps.mercancia.models import PedidoItem

@pytest.mark.django_db
def test_agregar_mismo_producto_dos_veces(client, producto):
    url = reverse("agregar_carrito_ajax")

    # Primera vez
    response1 = client.post(
        url,
        data=json.dumps({"producto_id": producto.id, "cantidad": 1}),
        content_type="application/json",
    )

    assert response1.status_code == 200 #todo correcto
    payload1 = response1.json()
    assert payload1["total_items"] == 1

    # Segunda vez (mismo producto)
    response2 = client.post(
        url,
        data=json.dumps({"producto_id": producto.id, "cantidad": 1}),
        content_type="application/json",
    )

    assert response2.status_code == 200
    payload2 = response2.json()
    assert payload2["total_items"] == 2

    # 🔍 Validación REAL de base de datos (clave)
    items = PedidoItem.objects.filter(producto=producto)

    assert items.count() == 1, "Debe existir un solo item para el producto"

    item = items.first()
    assert item.cantidad == 2, f"Cantidad incorrecta: {item.cantidad}"
    print(f"Cantidad en base de datos: {item.cantidad}")



#validar que un pedido pertenzca a un usuario 
#validar que si el producto tiene cantidad 1 y se quita 1 se elimine el pedido item 
# y no quede con cantidad 0
@pytest.mark.django_db
def test_pedidoItem_eliminado_sin_producto(client,producto):

    url = reverse("agregar_carrito_ajax")

    response2 = client.post(
        url,
        data=json.dumps({"producto_id": producto.id, "cantidad": 0}),
        content_type="application/json",
    )

    assert response2.status_code == 200
    payload2 = response2.json()
    assert payload2["success"] is True
    assert payload2["total_items"] == 0
    
   



#Agregar producto,Luego enviar cantidad = 0,Validar:, El item desaparece,El pedido sigue existiendo


