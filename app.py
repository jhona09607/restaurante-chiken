from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = "supersecreto"

# Lista de productos
productos = [
    {"id": 1, "nombre": "Pollo Entero Plus", "precio": 12.50, "categoria": "pollo", "imagen": "Pollo_12.50.jpg"},
    {"id": 2, "nombre": "1/2 Pollo Asado", "precio": 7.50, "categoria": "pollo", "imagen": "Pollo_7.50.jpg"},
    {"id": 3, "nombre": "Pollo Entero Especial", "precio": 14.00, "categoria": "pollo", "imagen": "Pollo_14.00.jpg"},
    {"id": 4, "nombre": "Combo Pollo Familiar", "precio": 16.00, "categoria": "pollo", "imagen": "Pollo_16.00.jpg"},
    {"id": 5, "nombre": "Papi completa", "precio": 3.50, "categoria": "pollo", "imagen": "Papi_completa.jpg"},
    {"id": 6, "nombre": "Papi pollo", "precio": 2.50, "categoria": "pollo", "imagen": "Papi_pollo.jpg"},
    {"id": 7, "nombre": "Wraps de Pollo", "precio": 2.50, "categoria": "wraps", "imagen": "wrap_pollo.jpg"},
    {"id": 8, "nombre": "Wraps de carne", "precio": 2.50, "categoria": "wraps", "imagen": "wrap_carne.jpg"},
    {"id": 9, "nombre": "Wraps mixtos", "precio": 3.80, "categoria": "wraps", "imagen": "wrap_mixto.jpg"},
    {"id": 10, "nombre": "Humita", "precio": 1.50, "categoria": "extras", "imagen": "Humita.jpg"},
    {"id": 11, "nombre": "Tamal", "precio": 1.50, "categoria": "extras", "imagen": "Tamal.jpg"},
    {"id": 12, "nombre": "Quimbolito", "precio": 1.25, "categoria": "extras", "imagen": "Quimbolito.jpg"},
    {"id": 13, "nombre": "Tiramisú", "precio": 2.00, "categoria": "postres", "imagen": "Tiramisu.jpg"},
    {"id": 14, "nombre": "Helado Artesanal", "precio": 1.50, "categoria": "postres", "imagen": "Helado_artesanal.jpg"},
    {"id": 15, "nombre": "Jarra de Jugo Natural", "precio": 2.50, "categoria": "bebidas", "imagen": "Jugos_varios.jpg"},
    {"id": 16, "nombre": "Batidos", "precio": 1.50, "categoria": "bebidas", "imagen": "Batidos.jpg"},
    {"id": 17, "nombre": "Cerveza Artesanal", "precio": 4.00, "categoria": "bebidas", "imagen": "Cerveza_tradicional.jpg"},
]

@app.route("/")
def portal():
    return render_template("portal.html", productos=productos)

@app.route("/agregar/<int:producto_id>")
def agregar_carrito(producto_id):
    if "carrito" not in session:
        session["carrito"] = []

    carrito = session["carrito"]

    # Verificar si el producto ya está en el carrito
    for item in carrito:
        if item["id"] == producto_id:
            item["cantidad"] += 1
            session.modified = True
            return redirect(url_for("portal"))

    # Agregar producto nuevo con cantidad = 1
    producto = next((p for p in productos if p["id"] == producto_id), None)
    if producto:
        carrito.append({
            "id": producto["id"],
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": 1
        })
        session.modified = True

    return redirect(url_for("portal"))

@app.route("/carrito")
def ver_carrito():
    carrito = session.get("carrito", [])
    total_general = sum(item["precio"] * item["cantidad"] for item in carrito)
    return render_template("carrito.html", carrito=carrito, total_general=total_general)

@app.route("/eliminar/<int:producto_id>", methods=["POST"])
def eliminar_carrito(producto_id):
    carrito = session.get("carrito", [])
    carrito = [item for item in carrito if item["id"] != producto_id]
    session["carrito"] = carrito
    session.modified = True
    return redirect(url_for("ver_carrito"))

@app.route("/vaciar")
def vaciar_carrito():
    session["carrito"] = []
    session.modified = True
    return redirect(url_for("ver_carrito"))

@app.route("/finalizar")
def finalizar_compra():
    carrito = session.get("carrito", [])
    return render_template("finalizar.html", carrito=carrito)

if __name__ == "__main__":
    app.run(debug=True)
