/**
 * router.js — Hash router minimalista de la SPA.
 *
 * Escucha `hashchange`/`load` y renderiza la vista correspondiente dentro de
 * `#app`. Si el hash no coincide con ninguna ruta, redirige a `#/`.
 */
import { renderHome } from "./views/home.js";
import { renderDiagnostico } from "./views/diagnostico.js";
import { renderHistorial } from "./views/historial.js";
import { renderConocimiento } from "./views/conocimiento.js";

const routes = {
  "#/": renderHome,
  "#/diagnostico": renderDiagnostico,
  "#/historial": renderHistorial,
  "#/conocimiento": renderConocimiento,
};

const DEFAULT_ROUTE = "#/";

/**
 * Navegación programática.
 * @param {string} hash - p. ej. "#/diagnostico"
 */
export function navigate(hash) {
  if (window.location.hash === hash) {
    // Forzar re-render aunque el hash no cambie.
    handleRoute();
  } else {
    window.location.hash = hash;
  }
}

/** Marca el enlace activo en la navbar según el hash actual. */
function updateActiveLink(hash) {
  document.querySelectorAll(".navbar__link").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.route === hash);
  });
}

/** Cierra el menú móvil (si está abierto) tras navegar. */
function closeMobileMenu() {
  const menu = document.getElementById("navMenu");
  const toggle = document.getElementById("navToggle");
  if (menu) menu.classList.remove("is-open");
  if (toggle) toggle.setAttribute("aria-expanded", "false");
}

/** Resuelve y renderiza la vista de la ruta actual. */
function handleRoute() {
  const app = document.getElementById("app");
  let hash = window.location.hash || DEFAULT_ROUTE;

  // Normaliza rutas con query/params extra (no usadas, pero defensivo).
  const view = routes[hash];

  if (!view) {
    window.location.hash = DEFAULT_ROUTE;
    return;
  }

  updateActiveLink(hash);
  closeMobileMenu();
  window.scrollTo({ top: 0 });

  // Limpia cualquier modal abierto al cambiar de vista.
  const modalRoot = document.getElementById("modal-root");
  if (modalRoot) modalRoot.innerHTML = "";

  view(app);
}

/** Inicializa el botón de menú hamburguesa. */
function initMobileMenu() {
  const toggle = document.getElementById("navToggle");
  const menu = document.getElementById("navMenu");
  if (!toggle || !menu) return;

  toggle.addEventListener("click", () => {
    const isOpen = menu.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });
}

window.addEventListener("hashchange", handleRoute);
window.addEventListener("DOMContentLoaded", () => {
  initMobileMenu();
  if (!window.location.hash) {
    window.location.hash = DEFAULT_ROUTE;
  } else {
    handleRoute();
  }
});
