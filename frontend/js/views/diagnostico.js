/**
 * diagnostico.js — Vista de Diagnóstico (`#/diagnostico`).
 *
 * Flujo: carga síntomas (GET /api/sintomas) → el usuario selecciona ≥1 →
 * envía (POST /api/diagnostico) → muestra el resultado con fallas y
 * recomendaciones. Maneja los estados loading / error-422 / error-400 / error-500.
 */
import { api } from "../api.js";
import {
  Spinner,
  ErrorAlert,
  Badge,
  Toast,
  escapeHtml,
  formatTimestamp,
} from "../components.js";

/** Estado local de la vista. */
let sintomas = [];
let enviando = false;

/**
 * Renderiza la vista de diagnóstico.
 * @param {HTMLElement} app
 */
export function renderDiagnostico(app) {
  sintomas = [];
  enviando = false;

  app.innerHTML = `
    <header class="page-header">
      <h1 class="page-header__title">Diagnóstico</h1>
      <p class="page-header__subtitle">
        Selecciona los síntomas que presenta tu equipo y obtén un diagnóstico.
      </p>
    </header>

    <section class="card" id="symptomsPanel">
      ${Spinner("Cargando síntomas…")}
    </section>

    <section id="resultPanel" aria-live="polite"></section>
  `;

  loadSintomas();
}

/** Carga el catálogo de síntomas y renderiza los checkboxes. */
async function loadSintomas() {
  const panel = document.getElementById("symptomsPanel");
  try {
    sintomas = await api.getSintomas();
    if (!Array.isArray(sintomas) || sintomas.length === 0) {
      panel.innerHTML = ErrorAlert("No hay síntomas disponibles en este momento.");
      return;
    }
    renderSymptomsForm(panel);
  } catch (err) {
    const msg =
      err.status === 0
        ? "No se pudo conectar con el servidor. Verifica que la API esté en ejecución."
        : "No se pudieron cargar los síntomas. Intenta nuevamente.";
    panel.innerHTML = `
      ${ErrorAlert(msg)}
      <div class="form-actions">
        <button class="btn btn--secondary" id="retryBtn">Reintentar</button>
      </div>`;
    document.getElementById("retryBtn")?.addEventListener("click", () => {
      panel.innerHTML = Spinner("Cargando síntomas…");
      loadSintomas();
    });
  }
}

/**
 * Renderiza el formulario de selección de síntomas.
 * @param {HTMLElement} panel
 */
function renderSymptomsForm(panel) {
  panel.innerHTML = `
    <div class="symptoms-toolbar">
      <h2 class="section-title" style="margin:0;">Selecciona los síntomas</h2>
      <span class="text-muted" id="selCount">0 seleccionados</span>
    </div>

    <form id="symptomsForm">
      <div class="symptoms-grid">
        ${sintomas
          .map(
            (s) => `
          <label class="symptom-item">
            <input type="checkbox" name="sintoma" value="${escapeHtml(s.id)}" />
            <span class="symptom-item__label">
              ${escapeHtml(s.descripcion)}
              <span class="symptom-item__id">${escapeHtml(s.id)}</span>
            </span>
          </label>`
          )
          .join("")}
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn--primary" id="analyzeBtn" disabled>
          Analizar
        </button>
        <button type="button" class="btn btn--secondary" id="clearBtn">
          Limpiar selección
        </button>
      </div>
    </form>
  `;

  const form = document.getElementById("symptomsForm");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const clearBtn = document.getElementById("clearBtn");
  const selCount = document.getElementById("selCount");

  const refreshState = () => {
    const checked = form.querySelectorAll('input[name="sintoma"]:checked');
    analyzeBtn.disabled = checked.length === 0 || enviando;
    selCount.textContent = `${checked.length} seleccionado${checked.length === 1 ? "" : "s"}`;
  };

  form.addEventListener("change", refreshState);

  clearBtn.addEventListener("click", () => {
    form
      .querySelectorAll('input[name="sintoma"]:checked')
      .forEach((c) => (c.checked = false));
    refreshState();
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const seleccionados = [
      ...form.querySelectorAll('input[name="sintoma"]:checked'),
    ].map((c) => c.value);
    submitDiagnostico(seleccionados, analyzeBtn);
  });
}

