/**
 * home.js — Vista de Inicio (`#/`).
 *
 * Presenta el hero con CTA, los 3 pasos de "¿Cómo funciona?" y una tarjeta de
 * estado del sistema que consume `GET /api/health` al cargar.
 */
import { api } from "../api.js";

const STEPS = [
  {
    titulo: "Selecciona síntomas",
    texto: "Marca las señales que presenta tu computadora desde una lista clara.",
  },
  {
    titulo: "Analiza",
    texto: "El motor de inferencia Prolog evalúa los síntomas en segundos.",
  },
  {
    titulo: "Obtén resultado",
    texto: "Recibe las fallas probables y recomendaciones concretas de solución.",
  },
];

/**
 * Renderiza la vista de inicio.
 * @param {HTMLElement} app
 */
export function renderHome(app) {
  app.innerHTML = `
    <section class="hero">
      <div class="hero__content">
        <h1 class="hero__title">Doctor Byte</h1>
        <p class="hero__subtitle">
          Diagnostica fallas en tu computadora en segundos.
        </p>
        <div class="hero__cta">
          <a href="#/diagnostico" class="btn btn--primary btn--lg">
            Iniciar diagnóstico
          </a>
        </div>
      </div>
    </section>

    <section class="steps">
      <h2 class="section-title">¿Cómo funciona?</h2>
      <div class="steps__grid">
        ${STEPS.map(
          (step, i) => `
          <article class="step-card">
            <div class="step-card__num" aria-hidden="true">${i + 1}</div>
            <h3 class="step-card__title">${step.titulo}</h3>
            <p class="step-card__text">${step.texto}</p>
          </article>`
        ).join("")}
      </div>
    </section>

    <section class="system-status">
      <h2 class="section-title">Estado del sistema</h2>
      <div class="card status-card" id="statusCard">
        <div class="status-card__info">
          <span class="status-dot" id="statusDot"></span>
          <div>
            <p class="card__title" id="statusTitle">Comprobando estado…</p>
            <p class="text-muted" id="statusDesc">Consultando la API.</p>
          </div>
        </div>
        <div class="status-card__pills" id="statusPills"></div>
      </div>
    </section>
  `;

  loadHealth();
}

/** Consume el health check y actualiza la tarjeta de estado. */
async function loadHealth() {
  const dot = document.getElementById("statusDot");
  const title = document.getElementById("statusTitle");
  const desc = document.getElementById("statusDesc");
  const pills = document.getElementById("statusPills");
  if (!dot || !title) return;

  try {
    const health = await api.health();
    const ok = health.status === "ok";

    dot.className = `status-dot ${ok ? "status-dot--ok" : "status-dot--error"}`;
    title.textContent = ok ? "Sistema operativo" : "Sistema degradado";
    desc.textContent = ok
      ? "La API y el motor Prolog están funcionando correctamente."
      : "Algún componente no responde como se espera.";

    pills.innerHTML = `
      ${pill("API", health.api)}
      ${pill("Prolog", health.prolog)}
    `;
  } catch (err) {
    dot.className = "status-dot status-dot--error";
    title.textContent = "Sin conexión";
    desc.textContent =
      err.status === 0
        ? "No se pudo contactar la API. Verifica que el servidor esté en ejecución."
        : "Ocurrió un error al consultar el estado del sistema.";
    pills.innerHTML = "";
  }
}

/**
 * Genera un badge de estado para un subsistema.
 * @param {string} label
 * @param {string} value - "ok" | "error" | otro.
 */
function pill(label, value) {
  const ok = value === "ok";
  const variant = ok ? "badge--success" : "badge--error";
  const icon = ok ? "✓" : "✕";
  return `<span class="badge ${variant}">${icon} ${label}</span>`;
}
