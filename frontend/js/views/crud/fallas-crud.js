/**
 * fallas-crud.js — Tab de Fallas de la Base de Conocimiento.
 *
 * CRUD completo sobre /api/fallas. Cada falla puede tener N recomendaciones.
 * La edición de relaciones se hace con PUT (lista completa de `recomendaciones`).
 * Al eliminar una falla, el backend la desvincula en cascada de los síntomas.
 */
import { api } from "../../api.js";
import {
  Spinner,
  ErrorAlert,
  EntityTable,
  ConfirmModal,
  Modal,
  Toast,
  isValidId,
  manejarErrorCrud,
  escapeHtml,
} from "../../components.js";

/** Estado local del módulo. */
let fallas = [];
let recomendaciones = []; // catálogo para los checkboxes
let filtro = "";

/**
 * Punto de entrada del tab.
 * @param {HTMLElement} container - Contenedor `#tab-content`.
 */
export function renderFallasCrud(container) {
  filtro = "";
  container.innerHTML = Spinner("Cargando fallas…");
  cargar(container);
}

/** Carga fallas (con recomendaciones) y el catálogo de recomendaciones. */
async function cargar(container) {
  try {
    [fallas, recomendaciones] = await Promise.all([
      api.getFallasDetalle(),
      api.getRecomendaciones(),
    ]);
    pintar(container);
  } catch (err) {
    const msg =
      err.status === 0
        ? "No se pudo conectar con el servidor. Verifica que la API esté en ejecución."
        : "No se pudieron cargar las fallas. Intenta nuevamente.";
    container.innerHTML = `
      ${ErrorAlert(msg)}
      <div class="form-actions">
        <button class="btn btn--secondary" id="retryBtn">Reintentar</button>
      </div>`;
    document
      .getElementById("retryBtn")
      ?.addEventListener("click", () => renderFallasCrud(container));
  }
}

/** Renderiza la barra de herramientas y la tabla con el filtro aplicado. */
function pintar(container) {
  const q = filtro.trim().toLowerCase();
  const rows = fallas.filter(
    (f) =>
      !q ||
      f.id.toLowerCase().includes(q) ||
      (f.descripcion || "").toLowerCase().includes(q)
  );

  const hint = recomendaciones.length === 0
    ? `<div class="crud-hint"><span aria-hidden="true">💡</span> Crea recomendaciones antes de asociarlas a una falla.</div>`
    : "";

  container.innerHTML = `
    ${hint}
    <div class="crud-toolbar">
      <button class="btn btn--primary" id="nuevoBtn">+ Nueva falla</button>
      <input
        type="search"
        class="crud-search"
        id="buscarInput"
        placeholder="Buscar por ID o descripción…"
        value="${escapeHtml(filtro)}"
        aria-label="Buscar fallas"
      />
    </div>
    <div id="tablaFallas">
      ${EntityTable({
        columns: [
          { key: "id", label: "ID" },
          { key: "descripcion", label: "Descripción" },
          { key: "recomendaciones", label: "Recomendaciones", type: "badges" },
        ],
        rows,
        emptyText: q
          ? "Ninguna falla coincide con la búsqueda."
          : "Aún no hay fallas. Crea la primera para empezar.",
      })}
    </div>
  `;

  document.getElementById("nuevoBtn").addEventListener("click", () => abrirForm(container, null));

  const buscar = document.getElementById("buscarInput");
  buscar.addEventListener("input", (e) => {
    filtro = e.target.value;
    pintar(container);
    const nuevo = document.getElementById("buscarInput");
    nuevo.focus();
    nuevo.setSelectionRange(nuevo.value.length, nuevo.value.length);
  });

  vincularAcciones(container, rows);
}

/** Vincula los botones Editar/Eliminar de cada fila. */
function vincularAcciones(container, rows) {
  container.querySelectorAll("tr[data-id]").forEach((tr) => {
    const id = tr.dataset.id;
    const item = rows.find((f) => f.id === id);
    tr.querySelector('[data-action="edit"]')?.addEventListener("click", () =>
      abrirForm(container, item)
    );
    tr.querySelector('[data-action="delete"]')?.addEventListener("click", () =>
      confirmarEliminar(container, id)
    );
  });
}

/**
 * Abre el modal de crear o editar.
 * @param {HTMLElement} container
 * @param {object|null} item - null para crear; objeto para editar.
 */
