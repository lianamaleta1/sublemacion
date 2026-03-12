
let carrito = {}

function agregarProducto(id){

carrito[id] = 1

renderCantidad(id)

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

function cambiarCantidad(id,valor){

carrito[id] += valor

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