from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MAX_PESO_KG = 1000

# Ciudades de demostración para la maqueta escolar.
CIUDADES = [
    "Nuevo Casas Grandes, Chihuahua",
    "Chihuahua, Chihuahua",
    "Ciudad Juárez, Chihuahua",
    "Hermosillo, Sonora",
    "Monterrey, Nuevo León",
    "Torreón, Coahuila",
    "Ciudad de México",
    "Guadalajara, Jalisco",
]

# Multiplicadores ilustrativos por tipo de recorrido.
# NO representan tarifas reales; solo sirven para demostrar el cálculo.
MULTIPLICADORES_RUTA = {
    "local": 1.00,
    "regional": 1.15,
    "nacional": 1.35,
}

# Datos DEMO para la maqueta escolar.
ENVIOS_DEMO = {
    "RLX-2026-001": {
        "guia": "RLX-2026-001",
        "estado": "En tránsito",
        "estado_clase": "transito",
        "origen": "Ciudad de México",
        "destino": "Chihuahua, Chihuahua",
        "fecha_salida": "24 sep 2026",
        "entrega_estimada": "28 sep 2026",
        "servicio": "Estándar",
        "ultimo_movimiento": "En camino al centro de distribución de Chihuahua",
        "movimientos": [
            {"fecha": "27 sep 2026 · 10:20", "titulo": "En tránsito", "detalle": "La unidad continúa hacia el destino."},
            {"fecha": "26 sep 2026 · 18:05", "titulo": "Salida de centro logístico", "detalle": "El paquete salió del centro de distribución de Querétaro."},
            {"fecha": "24 sep 2026 · 14:40", "titulo": "Paquete recibido", "detalle": "Se registró la recepción del paquete."},
        ],
    },
    "RLX-2026-002": {
        "guia": "RLX-2026-002",
        "estado": "Preparando envío",
        "estado_clase": "preparando",
        "origen": "Monterrey, Nuevo León",
        "destino": "Torreón, Coahuila",
        "fecha_salida": "27 sep 2026",
        "entrega_estimada": "29 sep 2026",
        "servicio": "Express",
        "ultimo_movimiento": "Paquete listo para salir del centro de origen",
        "movimientos": [
            {"fecha": "27 sep 2026 · 16:15", "titulo": "Preparando envío", "detalle": "El paquete fue clasificado para salida."},
            {"fecha": "27 sep 2026 · 12:30", "titulo": "Paquete recibido", "detalle": "Se registró la recepción del paquete."},
        ],
    },
    "RLX-2026-003": {
        "guia": "RLX-2026-003",
        "estado": "Entregado",
        "estado_clase": "entregado",
        "origen": "Ciudad Juárez, Chihuahua",
        "destino": "Nuevo Casas Grandes, Chihuahua",
        "fecha_salida": "25 sep 2026",
        "entrega_estimada": "26 sep 2026",
        "servicio": "Estándar",
        "ultimo_movimiento": "Entrega completada en destino",
        "movimientos": [
            {"fecha": "26 sep 2026 · 13:05", "titulo": "Entregado", "detalle": "El envío fue entregado en el destino indicado."},
            {"fecha": "26 sep 2026 · 08:10", "titulo": "En ruta de entrega", "detalle": "La unidad salió para la última milla."},
            {"fecha": "25 sep 2026 · 20:45", "titulo": "Llegó a centro de destino", "detalle": "El paquete llegó al centro de distribución local."},
        ],
    },
}

SERVICIOS = [
    {
        "nombre": "Estándar",
        "descripcion": "Envíos nacionales con tiempos de entrega estimados y seguimiento básico.",
        "tiempo": "2 a 5 días",
        "detalle": "Pensado para mercancía de entrega regular dentro de la cobertura nacional.",
    },
    {
        "nombre": "Express",
        "descripcion": "Opción prioritaria para envíos que requieren una ventana de entrega más corta.",
        "tiempo": "1 a 2 días",
        "detalle": "Servicio demostrativo para representar envíos prioritarios.",
    },
    {
        "nombre": "Recolección",
        "descripcion": "Solicitud de recolección para recoger el paquete antes de iniciar el traslado.",
        "tiempo": "Mismo día / programado",
        "detalle": "La disponibilidad dependería de la zona y la programación del servicio.",
    },
]

