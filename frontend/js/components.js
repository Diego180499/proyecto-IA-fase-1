/**
 * components.js — Componentes reutilizables de UI.
 *
 * Los componentes "de string" devuelven HTML listo para inyectar con innerHTML.
 * Los componentes "interactivos" (Toast, Modal) manipulan el DOM directamente.
 */

/**
 * Escapa texto para prevenir inyección de HTML al usar innerHTML.
 * @param {unknown} value
 * @returns {string}
 */
export function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

/**
 * Etiqueta pequeña.
 * @param {string} texto
 * @param {"default"|"success"|"error"|"muted"} [variant]
 */
export function Badge(texto, variant = "default") {
  const cls = variant === "default" ? "badge" : `badge badge--${variant}`;
  return `<span class="${cls}">${escapeHtml(texto)}</span>`;
}

/**
 * Contenedor con sombra y borde.
 * @param {string} titulo
 * @param {string} contenidoHtml - HTML ya escapado/confiable.
 */
export function Card(titulo, contenidoHtml) {
  const head = titulo ? `<h3 class="card__title">${escapeHtml(titulo)}</h3>` : "";
  return `<div class="card">${head}${contenidoHtml}</div>`;
}

/**
 * Indicador de carga circular.
 * @param {string} [mensaje]
 */
export function Spinner(mensaje = "Cargando…") {
  return `
    <div class="spinner-wrap">
      <div class="spinner" role="status" aria-label="${escapeHtml(mensaje)}"></div>
      <p>${escapeHtml(mensaje)}</p>
    </div>`;
}

/**
 * Estado vacío con ícono, mensaje y CTA opcional.
 * @param {string} mensaje
 * @param {{href:string,label:string}} [cta]
 * @param {string} [icon]
 */
export function EmptyState(mensaje, cta = null, icon = "🗂") {
  const ctaHtml = cta
    ? `<a href="${escapeHtml(cta.href)}" class="btn btn--primary">${escapeHtml(cta.label)}</a>`
    : "";
  return `
    <div class="empty-state">
      <div class="empty-state__icon" aria-hidden="true">${icon}</div>
      <p class="empty-state__message">${escapeHtml(mensaje)}</p>
      ${ctaHtml}
    </div>`;
}

/**
 * Bloque de error con estilo de alerta.
 * @param {string} mensaje
 */
export function ErrorAlert(mensaje) {
  return `
    <div class="alert alert--error" role="alert">
      <span aria-hidden="true">⚠</span>
      <span>${escapeHtml(mensaje)}</span>
    </div>`;
}

/* -------------------------------------------------------------------------- */
/* Toast                                                                      */
/* -------------------------------------------------------------------------- */

/**
 * Muestra una notificación temporal en la esquina superior derecha.
 * @param {string} mensaje
 * @param {"info"|"success"|"error"} [tipo]
 * @param {number} [duracionMs]
 */
export function Toast(mensaje, tipo = "info", duracionMs = 3200) {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const el = document.createElement("div");
  el.className = `toast toast--${tipo}`;
  el.setAttribute("role", "status");
  el.textContent = mensaje;
  container.appendChild(el);

  const remove = () => {
    el.classList.add("is-leaving");
    el.addEventListener("animationend", () => el.remove(), { once: true });
  };
  setTimeout(remove, duracionMs);
}

/* -------------------------------------------------------------------------- */
/* Modal                                                                      */
/* -------------------------------------------------------------------------- */

/**
 * Renderiza un modal de superposición con scroll interno.
 * @param {object} opts
 * @param {string} opts.titulo
 * @param {string} opts.contenidoHtml - HTML confiable a inyectar en el cuerpo.
 * @param {Array<{label:string, variant?:string, onClick?:Function, close?:boolean}>} [opts.acciones]
 * @returns {{close:Function, root:HTMLElement}}
 */
export function Modal({ titulo, contenidoHtml, acciones = [] }) {
  const root = document.getElementById("modal-root");

  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true" aria-label="${escapeHtml(titulo)}">
      <div class="modal__header">
        <h2 class="modal__title">${escapeHtml(titulo)}</h2>
        <button class="modal__close" aria-label="Cerrar">×</button>
      </div>
      <div class="modal__body">${contenidoHtml}</div>
      <div class="modal__footer"></div>
    </div>`;

  const close = () => {
    document.removeEventListener("keydown", onKey);
    overlay.remove();
  };

  const onKey = (e) => {
    if (e.key === "Escape") close();
  };

  // Cerrar al hacer clic fuera del modal o en la "X".
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) close();
  });
  overlay.querySelector(".modal__close").addEventListener("click", close);
  document.addEventListener("keydown", onKey);

  // Acciones del pie. Si no hay, se ofrece un botón "Cerrar" por defecto.
  const footer = overlay.querySelector(".modal__footer");
  const lista =
    acciones.length > 0
      ? acciones
      : [{ label: "Cerrar", variant: "primary", close: true }];

  lista.forEach((accion) => {
    const btn = document.createElement("button");
    btn.className = `btn btn--${accion.variant || "secondary"}`;
    btn.textContent = accion.label;
    btn.addEventListener("click", async () => {
      if (accion.onClick) await accion.onClick();
      if (accion.close !== false) close();
    });
    footer.appendChild(btn);
  });

  root.appendChild(overlay);
  return { close, root: overlay };
}

/* -------------------------------------------------------------------------- */
/* Helpers de formato                                                         */
/* -------------------------------------------------------------------------- */

/**
 * Formatea un timestamp ISO 8601 a un formato legible en español.
 * @param {string} iso
 * @returns {string}
 */
export function formatTimestamp(iso) {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso ?? "—";
  return date.toLocaleString("es-GT", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
