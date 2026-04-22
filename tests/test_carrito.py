import pytest
from django.urls import reverse

def test_agregar_producto_inexistente(client):
    url = reverse('agregar_carrito_ajax')

    response = client.post(url, {
        'producto_id': 9999,
        'cantidad': 1
    })

    assert response.status_code in [400, 404]