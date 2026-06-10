let carrito = [];
let total = 0;

function agregarCarrito(nombre, precio, id) {
  carrito.push({ id, nombre, precio });
  total += precio;
  mostrarCarrito();
  actualizarContador();

  // Animación
  const btn = event.target;
  btn.textContent = "✓ Agregado";
  setTimeout(() => {
    btn.textContent = "🛒 Agregar al Carrito";
  }, 1000);
}

function mostrarCarrito() {
  const lista = document.getElementById("lista-carrito");
  const carritoVacio = document.getElementById("carrito-vacio");

  if (carrito.length === 0) {
    carritoVacio.style.display = "block";
    lista.innerHTML = "";
  } else {
    carritoVacio.style.display = "none";
    lista.innerHTML = "";
    carrito.forEach((item, index) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <span>${item.nombre}</span>
        <span>
          Bs ${item.precio}
          <button onclick="eliminarDelCarrito(${index})" style="margin-left: 10px; background: #f44336; color: white; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer;">✕</button>
        </span>
      `;
      lista.appendChild(li);
    });
  }

  document.getElementById("total").textContent = `Total: Bs ${total}`;
}

function eliminarDelCarrito(index) {
  total -= carrito[index].precio;
  carrito.splice(index, 1);
  mostrarCarrito();
  actualizarContador();
}

function actualizarContador() {
  const count = carrito.length;
  document.getElementById("carrito-count").textContent = count;
}

function finalizarPedido() {
  if (carrito.length === 0) {
    alert("❌ No hay productos en el carrito");
    return;
  }

  fetch("/api/pedidos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      productos: carrito,
      total: total,
      fecha: new Date().toLocaleString(),
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      alert(
        `✅ ¡Pedido confirmado!\nTotal: Bs ${total}\nNúmero de pedido: #${data.pedido.id}\nEstado: ${data.pedido.estado}`,
      );
      carrito = [];
      total = 0;
      mostrarCarrito();
      actualizarContador();
      toggleCarrito();
    })
    .catch((error) => {
      alert("Error al realizar el pedido");
      console.error(error);
    });
}

function scrollToMenu() {
  document.getElementById("menu").scrollIntoView({ behavior: "smooth" });
}

function toggleCarrito() {
  const carrito = document.getElementById("carrito-sidebar");
  carrito.classList.toggle("abierto");
}

// Cerrar carrito al hacer clic fuera
document.addEventListener("click", function (event) {
  const carrito = document.getElementById("carrito-sidebar");
  const carritoBtn = document.querySelector(".carrito-flotante");

  if (
    carrito.classList.contains("abierto") &&
    !carrito.contains(event.target) &&
    !carritoBtn.contains(event.target)
  ) {
    carrito.classList.remove("abierto");
  }
});
