/**
 * api.js — Capa de comunicación con la API REST de Doctor Byte.
 *
 * Centraliza todas las llamadas HTTP usando `fetch` nativo con async/await.
 * Cada error se normaliza a `{ status, data }` para que las vistas decidan
 * qué mensaje mostrar al usuario sin exponer detalles técnicos.
 */

const BASE_URL = "http://localhost:8000";

/**
 * Realiza una petición HTTP a la API.
 * @param {string} method - Verbo HTTP (GET, POST, DELETE...).
 * @param {string} path - Ruta relativa a partir de BASE_URL.
 * @param {object|null} body - Cuerpo JSON opcional.
 * @returns {Promise<any|null>} Datos parseados o `null` en 204.
 * @throws {{status:number, data:any}} Cuando la respuesta no es OK o la red falla.
 */
async function request(method, path, body = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body) options.body = JSON.stringify(body);

  let res;
  try {
    res = await fetch(`${BASE_URL}${path}`, options);
  } catch (networkError) {
    // status 0 ⇒ no se pudo contactar la API (servidor caído, CORS, sin red).
    throw { status: 0, data: { detail: "No se pudo conectar con el servidor." } };
  }

  if (res.status === 204) return null;

  // Algunas respuestas de error podrían no traer JSON; se protege el parseo.
  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    throw { status: res.status, data };
  }

  return data;
}

export const api = {
  /** GET /api/health — Estado de la API y del motor Prolog. */
  health: () => request("GET", "/api/health"),

  /** GET /api/sintomas — Catálogo de síntomas disponibles. */
  getSintomas: () => request("GET", "/api/sintomas"),

  /** GET /api/fallas — Catálogo de fallas diagnosticables. */
  getFallas: () => request("GET", "/api/fallas"),

  /** POST /api/diagnostico — Ejecuta la inferencia con los síntomas dados. */
  crearDiagnostico: (sintomas) => request("POST", "/api/diagnostico", { sintomas }),

  /** GET /api/historial — Lista paginada de diagnósticos. */
  getHistorial: (limit, offset = 0) => {
    const params = new URLSearchParams();
    if (limit != null) params.set("limit", String(limit));
    params.set("offset", String(offset));
    return request("GET", `/api/historial?${params.toString()}`);
  },

  /** GET /api/historial/{id} — Detalle de un diagnóstico. */
  getDiagnostico: (id) => request("GET", `/api/historial/${id}`),

  /** DELETE /api/historial/{id} — Elimina un diagnóstico. */
  eliminarDiag: (id) => request("DELETE", `/api/historial/${id}`),
};
