let carrito = {};

const data = document.getElementById("data-carrito");

if (data) {
    const contenido = data.textContent.trim();
    if (contenido) {
        carrito = JSON.parse(contenido);
    }
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

function obtenerTotalLocal() {
    return Object.values(carrito).reduce(
        (total, cantidad) => total + Number(cantidad || 0),
        0
    );
}

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
                // Sincroniza con backend
                actualizarContador(data.total_items);
            } else {
                vistaBasecarrito();
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            vistaBasecarrito();
        });
}

function cambiarCantidad(id, valor) {
    id = Number(id);

    carrito[id] = (carrito[id] || 0) + valor;

    fetch("/ajax/agregar-carrito/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            producto_id: id,
            cantidad: valor,
        }),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                actualizarContador(data.total_items);
            } else {
                vistaBasecarrito();
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            vistaBasecarrito();
        });

    if (carrito[id] <= 0) {
        delete carrito[id];
        actualizarContador(obtenerTotalLocal());

        const contenedor = document.getElementById("carrito-" + id);
        if (contenedor) {
            contenedor.innerHTML = `
                <button class="btn btn-warning" onclick="agregarProducto(${id})">
                    🛒 Añadir
                </button>
            `;
        }
        return;
    }

    const cantidadEl = document.getElementById("cantidad-" + id);
    if (cantidadEl) {
        cantidadEl.innerText = carrito[id];
    }

    actualizarContador(obtenerTotalLocal());
}

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