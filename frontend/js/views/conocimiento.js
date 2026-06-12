/**
 * conocimiento.js — Vista de Base de Conocimiento (`#/conocimiento`).
 *
 * Agrupa los tres CRUDs (Síntomas, Fallas, Recomendaciones) en una sola página
 * con pestañas. Cada pestaña delega el render a su módulo correspondiente sobre
 * el contenedor `#tab-content`.
 */
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
      <h1 class="page-header__title">Base de Conocimiento</h1>
      <p class="page-header__subtitle">
        Gestiona los síntomas, fallas y recomendaciones del sistema experto.
      </p>
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
