
let carrito = []

function agregarCarrito(nombre,precio){

carrito.push({
nombre:nombre,
precio:precio
})

document.getElementById("contador-carrito").innerText = carrito.length

alert("Producto agregado al carrito")

}