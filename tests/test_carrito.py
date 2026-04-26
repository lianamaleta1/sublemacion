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
    payload = response.json()
    assert payload["success"] is True
    assert payload["total_items"] == 1

    item = PedidoItem.objects.get(producto=producto)
    assert item.cantidad == 1