function abrirForm(container, item) {
  const esEdicion = Boolean(item);
  const seleccionadas = new Set(esEdicion ? item.recomendaciones || [] : []);

  const checkboxes =
    recomendaciones.length > 0
      ? `<div class="checkbox-grid">
          ${recomendaciones
            .map(
              (r) => `
            <label class="checkbox-item">
              <input type="checkbox" name="rec" value="${escapeHtml(r.id)}" ${
                seleccionadas.has(r.id) ? "checked" : ""
              } />
              <span class="checkbox-item__text">
                ${escapeHtml(r.descripcion)}
                <span class="checkbox-item__id">${escapeHtml(r.id)}</span>
              </span>
            </label>`
            )
            .join("")}
        </div>`
      : `<p class="text-muted">No hay recomendaciones disponibles. Créalas primero en su pestaña.</p>`;

  const cuerpo = `
    <form id="fallaForm" novalidate>
      <div class="form-field" id="field-id">
        <label class="form-field__label" for="falla-id">ID *</label>
        <input
          class="form-field__input"
          id="falla-id"
          type="text"
          value="${esEdicion ? escapeHtml(item.id) : ""}"
          placeholder="falla_ram"
          ${esEdicion ? "disabled" : ""}
        />
        <span class="form-field__hint">Solo minúsculas, números y guion bajo. Debe iniciar con letra.</span>
        <span class="form-field__error" id="error-id" hidden></span>
      </div>

      <div class="form-field" id="field-desc">
        <label class="form-field__label" for="falla-desc">Descripción *</label>
        <textarea
          class="form-field__textarea"
          id="falla-desc"
          placeholder="Falla en módulo RAM"
        >${esEdicion ? escapeHtml(item.descripcion) : ""}</textarea>
        <span class="form-field__error" id="error-desc" hidden></span>
      </div>

      <div class="form-field">
        <span class="form-field__label">Recomendaciones asociadas</span>
        ${checkboxes}
      </div>
    </form>
  `;

  let modalRef;
  modalRef = Modal({
    titulo: esEdicion ? "Editar falla" : "Nueva falla",
    contenidoHtml: cuerpo,
    acciones: [
      { label: "Cancelar", variant: "secondary", close: true },
      {
        label: "Guardar",
        variant: "primary",
        close: false,
        onClick: () => guardar(container, item, modalRef),
      },
    ],
  });
}

/**
 * Valida y persiste el formulario.
 * @param {HTMLElement} container
 * @param {object|null} item
 * @param {{close:Function}} modalRef
 */
async function guardar(container, item, modalRef) {
  const esEdicion = Boolean(item);
  const id = esEdicion ? item.id : document.getElementById("falla-id").value.trim();
  const descripcion = document.getElementById("falla-desc").value.trim();
  const recs = [...document.querySelectorAll('input[name="rec"]:checked')].map(
    (c) => c.value
  );

  let valido = true;
  if (!esEdicion) {
    valido = setError("id", isValidId(id) ? "" : "El ID debe iniciar con minúscula y contener solo letras, números o guion bajo.") && valido;
  }
  valido = setError("desc", descripcion ? "" : "La descripción no puede estar vacía.") && valido;
  if (!valido) return;

  try {
    if (esEdicion) {
      await api.actualizarFalla(id, { descripcion, recomendaciones: recs });
      Toast("Falla actualizada.", "success");
    } else {
      await api.crearFalla({ id, descripcion, recomendaciones: recs });
      Toast("Falla creada.", "success");
    }
    modalRef.close();
    renderFallasCrud(container);
  } catch (err) {
    manejarErrorCrud(err);
  }
}

/**
 * Muestra/limpia el mensaje de error de un campo.
 * @param {"id"|"desc"} campo
 * @param {string} mensaje
 * @returns {boolean}
 */
function setError(campo, mensaje) {
  const field = document.getElementById(`field-${campo}`);
  const error = document.getElementById(`error-${campo}`);
  if (!field || !error) return true;
  if (mensaje) {
    field.classList.add("form-field--error");
    error.textContent = mensaje;
    error.hidden = false;
    return false;
  }
  field.classList.remove("form-field--error");
  error.hidden = true;
  return true;
}

/**
 * Confirma y ejecuta la eliminación de una falla.
 * @param {HTMLElement} container
 * @param {string} id
 */
function confirmarEliminar(container, id) {
  ConfirmModal(
    `¿Eliminar la falla "${id}"? Se desvinculará de todos los síntomas asociados. Esta acción no se puede deshacer.`,
    async () => {
      try {
        await api.eliminarFalla(id);
        Toast("Falla eliminada y desvinculada de los síntomas asociados.", "success");
        renderFallasCrud(container);
      } catch (err) {
        manejarErrorCrud(err);
      }
    }
  );
}
