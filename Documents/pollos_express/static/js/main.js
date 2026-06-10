// ── Cart State ──────────────────────────────────────────────────────────────
const cart = { items: [], get total() { return this.items.reduce((s, i) => s + i.precio * i.qty, 0); } };

function addToCart(id, nombre, precio) {
  const existing = cart.items.find(i => i.id === id);
  if (existing) { existing.qty++; }
  else { cart.items.push({ id, nombre, precio, qty: 1 }); }
  renderCart();
  openCart();
}

function changeQty(id, delta) {
  const item = cart.items.find(i => i.id === id);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) cart.items.splice(cart.items.indexOf(item), 1);
  renderCart();
}

function renderCart() {
  const list = document.getElementById('cart-items');
  const empty = document.getElementById('cart-empty');
  const footer = document.getElementById('cart-footer');
  const badge = document.getElementById('cart-badge');
  if (!list) return;

  const count = cart.items.reduce((s, i) => s + i.qty, 0);
  if (badge) { badge.textContent = count; badge.style.display = count > 0 ? 'flex' : 'none'; }

  if (cart.items.length === 0) {
    list.innerHTML = '';
    if (empty) empty.style.display = 'block';
    if (footer) footer.style.display = 'none';
    return;
  }
  if (empty) empty.style.display = 'none';
  if (footer) footer.style.display = 'block';

  list.innerHTML = cart.items.map(item => `
    <div class="cart-item">
      <div class="cart-item-name">${item.nombre}</div>
      <div class="cart-item-qty">
        <button class="qty-btn" onclick="changeQty(${item.id}, -1)">−</button>
        <span>${item.qty}</span>
        <button class="qty-btn" onclick="changeQty(${item.id}, 1)">+</button>
      </div>
      <div class="cart-item-price">Bs ${(item.precio * item.qty).toFixed(0)}</div>
    </div>
  `).join('');

  const totalEl = document.getElementById('cart-total');
  if (totalEl) totalEl.textContent = `Bs ${cart.total.toFixed(0)}`;
}

function openCart() {
  document.getElementById('cart-panel')?.classList.add('open');
  document.getElementById('cart-overlay')?.classList.add('open');
}
function closeCart() {
  document.getElementById('cart-panel')?.classList.remove('open');
  document.getElementById('cart-overlay')?.classList.remove('open');
}

async function checkout() {
  if (cart.items.length === 0) return;
  const nombre = document.getElementById('cliente-nombre')?.value?.trim();
  const telefono = document.getElementById('cliente-telefono')?.value?.trim();
  const direccion = document.getElementById('cliente-direccion')?.value?.trim();

  if (!nombre || !telefono) {
    alert('Por favor ingresa tu nombre y teléfono.');
    return;
  }

  const btn = document.getElementById('checkout-btn');
  if (btn) { btn.disabled = true; btn.textContent = 'Enviando...'; }

  try {
    const res = await fetch('/api/pedidos', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ total: cart.total, productos: cart.items, nombre, telefono, direccion })
    });
    const data = await res.json();
    cart.items = [];
    renderCart();
    closeCart();
    showToast(`✅ Pedido #${data.numero} confirmado. ¡Gracias ${nombre}!`, 'success');
  } catch (e) {
    showToast('Error al enviar el pedido. Intenta de nuevo.', 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = 'Confirmar pedido'; }
  }
}

// ── Toast ───────────────────────────────────────────────────────────────────
function showToast(msg, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);z-index:500;display:flex;flex-direction:column;gap:8px;';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.style.cssText = `background:${type==='success'?'#1A5C30':'#8B0000'};color:#fff;padding:12px 20px;border-radius:10px;font-size:0.9rem;font-weight:500;box-shadow:0 4px 12px rgba(0,0,0,0.2);animation:fadeIn 0.3s;`;
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

// ── Category filter ─────────────────────────────────────────────────────────
function filterCategory(cat, btn) {
  document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.product-card').forEach(card => {
    card.style.display = (cat === 'Todos' || card.dataset.cat === cat) ? '' : 'none';
  });
}

// ── Dashboard: update order status ─────────────────────────────────────────
async function updateOrderStatus(id, select) {
  const estado = select.value;
  await fetch(`/api/pedidos/${id}/estado`, {
    method: 'PUT', headers: {'Content-Type':'application/json'},
    body: JSON.stringify({estado})
  });
  showToast('Estado actualizado', 'success');
}

// ── Init ────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('cart-overlay');
  if (overlay) overlay.addEventListener('click', closeCart);
  renderCart();
});
