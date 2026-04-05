let carrito = {}

const data = document.getElementById("data-carrito")

if(data){
    carrito = JSON.parse(data.textContent)
}

function actualizarContador(totalItems) {
    const contador = document.getElementById("carrito-contador");
    if (!contador) return;

    contador.innerText = totalItems;
    contador.style.transform = "scale(1.3)";
    setTimeout(() => {
        contador.style.transform = "scale(1)";
    }, 200);
}

 
function agregarProducto(id){
    
        carrito[id] = 1

        renderCantidad(id)
   
        fetch("/ajax/agregar-carrito/", {
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

        if (data.success) {
            actualizarContador(data.total_items);
        }


    }) 
    .catch(error => console.error("Error:", error));

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


function vistaBasecarrito() {
    fetch("/vistaBasecarrito/")
    .then(res => res.json())
    .then(data => {
        actualizarContador(data.total_items);
    })
    .catch(error => console.error("Error:", error));
}
document.addEventListener("DOMContentLoaded", function() {
    vistaBasecarrito();
});


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
document.querySelectorAll(".btn-agregar").forEach(btn => {
    btn.addEventListener("click", function() {
        const id = Number(this.dataset.id);
        agregarProducto(id);
    });
});

window.agregarProducto = agregarProducto;
window.cambiarCantidad = cambiarCantidad;
window.vistaBasecarrito = vistaBasecarrito;
