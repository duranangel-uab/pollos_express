let carrito = [];
let total = 0;

function agregarCarrito(nombre, precio) {
  carrito.push({ nombre, precio });
  total += precio;
  mostrarCarrito();
}

function mostrarCarrito() {
  const lista = document.getElementById('lista-carrito');
  lista.innerHTML = '';
  carrito.forEach(item => {
    const li = document.createElement('li');
    li.textContent = `${item.nombre} - Bs ${item.precio}`;
    lista.appendChild(li);
  });
  document.getElementById('total').textContent = `Total: Bs ${total}`;
}

function finalizarPedido() {
  fetch('/api/pedidos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: Date.now(), total, productos: carrito })
  });
  alert(`Pedido confirmado por Bs ${total}`);
  carrito = [];
  total = 0;
  mostrarCarrito();
}

function scrollToMenu() {
  document.getElementById('menu').scrollIntoView({ behavior: 'smooth' });
}
