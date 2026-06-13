# Manual Técnico — Doctor Byte

> Sistema experto para el diagnóstico de fallas en computadoras.
> Motor de inferencia: SWI-Prolog. Backend: Python + FastAPI. Frontend: SPA Vanilla JS.

---

## Tabla de Contenidos

1. [Documentación Técnica — Frontend](#1-documentación-técnica--frontend)
   - 1.1 [Tecnologías usadas](#11-tecnologías-usadas)
   - 1.2 [Patrón de diseño usado](#12-patrón-de-diseño-usado)
   - 1.3 [Responsabilidad de cada vista](#13-responsabilidad-de-cada-vista)
   - 1.4 [Distribución de carpetas](#14-distribución-de-carpetas)
   - 1.5 [Tecnología para consumir la API REST](#15-tecnología-para-consumir-la-api-rest)
   - 1.6 [Paleta de colores](#16-paleta-de-colores)
   - 1.7 [Sistema de componentes UI](#17-sistema-de-componentes-ui)
2. [Documentación Técnica — Backend](#2-documentación-técnica--backend)
   - 2.1 [Tecnologías usadas](#21-tecnologías-usadas)
   - 2.2 [Patrón de diseño usado](#22-patrón-de-diseño-usado)
   - 2.3 [Detalle de endpoints](#23-detalle-de-endpoints)
   - 2.4 [Distribución de carpetas](#24-distribución-de-carpetas)
   - 2.5 [Hechos y reglas Prolog](#25-hechos-y-reglas-prolog)
   - 2.6 [Responsabilidades de Prolog](#26-responsabilidades-de-prolog)
   - 2.7 [Responsabilidades de Python](#27-responsabilidades-de-python)
   - 2.8 [Pasos para iniciar la aplicación en local](#28-pasos-para-iniciar-la-aplicación-en-local)

---

## 1. Documentación Técnica — Frontend

### 1.1 Tecnologías usadas

| Tecnología | Versión / Detalle | Rol |
|---|---|---|
| **HTML5** | Semántico (secciones, article, nav, main) | Estructura de la SPA |
| **CSS3** | Variables nativas (Custom Properties), Flexbox, Grid | Estilos y layout responsivo |
| **JavaScript (ES Modules)** | Vanilla JS con `type="module"` | Lógica de la aplicación |
| **Google Fonts — Inter** | 400 / 500 / 600 / 700 | Tipografía principal |
| **Fetch API** | API nativa del navegador | Comunicación con el backend |

El proyecto **no utiliza ningún framework ni biblioteca de terceros** (ni React, Vue, Angular, jQuery, etc.). Toda la funcionalidad está construida sobre las APIs nativas del navegador, usando el estándar ES Modules para organizar el código.

---

### 1.2 Patrón de diseño usado

El frontend implementa el patrón **SPA con Hash Router** (Single Page Application con enrutamiento por fragmento de URL).

**Cómo funciona:**

- El archivo `index.html` es el único punto de entrada. Contiene un elemento `<main id="app">` que actúa como contenedor dinámico de la vista activa.
- El módulo `router.js` escucha los eventos `hashchange` y `DOMContentLoaded` del navegador. Cuando el hash de la URL cambia (por ejemplo de `#/` a `#/diagnostico`), el router resuelve la función de render correspondiente y la ejecuta sobre `#app`.
- Cada vista es una función pura `render(app: HTMLElement)` que genera e inyecta su propio HTML usando `innerHTML`. Esto evita mezclar la lógica de negocio con la estructura del documento.
- La separación de responsabilidades se refuerza con tres capas bien delimitadas:
  - **`api.js`** — capa de datos (acceso al backend).
  - **`components.js`** — capa de presentación (generadores de HTML reutilizable).
  - **`views/`** — capa de vistas (orquestación de datos + componentes).

Complementariamente, dentro de la vista de Módulo de Administración se aplica el patrón **Tab / Pestaña** donde cada pestaña delega el render a su módulo CRUD específico (`sintomas-crud.js`, `fallas-crud.js`, `recomendaciones-crud.js`).

---

### 1.3 Responsabilidad de cada vista

#### Vista: Inicio (`#/`)
**Archivo:** `js/views/home.js`

Presenta la página de bienvenida del sistema. Sus responsabilidades son mostrar el hero con el título de la aplicación y el botón de llamada a la acción ("Iniciar diagnóstico"), renderizar la sección "¿Cómo funciona?" con los tres pasos del flujo de diagnóstico, y mostrar una tarjeta de estado del sistema que consume `GET /api/health` al cargar la vista para reportar si la API y el motor Prolog están operativos.

#### Vista: Diagnóstico (`#/diagnostico`)
**Archivo:** `js/views/diagnostico.js`

Es la vista principal de la aplicación. Su flujo es el siguiente:

1. Al renderizarse, llama a `GET /api/sintomas` y muestra un spinner mientras carga.
2. Genera un formulario con checkboxes para cada síntoma disponible en la base de conocimiento.
3. El botón "Analizar" permanece deshabilitado hasta que el usuario selecciona al menos un síntoma.
4. Al enviar el formulario, llama a `POST /api/diagnostico` con la lista de síntomas seleccionados.
5. Muestra el resultado del diagnóstico: síntomas ingresados (como badges), fallas detectadas con su descripción, y la lista ordenada de recomendaciones.
6. Gestiona todos los estados de error posibles: sin conexión al servidor (status 0), síntoma no reconocido (400), validación (422), error de servidor (500).

#### Vista: Historial (`#/historial`)
**Archivo:** `js/views/historial.js`

Lista paginada de todos los diagnósticos realizados. Permite al usuario seleccionar cuántos registros ver por página (10, 20 o 50), navegar entre páginas con botones "Anterior / Siguiente", ver el detalle completo de un diagnóstico en un modal (llama a `GET /api/historial/{id}`), y eliminar un diagnóstico del historial con confirmación del navegador (llama a `DELETE /api/historial/{id}`). Maneja el estado vacío cuando no existen diagnósticos.

#### Vista: Módulo de Administración (`#/conocimiento`)
**Archivo:** `js/views/conocimiento.js` + `js/views/crud/`

Panel de administración del sistema experto. Organiza tres CRUDs en pestañas:

- **Pestaña Síntomas** (`sintomas-crud.js`): Listado, creación, edición y eliminación de síntomas. Permite además asociar y desasociar fallas a un síntoma.
- **Pestaña Fallas** (`fallas-crud.js`): Listado, creación, edición y eliminación de fallas. Permite asociar y desasociar recomendaciones a una falla.
- **Pestaña Recomendaciones** (`recomendaciones-crud.js`): Listado, creación, edición y eliminación de recomendaciones del catálogo.

Adicionalmente, esta vista incluye un botón en el encabezado para alternar la disponibilidad del bot de Telegram, que consume `GET /bot` para conocer el estado actual y `POST /bot/availability` para cambiarlo.

---

### 1.4 Distribución de carpetas

```
frontend/
├── index.html                  # Único punto de entrada de la SPA
├── css/
│   ├── reset.css               # Normalización de estilos del navegador
│   ├── variables.css           # Design tokens: paleta, tipografía, espaciado
│   └── styles.css              # Estilos globales, layout y componentes
└── js/
    ├── api.js                  # Capa de comunicación con la API REST (fetch)
    ├── components.js           # Componentes UI reutilizables (HTML + DOM)
    ├── router.js               # Hash router: despacha vistas según el hash
    └── views/
        ├── home.js             # Vista Inicio (#/)
        ├── diagnostico.js      # Vista Diagnóstico (#/diagnostico)
        ├── historial.js        # Vista Historial (#/historial)
        ├── conocimiento.js     # Vista Módulo Administración (#/conocimiento)
        └── crud/
            ├── sintomas-crud.js        # CRUD de síntomas
            ├── fallas-crud.js          # CRUD de fallas
            └── recomendaciones-crud.js # CRUD de recomendaciones
```

---

### 1.5 Tecnología para consumir la API REST

El frontend utiliza la **Fetch API nativa del navegador** con `async/await` para todas las llamadas HTTP. La lógica de comunicación está completamente centralizada en el archivo `js/api.js`.

**Arquitectura de la capa HTTP:**

`api.js` expone una función `request(method, path, body)` que encapsula:

- La construcción de la URL completa a partir de `BASE_URL = "http://localhost:8000"` y la ruta relativa.
- El envío del header `Content-Type: application/json`.
- La serialización automática del cuerpo con `JSON.stringify`.
- La gestión de errores de red (captura del `TypeError` de fetch y lo normaliza a `{ status: 0, data: {...} }`).
- La gestión de respuestas `204 No Content` (retorna `null` en lugar de intentar parsear JSON vacío).
- La propagación de errores HTTP como objetos `{ status, data }` que las vistas capturan con `try/catch` para mostrar mensajes específicos al usuario.

El objeto exportado `api` expone métodos con nombre semántico para cada endpoint (`api.getSintomas()`, `api.crearDiagnostico(sintomas)`, `api.getHistorial(limit, offset)`, etc.), aislando a las vistas del detalle de las rutas HTTP.

---

### 1.6 Paleta de colores

La paleta está definida como CSS Custom Properties en `css/variables.css`, bajo el comentario "In Color Balance".

**Colores principales:**

| Token CSS | Valor HEX | Uso |
|---|---|---|
| `--color-navy-dark` | `#1a2744` | Fondo de navbar, footer y elementos de peso |
| `--color-navy` | `#2d4a7a` | Botones primarios, encabezados de sección |
| `--color-blue` | `#5b7fb5` | Acentos, bordes activos, hover |
| `--color-blue-light` | `#adc5e0` | Fondos de tarjetas, badges, estados vacíos |
| `--color-gray-light` | `#f0f2f5` | Fondo general del body, superficies neutras |

**Colores funcionales:**

| Token CSS | Valor HEX | Uso |
|---|---|---|
| `--color-white` | `#ffffff` | Texto sobre fondos oscuros, superficies de tarjetas |
| `--color-text` | `#1a2744` | Texto principal sobre fondos claros |
| `--color-text-muted` | `#5b7fb5` | Texto secundario, placeholders |
| `--color-success` | `#2e7d52` | Estado: diagnóstico completado |
| `--color-error` | `#c0392b` | Estado: error, síntoma no reconocido |
| `--color-border` | `#d0dcec` | Bordes de tarjetas e inputs |

**Derivados con transparencia:**

| Token CSS | Valor | Uso |
|---|---|---|
| `--color-success-soft` | `rgba(46, 125, 82, 0.12)` | Fondos suaves de estado éxito |
| `--color-error-soft` | `rgba(192, 57, 43, 0.1)` | Fondos suaves de estado error |
| `--color-navy-soft` | `rgba(45, 74, 122, 0.08)` | Fondos suaves de elementos navy |

---

### 1.7 Sistema de componentes UI

`components.js` provee un conjunto de funciones de utilidad reutilizables en todas las vistas:

- **`Badge(texto, variant)`** — Etiqueta pequeña con variantes: `default`, `success`, `error`, `muted`.
- **`Card(titulo, contenidoHtml)`** — Contenedor con sombra y borde.
- **`Spinner(mensaje)`** — Indicador de carga circular accesible (atributo `role="status"`).
- **`EmptyState(mensaje, cta, icon)`** — Estado vacío con ícono, mensaje y CTA opcional.
- **`ErrorAlert(mensaje)`** — Bloque de error con estilo de alerta (`role="alert"`).
- **`Toast(mensaje, tipo, duracionMs)`** — Notificación temporal en la esquina superior derecha. Tipos: `info`, `success`, `error`.
- **`Modal({ titulo, contenidoHtml, acciones })`** — Modal de superposición con scroll interno. Se cierra con Escape o clic fuera del modal.
- **`ConfirmModal(mensaje, onConfirm)`** — Modal de confirmación para acciones destructivas.
- **`EntityTable({ columns, rows, canDelete, emptyText })`** — Tabla genérica para los CRUDs con columnas configurables, soporte para columnas de tipo "badges" y botones de editar/eliminar por fila.
- **`escapeHtml(value)`** — Función defensiva que escapa caracteres HTML para prevenir inyección de contenido al usar `innerHTML`.
- **`formatTimestamp(iso)`** — Formatea un timestamp ISO 8601 a formato legible en español con la localización `es-GT`.
- **`manejarErrorCrud(err)`** — Traduce errores HTTP de la capa API a mensajes Toast amigables para el usuario.

---

## 2. Documentación Técnica — Backend

### 2.1 Tecnologías usadas

| Tecnología | Versión | Rol |
|---|---|---|
| **Python** | 3.10+ | Lenguaje principal del backend |
| **FastAPI** | ≥ 0.111 | Framework web para la API REST |
| **Uvicorn** | ≥ 0.29 | Servidor ASGI para ejecutar FastAPI |
| **Pydantic** | ≥ 2.0 | Validación de datos y esquemas de entrada/salida |
| **SWI-Prolog** | Sistema instalado | Motor de inferencia lógica |
| **pyswip** | ≥ 0.3.1 | Puente Python ↔ SWI-Prolog |
| **httpx** | ≥ 0.27 | Cliente HTTP para llamadas a la Bot API de Telegram |
| **python-dotenv** | ≥ 1.0 | Carga de variables de entorno desde `.env` |
| **pytest** | ≥ 8.0 | Framework de pruebas unitarias |
| **JSON (stdlib)** | — | Persistencia del historial y la base de conocimiento |

---

### 2.2 Patrón de diseño usado

El backend implementa el patrón **Arquitectura en Capas** con una variante orientada a servicios, inspirada en el patrón **MVC (Model-View-Controller)** adaptado a una API REST:

```
Router (Controller)  →  Service (Model/Business Logic)  →  Schema (View/Serialization)
```

**Por qué se usó este patrón:**

Una API REST sin interfaz visual elimina la "Vista" clásica del MVC, pero la separación `Router → Service → Schema` cumple el mismo objetivo: cada capa tiene una única responsabilidad y no conoce los detalles internos de la otra. Esto permite que los routers sean declarativos y delgados (solo definen rutas y delegan), los servicios contengan toda la lógica de negocio (validaciones, orquestación, persistencia), y los schemas garanticen la integridad de los datos de entrada y salida con validación automática (Pydantic).

**Descripción de cada capa:**

**Routers (`app/routers/`)** — Son los controladores HTTP. Definen las rutas (`@router.get`, `@router.post`, etc.), validan las peticiones entrantes a través de los schemas Pydantic (FastAPI hace esto automáticamente), delegan la lógica al servicio correspondiente y convierten las excepciones de dominio a respuestas HTTP con el código correcto. No contienen lógica de negocio.

**Services (`app/services/`)** — Contienen toda la lógica de negocio de la aplicación. Cada servicio tiene una responsabilidad acotada: `prolog_service` gestiona el puente con SWI-Prolog, `conocimiento_service` implementa el CRUD de la base de conocimiento, `diagnostico_service` orquesta el flujo completo de un diagnóstico, `historial_service` gestiona la persistencia del historial, `telegram_service` encapsula las llamadas a la Bot API de Telegram, y `bot_availability_service` controla la bandera de habilitación del bot.

**Schemas (`app/schemas/`)** — Son los contratos de datos de la API, definidos con Pydantic. Definen qué campos acepta cada endpoint en el request body y qué estructura tiene cada respuesta. FastAPI usa estos schemas para validar automáticamente los datos entrantes y serializar las respuestas a JSON.

**Models (`app/models/`)** — Representan la estructura interna de los datos persistidos (dataclasses Python). Separan el modelo de dominio interno del contrato externo de la API (schemas).

**Prolog (`/prolog/`)** — Capa de motor de inferencia. Contiene la base de conocimiento, las reglas lógicas y los hechos dinámicos. Es invocada exclusivamente a través de `prolog_service.py`.

---

### 2.3 Detalle de endpoints

#### Health Check

---

**`GET /api/health`**

Responsabilidad: Verificar el estado operativo de la API y del motor de inferencia Prolog.

Query Params / Path Params: Ninguno.

Request Body: Ninguno.

Response Body:
```json
{
  "status": "ok",
  "api": "ok",
  "prolog": "ok"
}
```
En caso de error del motor Prolog, `status` retorna `"degraded"` y `prolog` retorna `"error"`.

---

#### Diagnóstico

---

**`POST /api/diagnostico`**

Responsabilidad: Recibir una lista de síntomas seleccionados por el usuario, ejecutar el motor de inferencia Prolog para identificar las fallas probables y sus recomendaciones, y persistir el resultado en el historial.

Query Params / Path Params: Ninguno.

Request Body:
```json
{
  "sintomas": ["pantalla_negra", "reinicio_inesperado"]
}
```

Response Body (HTTP 201):
```json
{
  "id": "uuid-generado",
  "sintomas_ingresados": ["pantalla_negra", "reinicio_inesperado"],
  "fallas_detectadas": [
    { "id": "falla_ram", "descripcion": "Falla en módulo(s) de memoria RAM" },
    { "id": "falla_fuente_poder", "descripcion": "Falla en la fuente de poder / adaptador" }
  ],
  "recomendaciones": [
    { "id": "rec_verificar_ram", "descripcion": "Verificar, re-insertar o reemplazar los módulos de RAM" },
    { "id": "rec_revisar_fuente", "descripcion": "Revisar la fuente de poder con multímetro o reemplazarla" }
  ],
  "timestamp": "2026-06-12T15:30:00Z"
}
```

Errores posibles: `422` si la lista de síntomas está vacía. `400` si uno o más síntomas no existen en la base de conocimiento.

---

#### Síntomas

---

**`GET /api/sintomas`**

Responsabilidad: Retornar el catálogo completo de síntomas disponibles con sus fallas asociadas.

Query Params / Path Params: Ninguno.

Request Body: Ninguno.

Response Body (HTTP 200): Lista de `SintomaDetalleOut`.
```json
[
  {
    "id": "pantalla_negra",
    "descripcion": "Pantalla en negro al encender el equipo",
    "fallas": ["falla_ram", "falla_fuente_poder", "falla_tarjeta_grafica"]
  }
]
```

---

**`GET /api/sintomas/{id}`**

Responsabilidad: Retornar el detalle de un síntoma específico por su identificador Prolog.

Path Params: `id` — Identificador del síntoma (ej. `pantalla_negra`).

Request Body: Ninguno.

Response Body (HTTP 200): Objeto `SintomaDetalleOut`. Retorna `404` si el síntoma no existe.

---

**`POST /api/sintomas`**

Responsabilidad: Crear un nuevo síntoma en la base de conocimiento y sincronizar el motor Prolog.

Query Params / Path Params: Ninguno.

Request Body:
```json
{
  "id": "sobrecarga_electrica",
  "descripcion": "El equipo se apaga por sobrecarga eléctrica",
  "fallas": ["falla_fuente_poder"]
}
```

Response Body (HTTP 201): Objeto `SintomaDetalleOut` creado. Errores: `409` si el ID ya existe, `422` si el ID no cumple el patrón Prolog, `400` si una falla referenciada no existe.

---

**`PUT /api/sintomas/{id}`**

Responsabilidad: Actualizar la descripción y/o las fallas asociadas de un síntoma existente.

Path Params: `id` — Identificador del síntoma.

Request Body (campos opcionales):
```json
{
  "descripcion": "Nueva descripción del síntoma",
  "fallas": ["falla_ram"]
}
```

Response Body (HTTP 200): Objeto `SintomaDetalleOut` actualizado. Retorna `404` si no existe.

---

**`DELETE /api/sintomas/{id}`**

Responsabilidad: Eliminar un síntoma de la base de conocimiento y sincronizar el motor Prolog.

Path Params: `id` — Identificador del síntoma.

Request Body: Ninguno.

Response Body: HTTP 204 No Content. Retorna `404` si no existe.

---

**`POST /api/sintomas/{id}/fallas`**

Responsabilidad: Asociar una falla existente a un síntoma (crea la relación `causa/2` en Prolog).

Path Params: `id` — Identificador del síntoma.

Request Body:
```json
{ "falla_id": "falla_ram" }
```

Response Body (HTTP 200): Objeto `SintomaDetalleOut` actualizado.

---

**`DELETE /api/sintomas/{id}/fallas/{falla_id}`**

Responsabilidad: Eliminar la asociación entre un síntoma y una falla.

Path Params: `id` — Identificador del síntoma. `falla_id` — Identificador de la falla.

Request Body: Ninguno.

Response Body (HTTP 200): Objeto `SintomaDetalleOut` actualizado.

---

#### Fallas

---

**`GET /api/fallas`**

Responsabilidad: Retornar la lista básica de fallas (id + descripción, sin recomendaciones). Endpoint de compatibilidad usado por la vista de diagnóstico.

Query Params / Path Params: Ninguno.

Request Body: Ninguno.

Response Body (HTTP 200): Lista de `FallaOut`.
```json
[
  { "id": "falla_ram", "descripcion": "Falla en módulo(s) de memoria RAM" }
]
```

---

**`GET /api/fallas/detalle`**

Responsabilidad: Retornar todas las fallas con sus recomendaciones asociadas.

Query Params / Path Params: Ninguno.

Request Body: Ninguno.

Response Body (HTTP 200): Lista de `FallaDetalleOut`.
```json
[
  {
    "id": "falla_ram",
    "descripcion": "Falla en módulo(s) de memoria RAM",
    "recomendaciones": ["rec_verificar_ram"]
  }
]
```

---

**`GET /api/fallas/{id}`**

Responsabilidad: Retornar el detalle de una falla específica con sus recomendaciones.

Path Params: `id` — Identificador de la falla.

Request Body: Ninguno.

Response Body (HTTP 200): Objeto `FallaDetalleOut`. Retorna `404` si no existe.

---

**`POST /api/fallas`**

Responsabilidad: Crear una nueva falla en la base de conocimiento.

Query Params / Path Params: Ninguno.

Request Body:
```json
{
  "id": "falla_lector_dvd",
  "descripcion": "Falla en el lector de DVD/CD",
  "recomendaciones": ["rec_servicio_tecnico"]
}
```

Response Body (HTTP 201): Objeto `FallaDetalleOut` creado. Errores: `409` si el ID ya existe, `422` si el ID no cumple el patrón Prolog, `400` si una recomendación referenciada no existe.

---

**`PUT /api/fallas/{id}`**

Responsabilidad: Actualizar la descripción y/o las recomendaciones asociadas de una falla existente.

Path Params: `id` — Identificador de la falla.

Request Body (campos opcionales):
```json
{
  "descripcion": "Nueva descripción de la falla",
  "recomendaciones": ["rec_servicio_tecnico"]
}
```

Response Body (HTTP 200): Objeto `FallaDetalleOut` actualizado.

---

**`DELETE /api/fallas/{id}`**

Responsabilidad: Eliminar una falla y desligarla en cascada de todos los síntomas que la referenciaban.

Path Params: `id` — Identificador de la falla.

Request Body: Ninguno.

Response Body: HTTP 204 No Content. Retorna `404` si no existe.

---

**`POST /api/fallas/{id}/recomendaciones`**

Responsabilidad: Asociar una recomendación existente a una falla (crea la relación `recomendacion/2` en Prolog).

Path Params: `id` — Identificador de la falla.

Request Body:
```json
{ "recomendacion_id": "rec_verificar_ram" }
```

Response Body (HTTP 200): Objeto `FallaDetalleOut` actualizado.

---

**`DELETE /api/fallas/{id}/recomendaciones/{rec_id}`**

Responsabilidad: Eliminar la asociación entre una falla y una recomendación.

Path Params: `id` — Identificador de la falla. `rec_id` — Identificador de la recomendación.

Request Body: Ninguno.

Response Body (HTTP 200): Objeto `FallaDetalleOut` actualizado.

---

#### Recomendaciones

---

**`GET /api/recomendaciones`**

Responsabilidad: Retornar el catálogo completo de recomendaciones disponibles.

Query Params / Path Params: Ninguno.

Request Body: Ninguno.

Response Body (HTTP 200): Lista de `RecomendacionOut`.
```json
[
  { "id": "rec_verificar_ram", "descripcion": "Verificar, re-insertar o reemplazar los módulos de RAM" }
]
```

---

**`GET /api/recomendaciones/{id}`**

Responsabilidad: Retornar el detalle de una recomendación por su identificador.

Path Params: `id` — Identificador de la recomendación.

Request Body: Ninguno.

Response Body (HTTP 200): Objeto `RecomendacionOut`. Retorna `404` si no existe.

---

**`POST /api/recomendaciones`**

Responsabilidad: Crear una nueva recomendación en el catálogo.

Query Params / Path Params: Ninguno.

Request Body:
```json
{
  "id": "rec_actualizar_bios",
  "descripcion": "Actualizar el BIOS/UEFI a la última versión disponible"
}
```

Response Body (HTTP 201): Objeto `RecomendacionOut` creado. Errores: `409` si el ID ya existe, `422` si el ID no cumple el patrón Prolog.

---

**`PUT /api/recomendaciones/{id}`**

Responsabilidad: Actualizar la descripción de una recomendación existente.

Path Params: `id` — Identificador de la recomendación.

Request Body:
```json
{ "descripcion": "Nueva descripción de la recomendación" }
```

Response Body (HTTP 200): Objeto `RecomendacionOut` actualizado.

---

**`DELETE /api/recomendaciones/{id}`**

Responsabilidad: Eliminar una recomendación del catálogo y desligarla en cascada de todas las fallas que la referenciaban. La recomendación `rec_servicio_tecnico` está protegida y no puede eliminarse (retorna `409`).

Path Params: `id` — Identificador de la recomendación.

Request Body: Ninguno.

Response Body: HTTP 204 No Content.

---

#### Historial

---

**`GET /api/historial`**

Responsabilidad: Retornar la lista paginada de diagnósticos registrados, ordenados del más reciente al más antiguo.

Query Params:
- `limit` (opcional, entero ≥ 1): Cantidad máxima de registros a retornar.
- `offset` (opcional, entero ≥ 0, default: 0): Registros a omitir desde el inicio.

Request Body: Ninguno.

Response Body (HTTP 200): Lista de `DiagnosticoResponse`.

---

**`GET /api/historial/{id}`**

Responsabilidad: Retornar el detalle completo de un diagnóstico por su UUID.

Path Params: `id` — UUID del diagnóstico.

Request Body: Ninguno.

Response Body (HTTP 200): Objeto `DiagnosticoResponse`. Retorna `404` si no existe.

---

**`DELETE /api/historial/{id}`**

Responsabilidad: Eliminar un diagnóstico del historial de forma permanente.

Path Params: `id` — UUID del diagnóstico.

Request Body: Ninguno.

Response Body: HTTP 204 No Content. Retorna `404` si no existe.

---

#### Bot de Telegram

---

**`GET /bot`**

Responsabilidad: Retornar el estado actual de la bandera que controla si el bot envía los diagnósticos a Telegram. `true` indica envío activo; `false` indica envío desactivado.

Query Params / Path Params: Ninguno.

Request Body: Ninguno.

Response Body (HTTP 200):
```json
{ "availability": true }
```

---

**`POST /bot/availability`**

Responsabilidad: Invertir el estado de la bandera de disponibilidad del bot. Si estaba activa la desactiva, y si estaba inactiva la activa. El campo `availability` del body es requerido por el contrato de la API pero el endpoint siempre alterna el estado actual.

Query Params / Path Params: Ninguno.

Request Body:
```json
{ "availability": true }
```

Response Body (HTTP 200):
```json
{ "availability": false }
```

---

**`POST /api/telegram/send`**

Responsabilidad: Enviar un mensaje de texto a un usuario de Telegram identificado por su `chat_id`. El usuario debe haber enviado `/start` al bot previamente.

Query Params / Path Params: Ninguno.

Request Body:
```json
{
  "chat_id": "123456789",
  "mensaje": "Texto del mensaje a enviar"
}
```

Response Body (HTTP 200):
```json
{
  "ok": true,
  "chat_id": "123456789",
  "message_id": 42,
  "texto_enviado": "Texto del mensaje a enviar",
  "detalle": "Mensaje enviado exitosamente."
}
```

Errores: `502` si Telegram rechaza el mensaje. `504` por timeout. `503` por error de conectividad.

---

**`GET /api/telegram/health`**

Responsabilidad: Verificar que el token de bot configurado en `TELEGRAM_BOT_TOKEN` es válido llamando al método `getMe` de la Bot API.

Query Params / Path Params: Ninguno.

Request Body: Ninguno.

Response Body (HTTP 200):
```json
{
  "status": "ok",
  "bot_id": 123456789,
  "bot_username": "doctorbyte_bot",
  "bot_name": "Doctor Byte"
}
```

Retorna `503` si el token es inválido o hay error de conectividad.

---

**`POST /send_diagnostic`**

Responsabilidad: Enviar un mensaje de texto a Telegram y retornar únicamente un indicador booleano de éxito. Si el bot está deshabilitado (`bot_availability_service.esta_habilitado()` retorna `false`), responde `success: true` sin enviar nada.

Query Params / Path Params: Ninguno.

Request Body:
```json
{
  "chat_id": "123456789",
  "text": "Texto del diagnóstico a enviar"
}
```

Response Body (HTTP 200):
```json
{ "success": true }
```

---

### 2.4 Distribución de carpetas

```
backend/
├── main.py                         # Punto de entrada FastAPI: configuración CORS,
│                                   # registro de routers, lifespan (carga Prolog al inicio)
├── requirements.txt                # Dependencias Python del proyecto
├── .env                            # Variables de entorno (tokens, rutas personalizadas)
├── conftest.py                     # Configuración de fixtures para pytest
├── tests/                          # Suite de pruebas unitarias
│   ├── test_bot_availability_service.py
│   ├── test_bot_router.py
│   ├── test_diagnostico_service.py
│   ├── test_historial_service.py
│   ├── test_prolog_service.py
│   └── test_telegram_service.py
└── app/
    ├── __init__.py
    ├── data/
    │   ├── conocimiento.json       # Persistencia de la base de conocimiento (CRUD)
    │   └── historial.json          # Persistencia del historial de diagnósticos
    ├── models/
    │   └── diagnostico_model.py    # Dataclass interna del diagnóstico persistido
    ├── routers/
    │   ├── bot_router.py           # GET /bot, POST /bot/availability
    │   ├── conocimiento_errores.py # Traductor de excepciones de dominio → HTTP codes
    │   ├── diagnostico_router.py   # POST /api/diagnostico
    │   ├── fallas_router.py        # CRUD /api/fallas
    │   ├── historial_router.py     # GET/DELETE /api/historial
    │   ├── recomendaciones_router.py # CRUD /api/recomendaciones
    │   ├── sintomas_router.py      # CRUD /api/sintomas + GET /api/fallas (básico)
    │   └── telegram_router.py      # POST /api/telegram/send, GET /api/telegram/health,
    │                               # POST /send_diagnostic
    ├── schemas/
    │   ├── bot_schema.py           # BotAvailabilityRequest/Response
    │   ├── diagnostico_schema.py   # DiagnosticoRequest/Response
    │   ├── sintoma_schema.py       # Schemas de síntomas, fallas y recomendaciones
    │   └── telegram_schema.py      # TelegramMessageRequest/Response, SendDiagnosticRequest/Response
    └── services/
        ├── bot_availability_service.py  # Bandera en memoria para habilitar/deshabilitar el bot
        ├── conocimiento_service.py      # CRUD de síntomas, fallas y recomendaciones (JSON + Prolog)
        ├── diagnostico_service.py       # Orquestador del flujo de diagnóstico
        ├── historial_service.py         # Persistencia del historial en JSON
        ├── prolog_service.py            # Puente Python ↔ SWI-Prolog (pyswip)
        └── telegram_service.py          # Cliente de la Bot API de Telegram (httpx)
```

Y fuera del directorio `backend/`, en la raíz del proyecto:

```
prolog/
├── main.pl                 # Archivo raíz: consulta (include) los demás .pl
├── base_conocimiento.pl    # Hechos iniciales: sintoma/1, causa/2, recomendacion/2
├── descripciones.pl        # Hechos de descripciones legibles: descripcion_sintoma/2,
│                           # descripcion_falla/2, descripcion_recomendacion/2
├── reglas.pl               # Reglas de inferencia: posible_falla/2,
│                           # posible_recomendacion/2, diagnosticar/3, obtener_fallas/1
└── persistencia.pl         # Soporte de historial dinámico en Prolog (Mecanismo 1 opcional)
```

---

### 2.5 Hechos y reglas Prolog

La base de conocimiento está compuesta por cuatro categorías de predicados:

**Hechos dinámicos de la base de conocimiento** (`base_conocimiento.pl`):

- `sintoma(ID)` — Declara un síntoma disponible en el sistema. Ejemplo: `sintoma(pantalla_negra).`
- `causa(Sintoma, Falla)` — Mapea un síntoma a la falla que puede indicar. Un síntoma puede apuntar a múltiples fallas. Ejemplo: `causa(pantalla_negra, falla_ram).`
- `recomendacion(Falla, Recomendacion)` — Asocia una falla con su acción de solución recomendada. Ejemplo: `recomendacion(falla_ram, rec_verificar_ram).`

Los tres predicados son declarados como `:- dynamic`, lo que permite que `prolog_service.py` los modifique en tiempo de ejecución mediante `assertz` y `retractall` al procesar cambios del CRUD.

**Hechos de descripciones legibles** (`descripciones.pl`):

- `descripcion_sintoma(ID, Texto)` — Descripción en lenguaje natural de un síntoma.
- `descripcion_falla(ID, Texto)` — Descripción en lenguaje natural de una falla.
- `descripcion_recomendacion(ID, Texto)` — Descripción en lenguaje natural de una recomendación.

También son `:- dynamic` para que el backend los reconstruya desde el estado del CRUD.

**Reglas de inferencia** (`reglas.pl`):

- `posible_falla(Sintomas, Falla)` — Dado un síntoma `S` miembro de la lista `Sintomas`, infiere que `Falla` es una falla posible si existe el hecho `causa(S, Falla)`.
- `posible_recomendacion(Falla, Rec)` — Dada una `Falla`, infiere que `Rec` es una recomendación aplicable si existe el hecho `recomendacion(Falla, Rec)`.
- `diagnosticar(Sintomas, Fallas, Recomendaciones)` — Regla principal de diagnóstico. Utiliza `findall/3` para colectar todas las fallas posibles sin duplicados (`list_to_set/2`). Si encuentra al menos una falla, usa corte (`!`) para evitar el caso fallback. Si no encuentra ninguna falla, activa el caso fallback: `Fallas = [sin_diagnostico]`, `Recomendaciones = [rec_servicio_tecnico]`.
- `obtener_sintomas(Sintomas)` — Colecta todos los átomos `S` que satisfacen `sintoma(S)`.
- `obtener_fallas(Fallas)` — Colecta todas las fallas que tienen al menos una recomendación definida.

**Soporte de historial en Prolog** (`persistencia.pl`):

- `historial_diagnostico(ID, Sintomas, Fallas, Timestamp)` — Hecho dinámico para registrar diagnósticos en memoria Prolog (Mecanismo 1 opcional, complementario al historial JSON gestionado por Python).
- `registrar_diagnostico(ID, Sintomas, Fallas)` — Regla que captura el timestamp actual con `get_time/1` y agrega el hecho al historial en memoria.
- `save_historial(Ruta)` — Regla que persiste todos los hechos del historial a un archivo usando `tell/1`, `portray_clause/1` y `told/0`.

---

### 2.6 Responsabilidades de Prolog

Prolog actúa exclusivamente como **motor de inferencia lógica**. No gestiona estado persistente entre reinicios ni interactúa con la red. Sus responsabilidades son:

1. **Almacenar la base de conocimiento inicial** como hechos (`sintoma/1`, `causa/2`, `recomendacion/2`) que sirven de semilla en el primer arranque del sistema, antes de que exista el archivo `conocimiento.json`.

2. **Ejecutar la inferencia de diagnóstico** con la regla `diagnosticar/3`: dado un conjunto de síntomas, determina qué fallas son probables y qué recomendaciones aplican, empleando búsqueda exhaustiva con `findall/3` y eliminación de duplicados con `list_to_set/2`.

3. **Proveer el caso fallback** cuando ningún síntoma es reconocido o no existe una falla mapeada, retornando `[sin_diagnostico]` y `[rec_servicio_tecnico]` para garantizar que el sistema siempre emita una respuesta.

4. **Mantener los hechos dinámicos actualizados**: cuando el usuario modifica la base de conocimiento a través del CRUD, `prolog_service.py` ejecuta `retractall` y `assertz` para reconstruir los hechos dinámicos en el motor en ejecución, manteniendo la inferencia sincronizada con los datos persistidos en JSON.

5. **Proveer las listas de catálogo**: los predicados `obtener_sintomas/1` y `obtener_fallas/1` son consultados por `prolog_service.py` para obtener los identificadores disponibles en el sistema.

---

### 2.7 Responsabilidades de Python

Python actúa como el **orquestador** de todo el sistema. Sus responsabilidades se distribuyen entre los servicios:

**`prolog_service.py`** — Es el único punto del sistema que habla con SWI-Prolog. Carga los archivos `.pl` al iniciar la aplicación (via `consult`), ejecuta las consultas usando `pyswip` (`_prolog.query()`), normaliza los resultados (convierte los términos Prolog a strings Python), y reconstruye los hechos dinámicos (`retractall` + `assertz`) cuando el CRUD actualiza la base de conocimiento. Usa un `threading.Lock` para evitar condiciones de carrera al acceder al motor Prolog desde múltiples requests concurrentes.

**`conocimiento_service.py`** — Implementa el CRUD completo de síntomas, fallas y recomendaciones. Mantiene el estado en memoria (diccionario `_estado`) y lo persiste en `app/data/conocimiento.json`. En el primer arranque (sin JSON), siembra el estado inicial desde los hechos Prolog. Tras cada cambio, llama a `prolog_service.reconstruir_desde_estado()` para mantener el motor sincronizado. Valida IDs, descripciones, referencias entre entidades y operaciones no permitidas, levantando excepciones de dominio específicas que los routers traducen a códigos HTTP.

**`diagnostico_service.py`** — Orquesta el flujo completo de un diagnóstico: valida que todos los síntomas recibidos existan, llama a `prolog_service.ejecutar_diagnostico()`, enriquece las fallas y recomendaciones con sus descripciones legibles, genera un UUID y timestamp para el registro, persiste el resultado en el historial y, si el bot está habilitado, envía la notificación a Telegram.

**`historial_service.py`** — Gestiona la persistencia del historial de diagnósticos en `app/data/historial.json`. Implementa las operaciones de lectura paginada (más reciente primero), búsqueda por ID y eliminación. Usa `threading.Lock` para acceso seguro al archivo en entornos concurrentes.

**`telegram_service.py`** — Encapsula las llamadas a la Bot API de Telegram usando `httpx` como cliente HTTP síncrono. Implementa `verificar_bot()` (llama a `getMe`) y `enviar_mensaje(texto, chat_id)` (llama a `sendMessage`). Lee las credenciales de las variables de entorno `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`.

**`bot_availability_service.py`** — Servicio simple que mantiene en memoria una bandera booleana (`_telegram_habilitado`) para activar o desactivar el envío de diagnósticos a Telegram. Expone `esta_habilitado()` y `alternar_disponibilidad()`.

**`main.py`** — Define la aplicación FastAPI, configura CORS (permite todos los orígenes), registra todos los routers y define el lifespan que carga Prolog y la base de conocimiento al iniciar el servidor.

---

### 2.8 Pasos para iniciar la aplicación en local

#### Prerrequisitos

- Python 3.10 o superior instalado.
- SWI-Prolog instalado y disponible en el PATH del sistema. Descarga: [https://www.swi-prolog.org/Download.html](https://www.swi-prolog.org/Download.html)
- `pip` disponible.

#### Pasos

**1. Clonar el repositorio y posicionarse en la carpeta del backend:**
```bash
cd proyecto-IA-fase-1/backend
```

**2. Crear y activar el entorno virtual de Python:**
```bash
# Crear el entorno virtual
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Activar en Linux / macOS
source .venv/bin/activate
```

**3. Instalar las dependencias:**
```bash
pip install -r requirements.txt
```

**4. Configurar las variables de entorno:**

Editar el archivo `.env` en `backend/` y completar los valores:
```env
TELEGRAM_BOT_TOKEN=<token-del-bot-de-telegram>
TELEGRAM_CHAT_ID=<chat-id-del-destino>

# Opcionales — se resuelven automáticamente si se dejan vacías:
# PROLOG_DIR=../prolog
# HISTORIAL_PATH=app/data/historial.json
# CONOCIMIENTO_PATH=app/data/conocimiento.json
```

**5. Levantar el servidor de desarrollo:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en `http://localhost:8000`.

La documentación interactiva (Swagger UI) generada automáticamente por FastAPI estará en `http://localhost:8000/docs`.

La documentación alternativa (ReDoc) estará en `http://localhost:8000/redoc`.

**6. Verificar que el sistema está operativo:**
```bash
curl http://localhost:8000/api/health
```

Respuesta esperada:
```json
{ "status": "ok", "api": "ok", "prolog": "ok" }
```

#### Ejecutar las pruebas unitarias

```bash
# Desde el directorio backend/
pytest tests/ -v
```

#### Levantar el frontend

El frontend es una SPA estática. Basta con servir la carpeta `frontend/` con cualquier servidor HTTP. La forma más sencilla en local:

```bash
# Desde la carpeta frontend/
python -m http.server 5500
```

Luego abrir `http://localhost:5500` en el navegador.

> **Nota:** El frontend espera que el backend esté corriendo en `http://localhost:8000`. Si se cambia el puerto del backend, actualizar la constante `BASE_URL` en `frontend/js/api.js`.
