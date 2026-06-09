from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

productos = [
    {"id": 1, "nombre": "Pollo Entero", "precio": 45, "imagen": "pollo_entero.jpg"},
    {"id": 2, "nombre": "Combo Familiar", "precio": 80, "imagen": "combo_familiar.jpg"},
    {"id": 3, "nombre": "Alitas BBQ", "precio": 30, "imagen": "alitas_bbq.jpg"}
]

pedidos = []

@app.route("/")
def inicio():
    return render_template("index.html", productos=productos)

@app.route("/admin")
def admin():
    return render_template("admin.html", pedidos=pedidos)

@app.route("/api/pedidos", methods=["POST"])
def api_pedidos():
    pedido = request.json
    pedidos.append(pedido)
    return jsonify({"mensaje": "Pedido recibido", "pedido": pedido})

if __name__ == "__main__":
    app.run(debug=True)
