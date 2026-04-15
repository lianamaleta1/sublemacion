let carrito = {};

const data = document.getElementById("data-carrito");

if (data) {
    const contenido = data.textContent.trim();
    if (contenido) {
        carrito = JSON.parse(contenido);
    }
}
//Actualiza el número del carrito en navbar y aplica una animación rápida de escala para feedback visual.
function actualizarContador(totalItems) {   
    const contador = document.getElementById("carrito-contador");
    if (!contador) return;

    contador.innerText = totalItems;
    contador.style.transform = "scale(1.3)";
    setTimeout(() => {
        contador.style.transform = "scale(1)";
    }, 200);
}

/* Calcula el total de items en el carrito sumando las cantidades almacenadas localmente.
 Esto se usa para mantener el contador actualizado incluso si hay discrepancias con el servidor.*/
function obtenerTotalLocal() {
    return Object.values(carrito).reduce(
        (total, cantidad) => total + Number(cantidad || 0),
        0
    );
}

//Muestra un mensaje de error o información relacionado con el carrito. El mensaje desaparece automáticamente después de unos segundos.
function mostrarMensajeCarrito(mensaje) {
    let aviso = document.getElementById("carrito-mensaje");

    if (!aviso) {
        aviso = document.createElement("div");
        aviso.id = "carrito-mensaje";
        aviso.style.position = "fixed";
        aviso.style.top = "90px";
        aviso.style.right = "20px";
        aviso.style.zIndex = "9999";
        aviso.style.background = "#dc3545";
        aviso.style.color = "#fff";
        aviso.style.padding = "10px 14px";
        aviso.style.borderRadius = "8px";
        aviso.style.boxShadow = "0 4px 12px rgba(0,0,0,.2)";
        document.body.appendChild(aviso);
    }

    aviso.innerText = mensaje;
    clearTimeout(aviso._timeoutId);
    aviso._timeoutId = setTimeout(() => {
        aviso.remove();
    }, 2800);
}

/*“Repara” la UI con la cantidad real que viene del backend:
si cantidadActual <= 0, elimina el item local y vuelve a botón “Añadir”;
si es mayor, re-renderiza controles +/- y pone cantidad correcta*/

function sincronizarCantidadProducto(id, cantidadActual) {
    if (cantidadActual <= 0) {
        delete carrito[id];
        document.getElementById("carrito-"+id).innerHTML =
        `<button class="btn btn-warning"
        onclick="agregarProducto(${id})">
        🛒 Añadir
        </button>`;
        return;
    }

    carrito[id] = cantidadActual;
    renderCantidad(id);
    document.getElementById("cantidad-"+id).innerText = cantidadActual;
}

/* Dibuja los botones - y + y el <span> con la cantidad para un producto específico..*/
function renderCantidad(id) {
    const contenedor = document.getElementById("carrito-" + id);
    if (!contenedor) return;

    contenedor.innerHTML = `
        <div class="cantidad-control">
            <button onclick="cambiarCantidad(${id}, -1)">-</button>
            <span id="cantidad-${id}">1</span>
            <button onclick="cambiarCantidad(${id}, 1)">+</button>
        </div>
    `;
}
/*  Flujo al hacer clic en “Añadir”:

    Incrementa localmente (carrito[id] += 1) para respuesta inmediata.

    Renderiza controles y contador local.

    Envía POST JSON a /ajax/agregar-carrito/.

    Si backend responde OK: usa data.total_items.

    Si backend responde error (límite, etc): sincroniza cantidad real y muestra mensaje.

    Si hay error de red: muestra mensaje genérico y refresca contador desde servidor.


    “iniciar o añadir por primera vez desde el botón de compra”.
    
    */
 