/**
 * Envía los síntomas seleccionados y renderiza el resultado.
 * @param {string[]} seleccionados
 * @param {HTMLButtonElement} analyzeBtn
 */
async function submitDiagnostico(seleccionados, analyzeBtn) {
  if (seleccionados.length === 0 || enviando) return;

  const resultPanel = document.getElementById("resultPanel");
  enviando = true;
  analyzeBtn.disabled = true;
  analyzeBtn.innerHTML = `<span class="spinner spinner--sm"></span> Analizando…`;
  resultPanel.innerHTML = `<div class="card">${Spinner("Analizando síntomas…")}</div>`;

  try {
    const diagnostico = await api.crearDiagnostico(seleccionados);
    renderResult(resultPanel, diagnostico);
    Toast("Diagnóstico completado.", "success");
    resultPanel.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    renderError(resultPanel, err);
  } finally {
    enviando = false;
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analizar";
  }
}

/**
 * Renderiza el panel de resultado de un diagnóstico exitoso.
 * @param {HTMLElement} panel
 * @param {object} d - DiagnosticoResponse
 */
function renderResult(panel, d) {
  const sintomasHtml =
    d.sintomas_ingresados?.map((id) => Badge(id)).join("") || "—";

  const fallasHtml =
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
      : `<p class="text-muted">No se detectaron fallas para los síntomas indicados.</p>`;

  const recsHtml =
    d.recomendaciones?.length > 0
      ? `<ol class="rec-list">${d.recomendaciones
          .map((r) => `<li>${escapeHtml(r.descripcion)}</li>`)
          .join("")}</ol>`
      : `<p class="text-muted">Sin recomendaciones asociadas.</p>`;

  panel.innerHTML = `
    <div class="card result">
      <div class="result__header">
        <span class="result__check" aria-hidden="true">✓</span>
        <div>
          <h2 class="result__title">Diagnóstico completado</h2>
          <p class="result__time">${escapeHtml(formatTimestamp(d.timestamp))}</p>
        </div>
      </div>

      <div class="result__block">
        <p class="result__block-title">Síntomas ingresados</p>
        <div class="badge-list">${sintomasHtml}</div>
      </div>

      <div class="result__block">
        <p class="result__block-title">Fallas detectadas</p>
        ${fallasHtml}
      </div>

      <div class="result__block">
        <p class="result__block-title">Recomendaciones</p>
        ${recsHtml}
      </div>

      <div class="form-actions">
        <button class="btn btn--primary" id="newDiagBtn">Nuevo diagnóstico</button>
      </div>
    </div>
  `;

  document.getElementById("newDiagBtn")?.addEventListener("click", () => {
    const app = document.getElementById("app");
    renderDiagnostico(app);
    document.getElementById("app").scrollIntoView({ behavior: "smooth" });
  });
}

/**
 * Renderiza un mensaje de error según el status devuelto por la API.
 * @param {HTMLElement} panel
 * @param {{status:number, data:any}} err
 */
function renderError(panel, err) {
  let mensaje;
  switch (err.status) {
    case 422:
      mensaje = "Selecciona al menos un síntoma.";
      break;
    case 400:
      mensaje = err.data?.detail || "Síntoma no reconocido.";
      break;
    case 0:
      mensaje =
        "No se pudo conectar con el servidor. Verifica que la API esté en ejecución.";
      break;
    case 500:
      mensaje = "Error del servidor. Intenta nuevamente.";
      break;
    default:
      mensaje =
        err.data?.detail || "Ocurrió un error al procesar el diagnóstico.";
  }

  panel.innerHTML = `<div class="card">${ErrorAlert(mensaje)}</div>`;
  Toast(mensaje, "error");
}
