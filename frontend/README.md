# Doctor Byte — Frontend

Interfaz web del sistema experto **Doctor Byte**, que diagnostica fallas comunes
en computadoras. El usuario selecciona los síntomas de su equipo y el motor de
inferencia Prolog (vía API REST) devuelve las fallas probables y las
recomendaciones de solución.

## Stack

- **HTML5** · **CSS3** · **JavaScript** (Vanilla ES6+, módulos nativos)
- SPA (Single Page Application) con **hash-router**, sin frameworks ni build step.
- Tipografía: [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts).

## Estructura

```
frontend/
├── index.html             # Shell de la SPA (navbar, #app, footer)
├── css/
│   ├── reset.css          # Normalización de estilos
│   ├── variables.css      # Tokens: paleta, tipografía, espaciado
│   └── styles.css         # Estilos globales y componentes
└── js/
    ├── api.js             # Capa de comunicación con la API REST
    ├── components.js      # Componentes reutilizables (Badge, Card, Modal…)
    ├── router.js          # Hash router (#/, #/diagnostico, #/historial)
    └── views/
        ├── home.js        # Inicio + health check
        ├── diagnostico.js # Flujo principal de diagnóstico
        └── historial.js   # Historial: lista, detalle y eliminación
```

## Requisitos

- La API de Doctor Byte debe estar corriendo en `http://localhost:8000`
  (CORS abierto, no requiere proxy). Si cambia la URL, edítala en
  [`js/api.js`](js/api.js) (constante `BASE_URL`).
- Un servidor estático. El uso de módulos ES (`import`/`export`) impide abrir
  `index.html` con `file://`; sírvelo en su lugar:

```bash
# Opción 1: Python
python -m http.server 5500

# Opción 2: extensión "Live Server" de VS Code (clic derecho → Open with Live Server)
```

Luego abre `http://localhost:5500` en el navegador.

## Vistas y endpoints

| Vista                         | Endpoint(s)                                                              |
| ----------------------------- | ------------------------------------------------------------------------ |
| Inicio (`#/`)                 | `GET /api/health`                                                        |
| Diagnóstico (`#/diagnostico`) | `GET /api/sintomas`, `POST /api/diagnostico`                             |
| Historial (`#/historial`)     | `GET /api/historial`, `GET /api/historial/{id}`, `DELETE /api/historial/{id}` |

## Paleta de colores

Definida como variables CSS en [`css/variables.css`](css/variables.css):

| Variable             | Hex       | Uso                                  |
| -------------------- | --------- | ------------------------------------ |
| `--color-navy-dark`  | `#1a2744` | Navbar, footer, elementos de peso    |
| `--color-navy`       | `#2d4a7a` | Botones primarios, encabezados       |
| `--color-blue`       | `#5b7fb5` | Acentos, bordes activos, hover       |
| `--color-blue-light` | `#adc5e0` | Fondos de tarjetas, badges           |
| `--color-gray-light` | `#f0f2f5` | Fondo general del body               |
