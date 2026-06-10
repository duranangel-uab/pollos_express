from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "pollos_express_secret_2024"

# ── Datos ─────────────────────────────────────────────────────────────────────

productos = [
    {"id": 1, "nombre": "Pollo Entero", "precio": 45, "categoria": "Platos principales",
     "descripcion": "Pollo a la brasa entero con guarnición", "imagen": "pollo_entero.jpg"},
    {"id": 2, "nombre": "Combo Familiar", "precio": 80, "categoria": "Combos",
     "descripcion": "4 piezas de pollo + papas + refresco familiar", "imagen": "combo_familiar.jpg"},
    {"id": 3, "nombre": "Alitas BBQ", "precio": 30, "categoria": "Entradas",
     "descripcion": "6 alitas bañadas en salsa BBQ artesanal", "imagen": "alitas_bbq.jpg"},
    {"id": 4, "nombre": "Media Pollo", "precio": 28, "categoria": "Platos principales",
     "descripcion": "Media pollo a la brasa con papas fritas", "imagen": "media_pollo.jpg"},
    {"id": 5, "nombre": "Combo Duo", "precio": 55, "categoria": "Combos",
     "descripcion": "2 piezas de pollo + papas + 2 refrescos", "imagen": "combo_duo.jpg"},
    {"id": 6, "nombre": "Ensalada César", "precio": 22, "categoria": "Ensaladas",
     "descripcion": "Lechuga romana, aderezo césar, crutones y parmesano", "imagen": "ensalada.jpg"},
]

pedidos = []
pedido_counter = [1000]

usuarios = {
    "admin": {"password": "admin123", "rol": "admin", "nombre": "Administrador"},
    "ventas": {"password": "ventas123", "rol": "ventas", "nombre": "Equipo Ventas"},
}

# ── Auth helpers ──────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def rol_requerido(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "usuario" not in session:
                return redirect(url_for("login"))
            if session.get("rol") not in roles:
                return redirect(url_for("sin_acceso"))
            return f(*args, **kwargs)
        return decorated
    return decorator

# ── Rutas públicas ────────────────────────────────────────────────────────────

@app.route("/")
def inicio():
    return render_template("index.html", productos=productos)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        if usuario in usuarios and usuarios[usuario]["password"] == password:
            session["usuario"] = usuario
            session["rol"] = usuarios[usuario]["rol"]
            session["nombre"] = usuarios[usuario]["nombre"]
            if session["rol"] == "admin":
                return redirect(url_for("admin_dashboard"))
            elif session["rol"] == "ventas":
                return redirect(url_for("ventas_dashboard"))
        else:
            error = "Usuario o contraseña incorrectos"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))

@app.route("/sin-acceso")
def sin_acceso():
    return render_template("sin_acceso.html"), 403

# ── Rutas Admin ───────────────────────────────────────────────────────────────

@app.route("/admin")
@rol_requerido("admin")
def admin_dashboard():
    total_ventas = sum(p["total"] for p in pedidos)
    pedidos_hoy = [p for p in pedidos if p.get("fecha", "")[:10] == datetime.now().strftime("%Y-%m-%d")]
    return render_template("admin/dashboard.html",
        pedidos=pedidos,
        pedidos_hoy=pedidos_hoy,
        total_ventas=total_ventas,
        productos=productos,
        usuario=session["nombre"])

@app.route("/admin/pedidos")
@rol_requerido("admin")
def admin_pedidos():
    return render_template("admin/pedidos.html", pedidos=pedidos, usuario=session["nombre"])

@app.route("/admin/productos")
@rol_requerido("admin")
def admin_productos():
    return render_template("admin/productos.html", productos=productos, usuario=session["nombre"])

# ── Rutas Ventas ──────────────────────────────────────────────────────────────

@app.route("/ventas")
@rol_requerido("ventas", "admin")
def ventas_dashboard():
    pedidos_activos = [p for p in pedidos if p.get("estado") in ("pendiente", "en_preparacion")]
    return render_template("ventas/dashboard.html",
        pedidos=pedidos,
        pedidos_activos=pedidos_activos,
        productos=productos,
        usuario=session["nombre"])

@app.route("/ventas/nuevo-pedido")
@rol_requerido("ventas", "admin")
def ventas_nuevo_pedido():
    return render_template("ventas/nuevo_pedido.html", productos=productos, usuario=session["nombre"])

# ── API ───────────────────────────────────────────────────────────────────────

@app.route("/api/pedidos", methods=["POST"])
def api_pedidos():
    pedido = request.json
    pedido_counter[0] += 1
    pedido["id"] = pedido_counter[0]
    pedido["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pedido["estado"] = "pendiente"
    pedidos.append(pedido)
    return jsonify({"mensaje": "Pedido recibido", "pedido": pedido, "numero": pedido_counter[0]})

@app.route("/api/pedidos/<int:pedido_id>/estado", methods=["PUT"])
@login_required
def actualizar_estado(pedido_id):
    nuevo_estado = request.json.get("estado")
    for p in pedidos:
        if p["id"] == pedido_id:
            p["estado"] = nuevo_estado
            return jsonify({"ok": True, "pedido": p})
    return jsonify({"error": "Pedido no encontrado"}), 404

@app.route("/api/pedidos", methods=["GET"])
@login_required
def api_listar_pedidos():
    return jsonify(pedidos)

if __name__ == "__main__":
    app.run(debug=True)
