from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Lista de productos (inicial)
productos = [
    {"id": 1, "nombre": "Pollo Entero", "precio": 45, "imagen": "pollo_entero.jpg"},
    {"id": 2, "nombre": "Combo Familiar", "precio": 80, "imagen": "combo_familiar.jpg"},
    {"id": 3, "nombre": "Alitas BBQ", "precio": 30, "imagen": "alitas_bbq.jpg"}
]

# Lista de pedidos
pedidos = []
proximo_id_pedido = 1

@app.route("/")
def inicio():
    """Página principal del cliente"""
    return render_template("index.html", productos=productos)

@app.route("/admin")
def admin():
    """Panel administrativo"""
    return render_template("admin.html", pedidos=pedidos)

# API para productos
@app.route("/api/productos", methods=["GET"])
def obtener_productos():
    """Obtener todos los productos"""
    return jsonify(productos)

@app.route("/api/productos", methods=["POST"])
def agregar_producto():
    """Agregar nuevo producto"""
    nuevo_producto = request.json
    productos.append(nuevo_producto)
    return jsonify({"mensaje": "Producto agregado exitosamente", "producto": nuevo_producto})

@app.route("/api/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    """Eliminar un producto"""
    global productos
    productos = [p for p in productos if p.get("id") != id]
    return jsonify({"mensaje": "Producto eliminado"})

# API para pedidos
@app.route("/api/pedidos", methods=["GET"])
def obtener_pedidos():
    """Obtener todos los pedidos"""
    return jsonify(pedidos)

@app.route("/api/pedidos", methods=["POST"])
def crear_pedido():
    """Crear un nuevo pedido"""
    global proximo_id_pedido
    pedido = request.json
    pedido["id"] = proximo_id_pedido
    pedido["estado"] = "Pendiente"
    proximo_id_pedido += 1
    pedidos.append(pedido)
    return jsonify({"mensaje": "Pedido recibido", "pedido": pedido})

@app.route("/api/pedidos/<int:id>/estado", methods=["PUT"])
def actualizar_estado_pedido(id):
    """Actualizar estado de un pedido"""
    nuevo_estado = request.json.get("estado")
    for pedido in pedidos:
        if pedido["id"] == id:
            pedido["estado"] = nuevo_estado
            return jsonify({"mensaje": "Estado actualizado", "pedido": pedido})
    return jsonify({"error": "Pedido no encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)