function agregarProducto(id) {
    id = Number(id);

    carrito[id] = (carrito[id] || 0) + 1;

    renderCantidad(id);
    const cantidadEl = document.getElementById("cantidad-" + id);
    if (cantidadEl) {
        cantidadEl.innerText = carrito[id];
    }

    // Actualización instantánea en UI
    actualizarContador(obtenerTotalLocal());

    fetch("/ajax/agregar-carrito/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            producto_id: id,
            cantidad: 1,
        }),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                actualizarContador(data.total_items);
            } else {
                if (typeof data.cantidad_actual === "number") {
                    sincronizarCantidadProducto(id, data.cantidad_actual);
                    actualizarContador(obtenerTotalLocal());
                }
                if (data.error) {
                    mostrarMensajeCarrito(data.error);
                }
                vistaBasecarrito();

            }
        })
        .catch((error) => {
            console.error("Error:", error);
            mostrarMensajeCarrito("No se pudo actualizar el carrito. Intenta de nuevo.");
            vistaBasecarrito();
        });
}

/*  Flujo al hacer clic en los botones de cantidad:
    Incrementa o decrementa localmente la cantidad (carrito[id] += valor) para respuesta inmediata.
    Renderiza controles y contador local.
    Envía POST JSON a /ajax/agregar-carrito/.
    Si backend responde OK: usa data.total_items.
    Si backend responde error (límite, etc): sincroniza cantidad real y muestra mensaje.
    Si hay error de red: muestra mensaje genérico y refresca contador desde servidor.
    
    “editar una cantidad que ya existe”.
    
    */
function cambiarCantidad(id, valor){

    carrito[id] = (carrito[id] || 0) + valor

    fetch("/ajax/agregar-carrito/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            producto_id: id,
            cantidad: valor
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            actualizarContador(data.total_items);
        } else {
            if (typeof data.cantidad_actual === "number") {
                sincronizarCantidadProducto(id, data.cantidad_actual);
                actualizarContador(obtenerTotalLocal());
            }
            if (data.error) {
                mostrarMensajeCarrito(data.error);
            }
            vistaBasecarrito();
        }
    })
    .catch(error => {
        console.error("Error:", error);
        mostrarMensajeCarrito("No se pudo actualizar el carrito. Intenta de nuevo.");
        vistaBasecarrito();
    });

    if(carrito[id] <= 0){

        delete carrito[id]
        actualizarContador(obtenerTotalLocal());

        document.getElementById("carrito-"+id).innerHTML=
        `<button class="btn btn-warning"
        onclick="agregarProducto(${id})">
        🛒 Añadir
        </button>`

        return
    }

    document.getElementById("cantidad-"+id).innerText=carrito[id]
    actualizarContador(obtenerTotalLocal());

}
   
/* Obtiene la cantidad actual de un producto en el carrito. Si el producto no está en el carrito, devuelve 0.*/
function vistaBasecarrito() {
    fetch("/vistaBasecarrito/")
        .then((res) => res.json())
        .then((data) => {
            actualizarContador(data.total_items);
        })
        .catch((error) => console.error("Error:", error));
}

document.addEventListener("DOMContentLoaded", function () {
    vistaBasecarrito();

    // Para botones con data-id
    document.querySelectorAll(".btn-agregar").forEach((btn) => {
        btn.addEventListener("click", function () {
            const id = Number(this.dataset.id);
            agregarProducto(id);
        });
    });
});

window.onload = function () {
    for (let id in carrito) {
        renderCantidad(id);
        const cantidadEl = document.getElementById("cantidad-" + id);
        if (cantidadEl) {
            cantidadEl.innerText = carrito[id];
        }
    }

    actualizarContador(obtenerTotalLocal());
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach((cookie) => {
            if (cookie.trim().startsWith(name + "=")) {
                cookieValue = cookie.trim().substring(name.length + 1);
            }
        });
    }
    return cookieValue;
}



window.agregarProducto = agregarProducto;
window.cambiarCantidad = cambiarCantidad;
window.vistaBasecarrito = vistaBasecarrito;