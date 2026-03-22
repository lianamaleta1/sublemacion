let carrito={}

function agregarProducto(id){

    carrito[id] = 1
    renderCantidad(id)

    fetch("/ajax/agregar-carrito/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: "producto_id=" + id
    })
    .then(res => res.json())
    .then(data => {

        if(data.success){

            let contador = document.getElementById("cart-count")

            if(contador){
                contador.innerText = data.total_items
            }

        }

    })

}

function renderCantidad(id){

let contenedor = document.getElementById("carrito-"+id)

contenedor.innerHTML = `

<div class="cantidad-control">

<button onclick="cambiarCantidad(${id},-1)">-</button>

<span id="cantidad-${id}">1</span>

<button onclick="cambiarCantidad(${id},1)">+</button>

</div>

`

}

function cambiarCantidad(id, valor){

    carrito[id] += valor

    fetch("/ajax/agregar-carrito/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: "producto_id=" + id
    })

    if(carrito[id] <= 0){

        delete carrito[id]

        document.getElementById("carrito-"+id).innerHTML=
        `<button class="btn btn-carrito"
        onclick="agregarProducto(${id})">
        🛒 Añadir a la cesta
        </button>`

        return
    }

    document.getElementById("cantidad-"+id).innerText=carrito[id]

}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            if (cookie.trim().startsWith(name + '=')) {
                cookieValue = cookie.trim().substring(name.length + 1);
            }
        });
    }
    return cookieValue;
}