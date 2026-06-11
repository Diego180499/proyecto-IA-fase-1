/**
 * historial.js — Vista de Historial (`#/historial`).
 *
 * Lista paginada de diagnósticos (GET /api/historial), con detalle en modal
 * (GET /api/historial/{id}) y eliminación con confirmación
 * (DELETE /api/historial/{id}). Maneja estado vacío y errores.
 */
import { api } from "../api.js";
import {
  Spinner,
  ErrorAlert,
  EmptyState,
  Modal,
  Toast,
  Badge,
  escapeHtml,
  formatTimestamp,
} from "../components.js";

/** Estado de paginación local. */
const state = {
  limit: 10,
  offset: 0,
  items: [],
};

/**
 * Renderiza la vista de historial.
 * @param {HTMLElement} app
 */
export function renderHistorial(app) {
  state.offset = 0;

  app.innerHTML = `
    <header class="page-header">
      <h1 class="page-header__title">Historial</h1>
      <p class="page-header__subtitle">
        Consulta, revisa el detalle o elimina diagnósticos anteriores.
      </p>
    </header>

    <div id="historyContent">${Spinner("Cargando historial…")}</div>
  `;

  loadHistorial();
}

/** Consume el historial con la paginación actual y lo renderiza. */
async function loadHistorial() {
  const content = document.getElementById("historyContent");
  if (!content) return;
  content.innerHTML = Spinner("Cargando historial…");

  try {
    state.items = await api.getHistorial(state.limit, state.offset);
    renderContent(content);
  } catch (err) {
    const msg =
      err.status === 0
        ? "No se pudo conectar con el servidor. Verifica que la API esté en ejecución."
        : "No se pudo cargar el historial. Intenta nuevamente.";
    content.innerHTML = `
      ${ErrorAlert(msg)}
      <div class="form-actions">
        <button class="btn btn--secondary" id="retryBtn">Reintentar</button>
      </div>`;
    document.getElementById("retryBtn")?.addEventListener("click", loadHistorial);
  }
}

/**
 * Renderiza la barra de herramientas y la tabla (o estado vacío).
 * @param {HTMLElement} content
 */
function renderContent(content) {
  const items = state.items || [];

  // Estado vacío: solo cuando estamos en la primera página y no hay registros.
  if (items.length === 0 && state.offset === 0) {
    content.innerHTML = EmptyState(
      "No hay diagnósticos registrados aún.",
      { href: "#/diagnostico", label: "Crear un diagnóstico" },
      "🩺"
    );
    return;
  }

  const desde = state.offset + 1;
  const hasta = state.offset + items.length;

  content.innerHTML = `
    <div class="history-toolbar">
      <span class="history-count">
        Mostrando ${items.length > 0 ? `${desde}–${hasta}` : "0"} ·
        ${items.length} registro${items.length === 1 ? "" : "s"} en esta página
      </span>

      <div class="pagination">
        <label class="pagination__group">
          Por página
          <select class="select" id="limitSelect">
            ${[10, 20, 50]
              .map(
                (n) =>
                  `<option value="${n}" ${n === state.limit ? "selected" : ""}>${n}</option>`
              )
              .join("")}
          </select>
        </label>
        <button class="btn btn--secondary btn--sm" id="prevBtn" ${
          state.offset === 0 ? "disabled" : ""
        }>← Anterior</button>
        <button class="btn btn--secondary btn--sm" id="nextBtn" ${
          items.length < state.limit ? "disabled" : ""
        }>Siguiente →</button>
      </div>
    </div>

    <div class="table-wrap">
      <table class="table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Síntomas ingresados</th>
            <th>Fallas</th>
            <th aria-label="Acciones"></th>
          </tr>
        </thead>
        <tbody>
          ${items.map(rowHtml).join("")}
        </tbody>
      </table>
    </div>
  `;

  bindToolbar();
  bindRowActions();
}

/**
 * Genera el HTML de una fila de la tabla.
 * @param {object} d - DiagnosticoResponse
 */
function rowHtml(d) {
  const sintomas = d.sintomas_ingresados || [];
  const resumen =
    sintomas.length > 3
      ? `${sintomas.slice(0, 3).join(", ")} +${sintomas.length - 3}`
      : sintomas.join(", ") || "—";
  const numFallas = d.fallas_detectadas?.length ?? 0;

  return `
    <tr data-id="${escapeHtml(d.id)}">
      <td>${escapeHtml(formatTimestamp(d.timestamp))}</td>
      <td class="table__symptoms">${escapeHtml(resumen)}</td>
      <td>${Badge(`${numFallas}`, numFallas > 0 ? "default" : "muted")}</td>
      <td>
        <div class="table__actions">
          <button class="btn btn--ghost btn--sm" data-action="view">Ver detalle</button>
          <button class="btn btn--danger btn--sm" data-action="delete">Eliminar</button>
        </div>
      </td>
    </tr>`;
}

