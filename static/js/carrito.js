let carrito = {}

const data = document.getElementById("data-carrito")

if(data){
    carrito = JSON.parse(data.textContent)
}

 
function agregarProducto(id){
    
    carrito[id] = 1

    renderCantidad(id)
   
   fetch(URL_AGREGAR_CARRITO, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({
        producto_id: id,
        cantidad: 1
    })
})
.then(res => res.json())
.then(data => {

    if(data.success){

        let contador = document.getElementById("cart-count")

        if(contador){
            contador.innerText = data.total_items
        }

    } else {
        console.log("Error:", data.error)
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
        body: "producto_id=" + id + "&cantidad=" + valor  // 👈 AQUÍ
    })

    if(carrito[id] <= 0){

        delete carrito[id]

        document.getElementById("carrito-"+id).innerHTML=
        `<button class="btn btn-warning"
        onclick="agregarProducto(${id})">
        🛒 Añadir
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

window.onload = function(){

    for(let id in carrito){

        renderCantidad(id)

        document.getElementById("cantidad-"+id).innerText = carrito[id]

    }

}