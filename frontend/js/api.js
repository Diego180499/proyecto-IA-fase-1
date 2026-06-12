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

  /* ----------------------------------------------------------------------- */
  /* Base de conocimiento — Síntomas CRUD                                    */
  /* ----------------------------------------------------------------------- */

  /** GET /api/sintomas — Síntomas con sus fallas asociadas. */
  getSintomasDetalle: () => request("GET", "/api/sintomas"),

  /** GET /api/sintomas/{id} — Detalle de un síntoma. */
  getSintoma: (id) => request("GET", `/api/sintomas/${id}`),

  /** POST /api/sintomas — Crea un síntoma. payload: { id, descripcion, fallas: [] } */
  crearSintoma: (payload) => request("POST", "/api/sintomas", payload),

  /** PUT /api/sintomas/{id} — Actualiza un síntoma. payload: { descripcion?, fallas?: [] } */
  actualizarSintoma: (id, payload) => request("PUT", `/api/sintomas/${id}`, payload),

  /** DELETE /api/sintomas/{id} — Elimina un síntoma. */
  eliminarSintoma: (id) => request("DELETE", `/api/sintomas/${id}`),

  /** POST /api/sintomas/{id}/fallas — Asocia una falla a un síntoma. */
  asociarFallaASintoma: (sintomaId, fallaId) =>
    request("POST", `/api/sintomas/${sintomaId}/fallas`, { falla_id: fallaId }),

  /** DELETE /api/sintomas/{id}/fallas/{falla_id} — Desasocia una falla de un síntoma. */
  desasociarFallaDeSintoma: (sintomaId, fallaId) =>
    request("DELETE", `/api/sintomas/${sintomaId}/fallas/${fallaId}`),

  /* ----------------------------------------------------------------------- */
  /* Base de conocimiento — Fallas CRUD                                      */
  /* ----------------------------------------------------------------------- */

  /** GET /api/fallas/detalle — Fallas con sus recomendaciones asociadas. */
  getFallasDetalle: () => request("GET", "/api/fallas/detalle"),

  /** GET /api/fallas/{id} — Detalle de una falla. */
  getFalla: (id) => request("GET", `/api/fallas/${id}`),

  /** POST /api/fallas — Crea una falla. payload: { id, descripcion, recomendaciones: [] } */
  crearFalla: (payload) => request("POST", "/api/fallas", payload),

  /** PUT /api/fallas/{id} — Actualiza una falla. payload: { descripcion?, recomendaciones?: [] } */
  actualizarFalla: (id, payload) => request("PUT", `/api/fallas/${id}`, payload),

  /** DELETE /api/fallas/{id} — Elimina una falla (cascada en síntomas). */
  eliminarFalla: (id) => request("DELETE", `/api/fallas/${id}`),

  /** POST /api/fallas/{id}/recomendaciones — Asocia una recomendación a una falla. */
  asociarRecAFalla: (fallaId, recId) =>
    request("POST", `/api/fallas/${fallaId}/recomendaciones`, { recomendacion_id: recId }),

  /** DELETE /api/fallas/{id}/recomendaciones/{rec_id} — Desasocia una recomendación. */
  desasociarRecDeFalla: (fallaId, recId) =>
    request("DELETE", `/api/fallas/${fallaId}/recomendaciones/${recId}`),

  /* ----------------------------------------------------------------------- */
  /* Base de conocimiento — Recomendaciones CRUD                            */
  /* ----------------------------------------------------------------------- */

  /** GET /api/recomendaciones — Catálogo de recomendaciones. */
  getRecomendaciones: () => request("GET", "/api/recomendaciones"),

  /** GET /api/recomendaciones/{id} — Detalle de una recomendación. */
  getRecomendacion: (id) => request("GET", `/api/recomendaciones/${id}`),

  /** POST /api/recomendaciones — Crea una recomendación. payload: { id, descripcion } */
  crearRecomendacion: (payload) => request("POST", "/api/recomendaciones", payload),

  /** PUT /api/recomendaciones/{id} — Actualiza una recomendación. payload: { descripcion } */
  actualizarRecomendacion: (id, payload) =>
    request("PUT", `/api/recomendaciones/${id}`, payload),

  /** DELETE /api/recomendaciones/{id} — Elimina una recomendación. */
  eliminarRecomendacion: (id) => request("DELETE", `/api/recomendaciones/${id}`),
};
