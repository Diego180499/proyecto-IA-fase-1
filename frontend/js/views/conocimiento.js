/**
 * conocimiento.js — Vista de Base de Conocimiento (`#/conocimiento`).
 *
 * Agrupa los tres CRUDs (Síntomas, Fallas, Recomendaciones) en una sola página
 * con pestañas. Cada pestaña delega el render a su módulo correspondiente sobre
 * el contenedor `#tab-content`.
 */
import { api } from "../api.js";
import { Toast } from "../components.js";
import { renderSintomasCrud } from "./crud/sintomas-crud.js";
import { renderFallasCrud } from "./crud/fallas-crud.js";
import { renderRecomendacionesCrud } from "./crud/recomendaciones-crud.js";

/** Mapa de pestañas: clave → { label, render }. */
const TABS = {
  sintomas: { label: "Síntomas", render: renderSintomasCrud },
  fallas: { label: "Fallas", render: renderFallasCrud },
  recomendaciones: { label: "Recomendaciones", render: renderRecomendacionesCrud },
};

/** Pestaña activa por defecto. */
let tabActiva = "sintomas";

/**
 * Renderiza la vista de Base de Conocimiento.
 * @param {HTMLElement} app
 */
export function renderConocimiento(app) {
  app.innerHTML = `
    <header class="page-header">
      <div class="page-header__top">
        <div class="page-header__text">
          <h1 class="page-header__title">Modulo de Administración</h1>
          <p class="page-header__subtitle">
            Gestiona los síntomas, fallas y recomendaciones del sistema experto.
          </p>
        </div>
        <button
          type="button"
          id="bot-toggle"
          class="btn bot-toggle bot-toggle--loading"
          aria-pressed="false"
          aria-label="Estado del bot de Telegram"
          disabled
        >Cargando…</button>
      </div>
    </header>

    <div class="tabs" role="tablist">
      ${Object.entries(TABS)
        .map(
          ([clave, { label }]) => `
        <button
          class="tab ${clave === tabActiva ? "is-active" : ""}"
          data-tab="${clave}"
          role="tab"
          aria-selected="${clave === tabActiva}"
        >${label}</button>`
        )
        .join("")}
    </div>

    <div id="tab-content" role="tabpanel"></div>
  `;

  const content = document.getElementById("tab-content");

  app.querySelectorAll(".tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      const clave = btn.dataset.tab;
      if (clave === tabActiva) return;
      tabActiva = clave;
      actualizarTabsActivas(app);
      TABS[clave].render(content);
    });
  });

  // Render inicial de la pestaña activa.
  TABS[tabActiva].render(content);

  const botToggle = document.getElementById("bot-toggle");
  if (botToggle) {
    cargarEstadoBot(botToggle);
    botToggle.addEventListener("click", () => alternarBot(botToggle));
  }
}

/**
 * Actualiza el aspecto del interruptor según la disponibilidad del bot.
 * @param {HTMLButtonElement} btn
 * @param {boolean} availability
 */
function actualizarBotonBot(btn, availability) {
  btn.disabled = false;
  btn.classList.remove("bot-toggle--loading", "bot-toggle--active", "bot-toggle--inactive");
  btn.classList.add(availability ? "bot-toggle--active" : "bot-toggle--inactive");
  btn.textContent = availability ? "Bot Activado" : "Bot Desactivado";
  btn.setAttribute("aria-pressed", String(availability));
}

/**
 * Consulta el estado actual del bot (GET /bot).
 * @param {HTMLButtonElement} btn
 */
async function cargarEstadoBot(btn) {
  try {
    const { availability } = await api.getBotAvailability();
    actualizarBotonBot(btn, availability);
  } catch {
    btn.disabled = false;
    btn.classList.remove("bot-toggle--loading", "bot-toggle--active", "bot-toggle--inactive");
    btn.classList.add("bot-toggle--inactive");
    btn.textContent = "Bot no disponible";
    Toast("No se pudo consultar el estado del bot.", "error");
  }
}

/**
 * Alterna la disponibilidad del bot y refresca el estado visual.
 * @param {HTMLButtonElement} btn
 */
async function alternarBot(btn) {
  btn.disabled = true;
  try {
    await api.toggleBotAvailability();
    const { availability } = await api.getBotAvailability();
    actualizarBotonBot(btn, availability);
  } catch {
    btn.disabled = false;
    Toast("No se pudo cambiar el estado del bot.", "error");
  }
}

/**
 * Sincroniza la clase y el estado ARIA de las pestañas.
 * @param {HTMLElement} app
 */
function actualizarTabsActivas(app) {
  app.querySelectorAll(".tab").forEach((btn) => {
    const activa = btn.dataset.tab === tabActiva;
    btn.classList.toggle("is-active", activa);
    btn.setAttribute("aria-selected", String(activa));
  });
}