/** Vincula los controles de la barra de herramientas (paginación). */
function bindToolbar() {
  document.getElementById("limitSelect")?.addEventListener("change", (e) => {
    state.limit = Number(e.target.value);
    state.offset = 0;
    loadHistorial();
  });

  document.getElementById("prevBtn")?.addEventListener("click", () => {
    state.offset = Math.max(0, state.offset - state.limit);
    loadHistorial();
  });

  document.getElementById("nextBtn")?.addEventListener("click", () => {
    state.offset += state.limit;
    loadHistorial();
  });
}

/** Vincula los botones "Ver detalle" y "Eliminar" de cada fila. */
function bindRowActions() {
  document.querySelectorAll("tr[data-id]").forEach((row) => {
    const id = row.dataset.id;
    row
      .querySelector('[data-action="view"]')
      ?.addEventListener("click", () => openDetail(id));
    row
      .querySelector('[data-action="delete"]')
      ?.addEventListener("click", () => confirmDelete(id));
  });
}

/**
 * Abre el modal de detalle de un diagnóstico.
 * @param {string} id
 */
async function openDetail(id) {
  // Modal con spinner mientras se carga el detalle.
  const modal = Modal({
    titulo: "Detalle del diagnóstico",
    contenidoHtml: Spinner("Cargando detalle…"),
  });

  const body = modal.root.querySelector(".modal__body");

  try {
    const d = await api.getDiagnostico(id);
    body.innerHTML = detailHtml(d);
  } catch (err) {
    const msg =
      err.status === 404
        ? "El diagnóstico ya no existe."
        : "No se pudo cargar el detalle.";
    body.innerHTML = ErrorAlert(msg);
  }
}

/**
 * Genera el HTML del detalle completo de un diagnóstico.
 * @param {object} d - DiagnosticoResponse
 */
function detailHtml(d) {
  const sintomas =
    d.sintomas_ingresados?.map((s) => Badge(s)).join("") || "—";

  const fallas =
    d.fallas_detectadas?.length > 0
      ? d.fallas_detectadas
          .map(
            (f) => `
        <div class="falla-card">
          <span class="falla-card__id">${escapeHtml(f.id)}</span>
          <p class="falla-card__desc">${escapeHtml(f.descripcion)}</p>
        </div>`
          )
          .join("")
      : `<p class="text-muted">Sin fallas detectadas.</p>`;

  const recs =
    d.recomendaciones?.length > 0
      ? `<ol class="rec-list">${d.recomendaciones
          .map((r) => `<li>${escapeHtml(r.descripcion)}</li>`)
          .join("")}</ol>`
      : `<p class="text-muted">Sin recomendaciones.</p>`;

  return `
    <p class="detail-meta">${escapeHtml(formatTimestamp(d.timestamp))} · ID ${escapeHtml(
    d.id
  )}</p>

    <div class="detail-section">
      <p class="detail-section__title">Síntomas ingresados</p>
      <div class="badge-list">${sintomas}</div>
    </div>

    <div class="detail-section">
      <p class="detail-section__title">Fallas detectadas</p>
      ${fallas}
    </div>

    <div class="detail-section">
      <p class="detail-section__title">Recomendaciones</p>
      ${recs}
    </div>
  `;
}

/**
 * Confirma y ejecuta la eliminación de un diagnóstico.
 * @param {string} id
 */
async function confirmDelete(id) {
  const ok = window.confirm(
    "¿Eliminar este diagnóstico del historial? Esta acción no se puede deshacer."
  );
  if (!ok) return;

  try {
    await api.eliminarDiag(id);
    Toast("Diagnóstico eliminado.", "success");

    // Si la página queda vacía tras eliminar, retrocede una página.
    if (state.items.length === 1 && state.offset > 0) {
      state.offset = Math.max(0, state.offset - state.limit);
    }
    loadHistorial();
  } catch (err) {
    const msg =
      err.status === 404
        ? "El diagnóstico ya no existe."
        : "No se pudo eliminar el diagnóstico.";
    Toast(msg, "error");
  }
}
