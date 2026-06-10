# 🍗 Pollos Express — Sistema Web Profesional

Sistema completo de pedidos y gestión para restaurante de pollos a la brasa.

## Roles de usuario

| Usuario | Contraseña | Acceso |
|---------|------------|--------|
| `admin`  | `admin123`  | Dashboard completo, pedidos, productos, reportes |
| `ventas` | `ventas123` | Nuevo pedido POS, seguimiento de pedidos activos |

## Estructura del proyecto

```
pollos_express/
├── app.py                     # Servidor Flask con auth y rutas
├── requirements.txt
├── static/
│   ├── css/main.css           # Diseño profesional completo
│   └── js/main.js             # Carrito, toasts, lógica cliente
└── templates/
    ├── base.html              # Layout base
    ├── index.html             # Sitio público con carrito
    ├── login.html             # Página de acceso
    ├── _sidebar.html          # Sidebar compartido
    ├── sin_acceso.html        # Error 403
    ├── admin/
    │   ├── dashboard.html     # Métricas, pedidos recientes
    │   ├── pedidos.html       # Gestión completa de pedidos
    │   └── productos.html     # Administración del menú
    └── ventas/
        ├── dashboard.html     # Vista de pedidos activos
        └── nuevo_pedido.html  # POS para pedidos presenciales
```

## Instalación

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

El servidor corre en http://localhost:5000

## Funcionalidades

### Sitio público (/)
- Menú con filtros por categoría
- Carrito persistente con modal lateral
- Formulario de cliente (nombre, teléfono, dirección)
- Confirmación de pedido con número de orden

### Panel Admin (/admin)
- Dashboard con estadísticas en tiempo real
- Gestión de pedidos con cambio de estado en línea
- Administración de productos del menú
- Filtros de pedidos por estado

### Panel Ventas (/ventas)
- Vista de pedidos activos con tarjetas visuales
- POS para registrar pedidos presenciales/telefónicos
- Historial del día
- Actualización de estados en tiempo real