RUTAS = [
    {"origen": "Ciudad de México", "destino": "Chihuahua", "tiempo": "3 a 5 días", "tipo": "Nacional"},
    {"origen": "Monterrey", "destino": "Torreón", "tiempo": "1 a 2 días", "tipo": "Regional"},
    {"origen": "Ciudad Juárez", "destino": "Nuevo Casas Grandes", "tiempo": "1 a 2 días", "tipo": "Regional"},
    {"origen": "Guadalajara", "destino": "Ciudad de México", "tiempo": "2 a 4 días", "tipo": "Nacional"},
]


def clasificar_ruta(origen: str, destino: str) -> str:
    """Clasifica el recorrido para generar una tarifa aproximada de demostración."""
    if origen == destino:
        return "local"

    chihuahua = {
        "Nuevo Casas Grandes, Chihuahua",
        "Chihuahua, Chihuahua",
        "Ciudad Juárez, Chihuahua",
    }

    if origen in chihuahua and destino in chihuahua:
        return "regional"

    return "nacional"


def calcular_cotizacion(peso_kg: float, origen: str, destino: str) -> dict:
    """Genera una cotización ilustrativa para la maqueta."""
    if peso_kg <= 0:
        raise ValueError("El peso debe ser mayor a 0 kg.")

    if peso_kg > MAX_PESO_KG:
        raise ValueError(f"El peso máximo permitido para esta maqueta es de {MAX_PESO_KG:,} kg.")

    if origen not in CIUDADES or destino not in CIUDADES:
        raise ValueError("Selecciona un origen y un destino disponibles.")

    if origen == destino:
        raise ValueError("El origen y el destino deben ser diferentes para calcular un envío.")

    # Escalones de peso ilustrativos para una cotización escolar.
    if peso_kg <= 5:
        base = 180
    elif peso_kg <= 20:
        base = 260
    elif peso_kg <= 50:
        base = 420
    elif peso_kg <= 100:
        base = 650
    elif peso_kg <= 250:
        base = 950
    elif peso_kg <= 500:
        base = 1500
    elif peso_kg <= 750:
        base = 2100
    else:
        base = 2800

    tipo_ruta = clasificar_ruta(origen, destino)
    multiplicador = MULTIPLICADORES_RUTA[tipo_ruta]
    total = round(base * multiplicador / 10) * 10

    tiempos = {
        "local": "1 día hábil",
        "regional": "1 a 2 días hábiles",
        "nacional": "2 a 5 días hábiles",
    }

    return {
        "peso": peso_kg,
        "origen": origen,
        "destino": destino,
        "tipo_ruta": tipo_ruta.capitalize(),
        "tiempo_estimado": tiempos[tipo_ruta],
        "base_peso": base,
        "total": total,
        "moneda": "MXN",
    }


@app.route("/")
def inicio():
    return render_template(
        "index.html",
        servicios=SERVICIOS,
        envios_demo=ENVIOS_DEMO,
        ciudades=CIUDADES,
        max_peso=MAX_PESO_KG,
    )


@app.route("/servicios")
def servicios():
    return render_template("servicios.html", servicios=SERVICIOS, max_peso=MAX_PESO_KG)


@app.route("/rutas")
def rutas():
    return render_template("rutas.html", rutas=RUTAS)


@app.route("/seguimiento")
def seguimiento():
    return render_template("seguimiento.html")


@app.route("/cotizacion")
def cotizacion():
    return render_template("cotizacion.html", ciudades=CIUDADES, max_peso=MAX_PESO_KG)


@app.route("/api/rastrear")
def api_rastrear():
    guia = request.args.get("guia", "").strip().upper()

    if not guia:
        return jsonify({"ok": False, "mensaje": "Escribe una guía para realizar la consulta."}), 400

    envio = ENVIOS_DEMO.get(guia)
    if not envio:
        return jsonify({
            "ok": False,
            "mensaje": "No encontramos esa guía en la maqueta. Prueba RLX-2026-001, RLX-2026-002 o RLX-2026-003."
        }), 404

    return jsonify({"ok": True, "envio": envio})


@app.route("/api/cotizar", methods=["POST"])
def api_cotizar():
    datos = request.get_json(silent=True) or {}

    try:
        peso_kg = float(datos.get("peso", 0))
        origen = str(datos.get("origen", "")).strip()
        destino = str(datos.get("destino", "")).strip()
        resultado = calcular_cotizacion(peso_kg, origen, destino)
    except (TypeError, ValueError) as error:
        return jsonify({"ok": False, "mensaje": str(error)}), 400

    return jsonify({"ok": True, "cotizacion": resultado})


@app.errorhandler(404)
def pagina_no_encontrada(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
