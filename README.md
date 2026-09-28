# REDLOGISTICA.MX

Maqueta escolar de una página web de recepción, traslado, cotización aproximada y entrega de paquetes.

## Requisitos

- Python 3.12
- VS Code (recomendado)
- Flask 3.x

## Instalación en Windows

Abre una terminal dentro de la carpeta del proyecto y ejecuta:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell no permite activar el entorno virtual, también puedes usar el Símbolo del sistema:

```bat
.venv\Scripts\activate.bat
```

## Ejecutar

Con el entorno virtual activado:

```powershell
python app.py
```

Después abre:

```text
http://127.0.0.1:5000
```

## Funciones de la maqueta

- Consulta de servicios.
- Consulta de rutas y tiempos estimados.
- Seguimiento de guías de demostración.
- Cotización aproximada por peso, origen y destino.
- Límite máximo de 1,000 kg por paquete.
- Ubicación de referencia: Nuevo Casas Grandes, Chihuahua, México.

## Guías de demostración

- `RLX-2026-001` — En tránsito
- `RLX-2026-002` — Preparando envío
- `RLX-2026-003` — Entregado

Todos los precios, rutas, tiempos y envíos son ilustrativos para fines académicos.
