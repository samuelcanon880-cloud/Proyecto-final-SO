import os
import socket
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Variable de entorno para identificar la instancia (ej. "Backend-1")
SERVER_NAME = os.getenv("SERVER_NAME", "Backend-Desconocido")

# group_by="endpoint": agrupa por ruta de Flask (evita una serie por cada URL distinta)
# default_labels: etiqueta "backend" en todas las métricas, útil para las gráficas
# excluded_paths: no cuenta la ruta /health
metrics = PrometheusMetrics(
    app,
    group_by="endpoint",
    default_labels={"backend": SERVER_NAME},
    excluded_paths=["/health"],
)
metrics.info("app_info", "Información del backend", server=SERVER_NAME)

# Ruta principal que muestra la identidad del contenedor
@app.route("/")
def index():
    hostname = socket.gethostname()
    return f"<h1>Hola desde {SERVER_NAME}</h1><p>Atendido por el contenedor: {hostname}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
