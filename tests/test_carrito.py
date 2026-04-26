import pytest
import json
from django.urls import reverse
from apps.mercancia.models  import Pedido, PedidoItem, Producto
from apps.mercancia.views import MAX_CANTIDAD_POR_PRODUCTO



@pytest.mark.django_db

def test_agregar_carrito_ajax_rechaza_cantidad_invalida(client, producto):
    url = reverse("agregar_carrito_ajax")
    response = client.post(
        url,
        data=json.dumps({"producto_id": producto.id, "cantidad": "Taza de cera"}),  # Cantidad inválida (excede el máximo permitido)
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"] == "cantidad inválida"
    




