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

/**
 * Modal de confirmación para acciones destructivas (eliminar).
 * @param {string} mensaje - Texto a mostrar.
 * @param {Function} onConfirm - Callback ejecutado al confirmar.
 * @returns {{close:Function, root:HTMLElement}}
 */
export function ConfirmModal(mensaje, onConfirm) {
  return Modal({
    titulo: "Confirmar acción",
    contenidoHtml: `<p>${escapeHtml(mensaje)}</p>`,
    acciones: [
      { label: "Cancelar", variant: "secondary", close: true },
      { label: "Eliminar", variant: "danger", close: true, onClick: onConfirm },
    ],
  });
}

/* -------------------------------------------------------------------------- */
/* EntityTable                                                                */
/* -------------------------------------------------------------------------- */

/**
 * Genera el HTML de una tabla reutilizable para los CRUDs.
 *
 * @param {object} opts
 * @param {Array<{key:string, label:string, type?:"text"|"badges"}>} opts.columns
 *   Definición de columnas. `type:"badges"` renderiza un arreglo como badges.
 * @param {Array<object>} opts.rows - Filas; cada objeto debe contener `id`.
 * @param {(id:string)=>boolean} [opts.canDelete] - Si retorna false, oculta el
 *   botón eliminar para esa fila (p. ej. entidad protegida).
 * @param {string} [opts.emptyText] - Texto cuando no hay filas.
 * @returns {string} HTML de la tabla.
 */
export function EntityTable({ columns, rows, canDelete = () => true, emptyText = "Sin registros." }) {
  if (!Array.isArray(rows) || rows.length === 0) {
    return `<p class="text-muted" style="padding: var(--space-4) 0;">${escapeHtml(emptyText)}</p>`;
  }

  const headCols = columns
    .map((c) => `<th>${escapeHtml(c.label)}</th>`)
    .join("");

  const bodyRows = rows
    .map((row) => {
      const cells = columns
        .map((c) => {
          const value = row[c.key];
          if (c.type === "badges") {
            const list = Array.isArray(value) ? value : [];
            const content =
              list.length > 0
                ? `<div class="badge-list">${list.map((v) => Badge(v)).join("")}</div>`
                : `<span class="text-muted">—</span>`;
            return `<td>${content}</td>`;
          }
          if (c.key === "id") {
            return `<td><code class="entity-id">${escapeHtml(value)}</code></td>`;
          }
          return `<td>${escapeHtml(value ?? "—")}</td>`;
        })
        .join("");

      const deleteBtn = canDelete(row.id)
        ? `<button class="btn btn--danger btn--sm" data-action="delete" aria-label="Eliminar ${escapeHtml(
            row.id
          )}">Eliminar</button>`
        : "";

      return `
        <tr data-id="${escapeHtml(row.id)}">
          ${cells}
          <td>
            <div class="table__actions">
              <button class="btn btn--ghost btn--sm" data-action="edit" aria-label="Editar ${escapeHtml(
                row.id
              )}">Editar</button>
              ${deleteBtn}
            </div>
          </td>
        </tr>`;
    })
    .join("");

  return `
    <div class="table-wrap">
      <table class="table">
        <thead>
          <tr>${headCols}<th aria-label="Acciones"></th></tr>
        </thead>
        <tbody>${bodyRows}</tbody>
      </table>
    </div>`;
}

/* -------------------------------------------------------------------------- */
/* Helpers de CRUD                                                            */
/* -------------------------------------------------------------------------- */

/** Patrón de ID válido para átomos de Prolog: minúscula inicial + [a-z0-9_]. */
export const ID_PATTERN = /^[a-z][a-z0-9_]*$/;

/**
 * Valida un ID contra el patrón aceptado por el backend.
 * @param {string} id
 * @returns {boolean}
 */
export function isValidId(id) {
  return ID_PATTERN.test(String(id ?? ""));
}

/**
 * Traduce un error de la capa API a un Toast con mensaje amigable.
 * Reutilizado por los tres módulos CRUD.
 * @param {{status:number, data:any}} err
 */
export function manejarErrorCrud(err) {
  const detalle = err?.data?.detail || "";
  switch (err?.status) {
    case 400:
      Toast(detalle || "No se encontró el elemento referenciado.", "error");
      break;
    case 404:
      Toast("El elemento no existe.", "error");
      break;
    case 409:
      Toast(
        detalle || "Ya existe un elemento con ese ID o la operación no está permitida.",
        "error"
      );
      break;
    case 422:
      Toast(
        "El ID debe iniciar con minúscula y contener solo letras, números o guion bajo.",
        "error"
      );
      break;
    case 0:
      Toast("No se pudo conectar con el servidor.", "error");
      break;
    default:
      Toast(detalle || "Ocurrió un error inesperado.", "error");
  }
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
