from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

devices = []
next_id = 1


def validar_device(data):
    campos_obligatorios = ["nombre", "tipo", "estado", "area", "fecha_registro"]

    for campo in campos_obligatorios:
        if campo not in data or str(data[campo]).strip() == "":
            return False, f"El campo '{campo}' es obligatorio y no puede estar vacío."

    return True, None


@app.route("/", methods=["GET"])
def inicio():
    return render_template("index.html")


@app.route("/api", methods=["GET"])
def api_info():
    return jsonify({
        "mensaje": "API REST de inventario de TI activa",
        "endpoints": [
            "GET /devices",
            "GET /devices/<id>",
            "POST /devices",
            "PUT /devices/<id>",
            "DELETE /devices/<id>"
        ]
    }), 200


@app.route("/devices", methods=["GET"])
def obtener_todos():
    return jsonify(devices), 200


@app.route("/devices/<int:device_id>", methods=["GET"])
def obtener_uno(device_id):
    for device in devices:
        if device["id"] == device_id:
            return jsonify(device), 200
    return jsonify({"error": "Dispositivo no encontrado"}), 404


@app.route("/devices", methods=["POST"])
def crear_device():
    global next_id

    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    valido, mensaje = validar_device(data)
    if not valido:
        return jsonify({"error": mensaje}), 400

    nuevo_device = {
        "id": next_id,
        "nombre": data["nombre"],
        "tipo": data["tipo"],
        "estado": data["estado"],
        "area": data["area"],
        "fecha_registro": data["fecha_registro"]
    }

    devices.append(nuevo_device)
    next_id += 1

    return jsonify(nuevo_device), 201


@app.route("/devices/<int:device_id>", methods=["PUT"])
def actualizar_device(device_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    valido, mensaje = validar_device(data)
    if not valido:
        return jsonify({"error": mensaje}), 400

    for device in devices:
        if device["id"] == device_id:
            device["nombre"] = data["nombre"]
            device["tipo"] = data["tipo"]
            device["estado"] = data["estado"]
            device["area"] = data["area"]
            device["fecha_registro"] = data["fecha_registro"]
            return jsonify(device), 200

    return jsonify({"error": "Dispositivo no encontrado"}), 404


@app.route("/devices/<int:device_id>", methods=["DELETE"])
def eliminar_device(device_id):
    for device in devices:
        if device["id"] == device_id:
            devices.remove(device)
            return jsonify({"mensaje": "Dispositivo eliminado correctamente"}), 200

    return jsonify({"error": "Dispositivo no encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)