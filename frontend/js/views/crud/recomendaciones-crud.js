/**
 * recomendaciones-crud.js — Tab de Recomendaciones de la Base de Conocimiento.
 *
 * CRUD completo sobre /api/recomendaciones. Es el recurso más simple: no tiene
 * relaciones que gestionar desde esta vista. La recomendación `rec_servicio_tecnico`
 * está protegida y no puede eliminarse (el backend retorna 409); por eso se oculta
 * su botón de eliminar.
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

/** ID de la recomendación protegida que no puede eliminarse. */
const REC_PROTEGIDA = "rec_servicio_tecnico";

/** Estado local del módulo. */
let recomendaciones = [];
let filtro = "";

/**
 * Punto de entrada del tab.
 * @param {HTMLElement} container - Contenedor `#tab-content`.
 */
export function renderRecomendacionesCrud(container) {
  filtro = "";
  container.innerHTML = Spinner("Cargando recomendaciones…");
  cargar(container);
}

/** Carga el catálogo de recomendaciones y renderiza la tabla. */
async function cargar(container) {
  try {
    recomendaciones = await api.getRecomendaciones();
    pintar(container);
  } catch (err) {
    const msg =
      err.status === 0
        ? "No se pudo conectar con el servidor. Verifica que la API esté en ejecución."
        : "No se pudieron cargar las recomendaciones. Intenta nuevamente.";
    container.innerHTML = `
      ${ErrorAlert(msg)}
      <div class="form-actions">
        <button class="btn btn--secondary" id="retryBtn">Reintentar</button>
      </div>`;
    document
      .getElementById("retryBtn")
      ?.addEventListener("click", () => renderRecomendacionesCrud(container));
  }
}

/** Renderiza la barra de herramientas y la tabla con el filtro aplicado. */
function pintar(container) {
  const q = filtro.trim().toLowerCase();
  const rows = recomendaciones.filter(
    (r) =>
      !q ||
      r.id.toLowerCase().includes(q) ||
      (r.descripcion || "").toLowerCase().includes(q)
  );

  container.innerHTML = `
    <div class="crud-toolbar">
      <button class="btn btn--primary" id="nuevoBtn">+ Nueva recomendación</button>
      <input
        type="search"
        class="crud-search"
        id="buscarInput"
        placeholder="Buscar por ID o descripción…"
        value="${escapeHtml(filtro)}"
        aria-label="Buscar recomendaciones"
      />
    </div>
    <div id="tablaRec">
      ${EntityTable({
        columns: [
          { key: "id", label: "ID" },
          { key: "descripcion", label: "Descripción" },
        ],
        rows,
        canDelete: (id) => id !== REC_PROTEGIDA,
        emptyText: q
          ? "Ninguna recomendación coincide con la búsqueda."
          : "Aún no hay recomendaciones. Crea la primera para empezar.",
      })}
    </div>
  `;

  document.getElementById("nuevoBtn").addEventListener("click", () => abrirForm(container, null));

  const buscar = document.getElementById("buscarInput");
  buscar.addEventListener("input", (e) => {
    filtro = e.target.value;
    pintar(container);
    // Mantener el foco en el buscador tras re-render.
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
    const item = rows.find((r) => r.id === id);
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

  const cuerpo = `
    <form id="recForm" novalidate>
      <div class="form-field" id="field-id">
        <label class="form-field__label" for="rec-id">ID *</label>
        <input
          class="form-field__input"
          id="rec-id"
          type="text"
          value="${esEdicion ? escapeHtml(item.id) : ""}"
          placeholder="rec_verificar_ram"
          ${esEdicion ? "disabled" : ""}
        />
        <span class="form-field__hint">Solo minúsculas, números y guion bajo. Debe iniciar con letra.</span>
        <span class="form-field__error" id="error-id" hidden></span>
      </div>

      <div class="form-field" id="field-desc">
        <label class="form-field__label" for="rec-desc">Descripción *</label>
        <textarea
          class="form-field__textarea"
          id="rec-desc"
          placeholder="Verificar y reemplazar módulos de RAM"
        >${esEdicion ? escapeHtml(item.descripcion) : ""}</textarea>
        <span class="form-field__error" id="error-desc" hidden></span>
      </div>
    </form>
  `;

  let modalRef;
  modalRef = Modal({
    titulo: esEdicion ? "Editar recomendación" : "Nueva recomendación",
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
  const id = esEdicion ? item.id : document.getElementById("rec-id").value.trim();
  const descripcion = document.getElementById("rec-desc").value.trim();

  let valido = true;
  if (!esEdicion) {
    valido = setError("id", isValidId(id) ? "" : "El ID debe iniciar con minúscula y contener solo letras, números o guion bajo.") && valido;
  }
  valido = setError("desc", descripcion ? "" : "La descripción no puede estar vacía.") && valido;
  if (!valido) return;

  try {
    if (esEdicion) {
      await api.actualizarRecomendacion(id, { descripcion });
      Toast("Recomendación actualizada.", "success");
    } else {
      await api.crearRecomendacion({ id, descripcion });
      Toast("Recomendación creada.", "success");
    }
    modalRef.close();
    renderRecomendacionesCrud(container);
  } catch (err) {
    manejarErrorCrud(err);
  }
}

/**
 * Muestra/limpia el mensaje de error de un campo.
 * @param {"id"|"desc"} campo
 * @param {string} mensaje - Vacío para limpiar.
 * @returns {boolean} true si el campo es válido.
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
 * Confirma y ejecuta la eliminación de una recomendación.
 * @param {HTMLElement} container
 * @param {string} id
 */
function confirmarEliminar(container, id) {
  ConfirmModal(
    `¿Eliminar la recomendación "${id}"? Esta acción no se puede deshacer.`,
    async () => {
      try {
        await api.eliminarRecomendacion(id);
        Toast("Recomendación eliminada.", "success");
        renderRecomendacionesCrud(container);
      } catch (err) {
        manejarErrorCrud(err);
      }
    }
  );
}
