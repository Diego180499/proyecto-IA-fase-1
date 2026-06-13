/**
 * sintomas-crud.js — Tab de Síntomas de la Base de Conocimiento.
 *
 * CRUD completo sobre /api/sintomas. Cada síntoma puede tener N fallas asociadas
 * (relación causa/2). La edición de relaciones se hace con PUT (lista completa
 * de `fallas`), siguiendo la recomendación del análisis para el alcance académico.
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
let sintomas = [];
let fallas = []; // catálogo para los checkboxes
let filtro = "";

/**
 * Punto de entrada del tab.
 * @param {HTMLElement} container - Contenedor `#tab-content`.
 */
export function renderSintomasCrud(container) {
  filtro = "";
  container.innerHTML = Spinner("Cargando síntomas…");
  cargar(container);
}

/** Carga síntomas (con fallas) y el catálogo de fallas. */
async function cargar(container) {
  try {
    [sintomas, fallas] = await Promise.all([
      api.getSintomasDetalle(),
      api.getFallasDetalle(),
    ]);
    pintar(container);
  } catch (err) {
    const msg =
      err.status === 0
        ? "No se pudo conectar con el servidor. Verifica que la API esté en ejecución."
        : "No se pudieron cargar los síntomas. Intenta nuevamente.";
    container.innerHTML = `
      ${ErrorAlert(msg)}
      <div class="form-actions">
        <button class="btn btn--secondary" id="retryBtn">Reintentar</button>
      </div>`;
    document
      .getElementById("retryBtn")
      ?.addEventListener("click", () => renderSintomasCrud(container));
  }
}

/** Renderiza la barra de herramientas y la tabla con el filtro aplicado. */
function pintar(container) {
  const q = filtro.trim().toLowerCase();
  const rows = sintomas.filter(
    (s) =>
      !q ||
      s.id.toLowerCase().includes(q) ||
      (s.descripcion || "").toLowerCase().includes(q)
  );

  const hint = fallas.length === 0
    ? `<div class="crud-hint"><span aria-hidden="true">💡</span> Asegúrate de tener fallas creadas antes de asociarlas a un síntoma.</div>`
    : "";

  container.innerHTML = `
    ${hint}
    <div class="crud-toolbar">
      <button class="btn btn--primary" id="nuevoBtn">+ Nuevo síntoma</button>
      <input
        type="search"
        class="crud-search"
        id="buscarInput"
        placeholder="Buscar por ID o descripción…"
        value="${escapeHtml(filtro)}"
        aria-label="Buscar síntomas"
      />
    </div>
    <div id="tablaSintomas">
      ${EntityTable({
        columns: [
          { key: "id", label: "ID" },
          { key: "descripcion", label: "Descripción" },
          { key: "fallas", label: "Fallas", type: "badges" },
        ],
        rows,
        emptyText: q
          ? "Ningún síntoma coincide con la búsqueda."
          : "Aún no hay síntomas. Crea el primero para empezar.",
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
    const item = rows.find((s) => s.id === id);
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
  const seleccionadas = new Set(esEdicion ? item.fallas || [] : []);

  const checkboxes =
    fallas.length > 0
      ? `<div class="checkbox-grid">
          ${fallas
            .map(
              (f) => `
            <label class="checkbox-item">
              <input type="checkbox" name="falla" value="${escapeHtml(f.id)}" ${
                seleccionadas.has(f.id) ? "checked" : ""
              } />
              <span class="checkbox-item__text">
                ${escapeHtml(f.descripcion)}
                <span class="checkbox-item__id">${escapeHtml(f.id)}</span>
              </span>
            </label>`
            )
            .join("")}
        </div>`
      : `<p class="text-muted">No hay fallas disponibles. Créalas primero en su pestaña.</p>`;

  const cuerpo = `
    <form id="sintomaForm" novalidate>
      <div class="form-field" id="field-id">
        <label class="form-field__label" for="sintoma-id">ID *</label>
        <input
          class="form-field__input"
          id="sintoma-id"
          type="text"
          value="${esEdicion ? escapeHtml(item.id) : ""}"
          placeholder="pantalla_negra"
          ${esEdicion ? "disabled" : ""}
        />
        <span class="form-field__hint">Solo minúsculas, números y guion bajo. Debe iniciar con letra.</span>
        <span class="form-field__error" id="error-id" hidden></span>
      </div>

      <div class="form-field" id="field-desc">
        <label class="form-field__label" for="sintoma-desc">Descripción *</label>
        <textarea
          class="form-field__textarea"
          id="sintoma-desc"
          placeholder="Pantalla en negro al encender"
        >${esEdicion ? escapeHtml(item.descripcion) : ""}</textarea>
        <span class="form-field__error" id="error-desc" hidden></span>
      </div>

      <div class="form-field">
        <span class="form-field__label">Fallas asociadas</span>
        ${checkboxes}
      </div>
    </form>
  `;

  let modalRef;
  modalRef = Modal({
    titulo: esEdicion ? "Editar síntoma" : "Nuevo síntoma",
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
  const id = esEdicion ? item.id : document.getElementById("sintoma-id").value.trim();
  const descripcion = document.getElementById("sintoma-desc").value.trim();
  const fallasSel = [...document.querySelectorAll('input[name="falla"]:checked')].map(
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
      await api.actualizarSintoma(id, { descripcion, fallas: fallasSel });
      Toast("Síntoma actualizado.", "success");
    } else {
      await api.crearSintoma({ id, descripcion, fallas: fallasSel });
      Toast("Síntoma creado.", "success");
    }
    modalRef.close();
    renderSintomasCrud(container);
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
 * Confirma y ejecuta la eliminación de un síntoma.
 * @param {HTMLElement} container
 * @param {string} id
 */
function confirmarEliminar(container, id) {
  ConfirmModal(
    `¿Eliminar el síntoma "${id}"? Esta acción no se puede deshacer.`,
    async () => {
      try {
        await api.eliminarSintoma(id);
        Toast("Síntoma eliminado.", "success");
        renderSintomasCrud(container);
      } catch (err) {
        manejarErrorCrud(err);
      }
    }
  );
}
