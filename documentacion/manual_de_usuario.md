# Manual de Usuario — Doctor Byte

> Sistema experto para el diagnóstico de fallas en computadoras.
> Este manual explica cómo utilizar cada sección y cada botón de la aplicación web.

---

## Tabla de Contenidos

1. [Acceso a la aplicación](#1-acceso-a-la-aplicación)
2. [Estructura general de la interfaz](#2-estructura-general-de-la-interfaz)
3. [Referencia de botones y controles](#3-referencia-de-botones-y-controles)
4. [Cómo usar la aplicación](#4-cómo-usar-la-aplicación)
   - 4.1 [Cómo realizar un diagnóstico](#41-cómo-realizar-un-diagnóstico)
   - 4.2 [Cómo consultar el historial de diagnósticos](#42-cómo-consultar-el-historial-de-diagnósticos)
   - 4.3 [Cómo ver el detalle de un diagnóstico anterior](#43-cómo-ver-el-detalle-de-un-diagnóstico-anterior)
   - 4.4 [Cómo eliminar un diagnóstico del historial](#44-cómo-eliminar-un-diagnóstico-del-historial)
   - 4.5 [Cómo gestionar síntomas (crear, editar, eliminar)](#45-cómo-gestionar-síntomas-crear-editar-eliminar)
   - 4.6 [Cómo asociar o desasociar una falla a un síntoma](#46-cómo-asociar-o-desasociar-una-falla-a-un-síntoma)
   - 4.7 [Cómo gestionar fallas (crear, editar, eliminar)](#47-cómo-gestionar-fallas-crear-editar-eliminar)
   - 4.8 [Cómo asociar o desasociar una recomendación a una falla](#48-cómo-asociar-o-desasociar-una-recomendación-a-una-falla)
   - 4.9 [Cómo gestionar recomendaciones (crear, editar, eliminar)](#49-cómo-gestionar-recomendaciones-crear-editar-eliminar)
   - 4.10 [Cómo activar o desactivar el bot de Telegram](#410-cómo-activar-o-desactivar-el-bot-de-telegram)
5. [Verificar el estado del sistema](#5-verificar-el-estado-del-sistema)
6. [Mensajes del sistema](#6-mensajes-del-sistema)
7. [Preguntas frecuentes](#7-preguntas-frecuentes)

---

## 1. Acceso a la aplicación

Para acceder a Doctor Byte, abre tu navegador web y escribe la siguiente dirección:

```
http://localhost:5500
```

> **Requisito previo:** El servidor backend debe estar corriendo en `http://localhost:8000` antes de abrir la aplicación. Si el backend no está activo, la aplicación mostrará mensajes de error indicando que no puede conectarse al servidor.

Al cargar, verás la página de **Inicio** con el nombre "Doctor Byte" y un botón para comenzar el diagnóstico.

---

## 2. Estructura general de la interfaz

La aplicación tiene tres zonas fijas que están presentes en todas las páginas:

### Barra de navegación (parte superior)

La barra azul oscura en la parte superior contiene:

- **Logotipo "Doctor Byte"** — Al hacer clic en él regresarás siempre a la página de Inicio.
- **Enlace "Inicio"** — Navega a la página principal.
- **Enlace "Diagnóstico"** — Navega a la herramienta de diagnóstico de fallas.
- **Enlace "Historial"** — Navega a la lista de diagnósticos realizados anteriormente.
- **Enlace "Modulo Administración"** — Navega al panel de gestión de la base de conocimiento.

El enlace de la página actualmente visible aparece subrayado o resaltado para indicar en qué sección te encuentras.

En pantallas pequeñas (móvil), los enlaces se ocultan y aparece un **botón de menú hamburguesa** (tres líneas horizontales) en la esquina derecha de la barra. Al presionarlo se despliega el menú de navegación.

### Área de contenido principal

Es la zona central donde se carga el contenido de cada sección según la página que estés visitando.

### Pie de página (parte inferior)

Muestra el nombre "Doctor Byte" y una breve descripción del sistema. Es meramente informativo.

---

## 3. Referencia de botones y controles

Esta sección lista todos los botones disponibles en la aplicación y explica para qué sirve cada uno.

### Botones de navegación

| Botón / Enlace | Ubicación | Función |
|---|---|---|
| **Doctor Byte** (logotipo) | Navbar | Regresa a la página de Inicio |
| **Inicio** | Navbar | Navega a la página principal |
| **Diagnóstico** | Navbar | Abre la herramienta de diagnóstico |
| **Historial** | Navbar | Abre el listado de diagnósticos pasados |
| **Modulo Administración** | Navbar | Abre el panel de administración del sistema experto |
| **☰** (hamburguesa) | Navbar (móvil) | Despliega/oculta el menú en pantallas pequeñas |

### Botones de la página Inicio

| Botón | Función |
|---|---|
| **Iniciar diagnóstico** | Lleva directamente a la vista de Diagnóstico para comenzar a evaluar síntomas |

### Botones de la vista Diagnóstico

| Botón / Control | Función |
|---|---|
| **Casillas de verificación (checkboxes)** | Selecciona los síntomas que presenta el equipo. Puede marcar una o varias. |
| **Analizar** | Envía los síntomas seleccionados al motor de inferencia y muestra el resultado del diagnóstico. Solo se activa cuando hay al menos un síntoma seleccionado. |
| **Limpiar selección** | Desmarca todos los checkboxes seleccionados sin recargar la página. |
| **Reintentar** | Aparece solo si hubo un error al cargar los síntomas. Vuelve a intentar la carga desde el servidor. |
| **Nuevo diagnóstico** | Aparece después de mostrar un resultado. Limpia el resultado y regresa al formulario de selección de síntomas para iniciar otro diagnóstico. |

### Botones de la vista Historial

| Botón / Control | Función |
|---|---|
| **Selector "Por página"** (10 / 20 / 50) | Controla cuántos registros se muestran por página en la tabla del historial. |
| **← Anterior** | Navega a la página anterior del historial. Está deshabilitado cuando estás en la primera página. |
| **Siguiente →** | Navega a la siguiente página del historial. Está deshabilitado cuando no hay más registros. |
| **Ver detalle** | Abre un modal con el detalle completo del diagnóstico seleccionado (síntomas, fallas y recomendaciones). |
| **Eliminar** | Elimina el diagnóstico seleccionado del historial. Pide confirmación antes de proceder. |
| **Reintentar** | Aparece si hubo un error al cargar el historial. Vuelve a intentar la carga. |

### Botones del modal de detalle (Historial)

| Botón | Función |
|---|---|
| **×** (cerrar) | Cierra el modal de detalle sin realizar cambios. |
| **Cerrar** | Cierra el modal de detalle (mismo efecto que la × o presionar Escape). |

### Botones del Módulo de Administración

| Botón / Control | Función |
|---|---|
| **Pestaña "Síntomas"** | Muestra la tabla de gestión de síntomas de la base de conocimiento. |
| **Pestaña "Fallas"** | Muestra la tabla de gestión de fallas de la base de conocimiento. |
| **Pestaña "Recomendaciones"** | Muestra la tabla de gestión de recomendaciones de la base de conocimiento. |
| **Bot Activado / Bot Desactivado** | Interruptor en la esquina superior derecha que activa o desactiva el envío automático de diagnósticos al bot de Telegram. |

### Botones comunes en los CRUDs (Síntomas, Fallas, Recomendaciones)

| Botón | Función |
|---|---|
| **Agregar [síntoma / falla / recomendación]** | Abre un formulario para crear una nueva entidad en la base de conocimiento. |
| **Editar** | Abre un modal con el formulario de edición del registro seleccionado. |
| **Eliminar** | Elimina el registro seleccionado. Pide confirmación antes de proceder. |

### Botones de los formularios modales (CRUD)

| Botón | Función |
|---|---|
| **Guardar** | Envía el formulario y crea o actualiza el registro en la base de conocimiento. |
| **Cancelar** | Cierra el modal sin guardar ningún cambio. |
| **×** (cerrar) | Cierra el modal (mismo efecto que Cancelar). |
| **Eliminar** (en modal de confirmación) | Confirma la eliminación del registro seleccionado. |

---

## 4. Cómo usar la aplicación

### 4.1 Cómo realizar un diagnóstico

El diagnóstico es la función principal de Doctor Byte. Permite identificar las posibles fallas de un equipo de cómputo a partir de los síntomas que presenta.

**Pasos:**

1. En la barra de navegación, haz clic en **"Diagnóstico"**. También puedes hacer clic en el botón **"Iniciar diagnóstico"** desde la página de Inicio.

2. La aplicación cargará la lista de síntomas disponibles. Verás una cuadrícula de opciones con nombres descriptivos como "Pantalla en negro al encender el equipo", "El equipo se reinicia solo sin previo aviso", etc.

3. Marca con un clic las casillas de verificación correspondientes a **todos los síntomas que presenta el equipo**. Puedes seleccionar uno o varios síntomas al mismo tiempo. El contador en la parte superior ("0 seleccionados") se actualiza en tiempo real.

4. Una vez seleccionado al menos un síntoma, el botón **"Analizar"** se activará (dejará de estar en gris). Haz clic en él.

5. La aplicación enviará los síntomas al motor de inferencia. Verás un indicador de carga ("Analizando síntomas…") mientras se procesa.

6. En pocos segundos aparecerá el resultado del diagnóstico con tres secciones:
   - **Síntomas ingresados:** los síntomas que seleccionaste, mostrados como etiquetas.
   - **Fallas detectadas:** las fallas que el sistema identificó como probables causas, con su descripción.
   - **Recomendaciones:** la lista ordenada de acciones sugeridas para resolver las fallas encontradas.

7. Si deseas realizar otro diagnóstico, haz clic en el botón **"Nuevo diagnóstico"** para limpiar el resultado y regresar al formulario.

> **Nota:** Si deseas desmarcar todos los síntomas de una sola vez, usa el botón **"Limpiar selección"** en cualquier momento antes de presionar "Analizar".

> **Resultado especial:** Si el sistema no puede determinar una falla a partir de los síntomas ingresados, mostrará el resultado "No se pudo determinar una falla a partir de los síntomas" con la recomendación de llevar el equipo a servicio técnico especializado.

---

### 4.2 Cómo consultar el historial de diagnósticos

El historial guarda todos los diagnósticos que se han realizado en la aplicación. Puedes consultarlos en cualquier momento.

**Pasos:**

1. En la barra de navegación, haz clic en **"Historial"**.

2. La aplicación cargará la lista de diagnósticos ordenados del más reciente al más antiguo. Cada fila de la tabla muestra:
   - **Fecha:** cuándo se realizó el diagnóstico.
   - **Síntomas ingresados:** un resumen de los síntomas (si hay más de 3, muestra los primeros 3 y un contador con los restantes, ej. "+2").
   - **Fallas:** el número de fallas detectadas en ese diagnóstico.

3. Usa el selector **"Por página"** (opciones: 10, 20 o 50) para controlar cuántos registros ves al mismo tiempo.

4. Usa los botones **"← Anterior"** y **"Siguiente →"** para navegar entre páginas cuando hay muchos diagnósticos.

> **Si el historial está vacío:** verás un mensaje "No hay diagnósticos registrados aún." con un botón **"Crear un diagnóstico"** que te llevará a la vista de Diagnóstico.

---

### 4.3 Cómo ver el detalle de un diagnóstico anterior

**Pasos:**

1. Ve a la sección **"Historial"** siguiendo los pasos del punto 4.2.

2. Localiza el diagnóstico que deseas consultar en la tabla.

3. Haz clic en el botón **"Ver detalle"** en la fila correspondiente.

4. Se abrirá un modal (ventana emergente) con el detalle completo:
   - **Fecha y ID del diagnóstico.**
   - **Síntomas ingresados** mostrados como etiquetas.
   - **Fallas detectadas** con el identificador y descripción de cada falla.
   - **Recomendaciones** numeradas para resolver las fallas encontradas.

5. Para cerrar el modal, haz clic en el botón **"Cerrar"**, en la **×** de la esquina superior derecha, o presiona la tecla **Escape**.

---

### 4.4 Cómo eliminar un diagnóstico del historial

**Pasos:**

1. Ve a la sección **"Historial"**.

2. Localiza el diagnóstico que deseas eliminar.

3. Haz clic en el botón **"Eliminar"** (en rojo) de la fila correspondiente.

4. El navegador mostrará un cuadro de confirmación preguntando: *"¿Eliminar este diagnóstico del historial? Esta acción no se puede deshacer."*

5. Haz clic en **"Aceptar"** para confirmar la eliminación o en **"Cancelar"** para abortarla.

6. Si confirmas, el diagnóstico desaparecerá de la lista y verás una notificación verde en la esquina superior derecha confirmando "Diagnóstico eliminado."

> **Advertencia:** La eliminación es permanente y no se puede recuperar el registro una vez eliminado.

---

### 4.5 Cómo gestionar síntomas (crear, editar, eliminar)

Los síntomas son las señales o comportamientos que puede presentar un equipo de cómputo. Desde el Módulo de Administración puedes agregar nuevos síntomas, modificar los existentes o eliminarlos.

#### Cómo crear un síntoma

1. En la barra de navegación, haz clic en **"Modulo Administración"**.
2. Asegúrate de que la pestaña **"Síntomas"** esté activa (es la primera pestaña por defecto).
3. Haz clic en el botón **"Agregar síntoma"**.
4. Se abrirá un formulario con los siguientes campos:
   - **ID:** identificador único del síntoma en formato Prolog. Debe comenzar con una letra minúscula y solo puede contener letras minúsculas, números y guiones bajos (ej. `sobrecarga_electrica`). Este campo es obligatorio.
   - **Descripción:** texto legible que describe el síntoma en lenguaje natural (ej. "El equipo se apaga por sobrecarga eléctrica"). Este campo es obligatorio.
   - **Fallas asociadas:** lista opcional de fallas que este síntoma puede indicar. Puedes seleccionarlas desde la lista disponible.
5. Completa los campos y haz clic en **"Guardar"**.
6. Si todo es correcto, el síntoma aparecerá en la tabla y verás una notificación de éxito. Si hay un error (ID duplicado, formato incorrecto, etc.), aparecerá una notificación roja con el mensaje correspondiente.

#### Cómo editar un síntoma

1. Ve a la pestaña **"Síntomas"** en el Módulo de Administración.
2. Localiza el síntoma que deseas modificar en la tabla.
3. Haz clic en el botón **"Editar"** de la fila correspondiente.
4. Se abrirá el formulario de edición con los datos actuales del síntoma precargados.
5. Modifica los campos que necesites (descripción y/o fallas asociadas). El ID no puede cambiarse.
6. Haz clic en **"Guardar"** para aplicar los cambios.

#### Cómo eliminar un síntoma

1. Ve a la pestaña **"Síntomas"** en el Módulo de Administración.
2. Localiza el síntoma que deseas eliminar.
3. Haz clic en el botón **"Eliminar"** (en rojo) de la fila correspondiente.
4. Confirma la acción en el modal de confirmación haciendo clic en **"Eliminar"**.
5. El síntoma desaparecerá de la tabla.

> **Nota:** Eliminar un síntoma lo remueve de la base de conocimiento. Los diagnósticos del historial que usaron ese síntoma no se ven afectados (el historial es independiente).

---

### 4.6 Cómo asociar o desasociar una falla a un síntoma

La relación entre un síntoma y una falla determina qué fallas puede indicar cada síntoma durante el diagnóstico. Puedes gestionar estas relaciones desde la pestaña de Síntomas.

#### Cómo asociar una falla a un síntoma

1. Ve a la pestaña **"Síntomas"** en el Módulo de Administración.
2. Haz clic en **"Editar"** sobre el síntoma al que deseas agregar una falla.
3. En el formulario de edición, agrega la falla deseada en el campo **"Fallas asociadas"** seleccionándola desde la lista.
4. Haz clic en **"Guardar"**. La falla quedará vinculada a ese síntoma.

#### Cómo desasociar una falla de un síntoma

1. Ve a la pestaña **"Síntomas"** en el Módulo de Administración.
2. Haz clic en **"Editar"** sobre el síntoma del que deseas quitar la falla.
3. En el formulario de edición, elimina la falla que deseas desasociar de la lista de "Fallas asociadas".
4. Haz clic en **"Guardar"**. La falla quedará desvinculada de ese síntoma.

---

### 4.7 Cómo gestionar fallas (crear, editar, eliminar)

Las fallas son los problemas o averías que el sistema puede diagnosticar a partir de los síntomas. Desde el Módulo de Administración puedes administrar el catálogo completo de fallas.

#### Cómo crear una falla

1. En el Módulo de Administración, haz clic en la pestaña **"Fallas"**.
2. Haz clic en el botón **"Agregar falla"**.
3. Completa el formulario:
   - **ID:** identificador único en formato Prolog (minúscula inicial, solo letras minúsculas, números y guion bajo; ej. `falla_lector_dvd`). Obligatorio.
   - **Descripción:** texto descriptivo de la falla en lenguaje natural (ej. "Falla en el lector de DVD/CD"). Obligatorio.
   - **Recomendaciones asociadas:** lista opcional de recomendaciones vinculadas a esta falla. Selecciónalas desde la lista disponible.
4. Haz clic en **"Guardar"**. La falla aparecerá en la tabla.

#### Cómo editar una falla

1. En la pestaña **"Fallas"**, localiza la falla que deseas modificar.
2. Haz clic en **"Editar"**.
3. Modifica la descripción y/o las recomendaciones asociadas en el formulario.
4. Haz clic en **"Guardar"** para aplicar los cambios.

#### Cómo eliminar una falla

1. En la pestaña **"Fallas"**, localiza la falla a eliminar.
2. Haz clic en **"Eliminar"** y confirma en el modal de confirmación.
3. La falla se eliminará del catálogo y también se desvinculará automáticamente de todos los síntomas que la referenciaban (eliminación en cascada).

> **Nota:** Si eliminas una falla que estaba siendo causada por varios síntomas, esos síntomas dejarán de apuntar a esa falla automáticamente. Verifica que los síntomas afectados estén correctamente configurados después de la eliminación.

---

### 4.8 Cómo asociar o desasociar una recomendación a una falla

Las recomendaciones son las acciones que el sistema sugiere para resolver una falla. Cada falla puede tener una o varias recomendaciones.

#### Cómo asociar una recomendación a una falla

1. Ve a la pestaña **"Fallas"** en el Módulo de Administración.
2. Haz clic en **"Editar"** sobre la falla a la que deseas agregar una recomendación.
3. En el formulario, agrega la recomendación en el campo **"Recomendaciones asociadas"** seleccionándola desde la lista.
4. Haz clic en **"Guardar"**.

#### Cómo desasociar una recomendación de una falla

1. Ve a la pestaña **"Fallas"** en el Módulo de Administración.
2. Haz clic en **"Editar"** sobre la falla de la que deseas quitar la recomendación.
3. Elimina la recomendación de la lista en el formulario de edición.
4. Haz clic en **"Guardar"**.

---

### 4.9 Cómo gestionar recomendaciones (crear, editar, eliminar)

Las recomendaciones son las acciones concretas que se le sugieren al usuario para resolver las fallas detectadas. Puedes administrar el catálogo completo desde el Módulo de Administración.

#### Cómo crear una recomendación

1. En el Módulo de Administración, haz clic en la pestaña **"Recomendaciones"**.
2. Haz clic en el botón **"Agregar recomendación"**.
3. Completa el formulario:
   - **ID:** identificador único en formato Prolog (ej. `rec_actualizar_bios`). Obligatorio.
   - **Descripción:** texto de la recomendación en lenguaje natural (ej. "Actualizar el BIOS/UEFI a la última versión disponible"). Obligatorio.
4. Haz clic en **"Guardar"**. La recomendación aparecerá en la tabla.

#### Cómo editar una recomendación

1. En la pestaña **"Recomendaciones"**, localiza la recomendación a modificar.
2. Haz clic en **"Editar"**.
3. Modifica la descripción en el formulario.
4. Haz clic en **"Guardar"**.

#### Cómo eliminar una recomendación

1. En la pestaña **"Recomendaciones"**, localiza la recomendación a eliminar.
2. Haz clic en **"Eliminar"** y confirma en el modal.
3. La recomendación se eliminará y también se desvinculará automáticamente de todas las fallas que la referenciaban.

> **Restricción importante:** La recomendación **"Llevar el equipo a servicio técnico especializado"** (`rec_servicio_tecnico`) está protegida y **no puede eliminarse**. Esta recomendación es necesaria para el diagnóstico de respaldo del sistema (cuando no se detecta ninguna falla concreta). Si intentas eliminarla, el sistema mostrará un mensaje de error indicando que la operación no está permitida.

---

### 4.10 Cómo activar o desactivar el bot de Telegram

Doctor Byte puede enviar automáticamente el resultado de cada diagnóstico a un chat de Telegram cuando el bot está activado.

**Pasos para activar el bot:**

1. En la barra de navegación, haz clic en **"Modulo Administración"**.
2. En la esquina superior derecha del encabezado de la página verás el botón del bot, que puede aparecer como:
   - **"Bot Desactivado"** (en gris/rojo): el bot está inactivo y no enviará diagnósticos a Telegram.
   - **"Bot Activado"** (en azul/verde): el bot está activo y enviará cada diagnóstico a Telegram automáticamente.
3. Haz clic en el botón para alternar el estado. El botón actualizará su texto y color para reflejar el nuevo estado.

> **Nota:** Si el backend no tiene configuradas las variables `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`, el botón mostrará "Bot no disponible" y no podrá activarse aunque se haga clic en él.

> **Funcionamiento:** Cuando el bot está activado, cada vez que se completa un diagnóstico (al presionar "Analizar"), el sistema envía automáticamente al chat de Telegram configurado un resumen con los síntomas ingresados, las fallas detectadas y las recomendaciones.

---

## 5. Verificar el estado del sistema

La página de **Inicio** incluye una tarjeta de "Estado del sistema" que se actualiza automáticamente cada vez que accedes a esa sección.

La tarjeta muestra:
- Un **indicador de color** (punto verde = operativo, punto rojo = error).
- El **título del estado**: "Sistema operativo" si todo funciona, "Sistema degradado" si hay algún componente con problemas, o "Sin conexión" si no se puede contactar el servidor.
- Una **descripción textual** explicando el estado.
- Dos **etiquetas de componentes**:
  - **✓ API** o **✕ API** — indica si el servidor backend responde correctamente.
  - **✓ Prolog** o **✕ Prolog** — indica si el motor de inferencia lógica está funcionando.

Si ves el estado **"Sin conexión"**, verifica que el servidor backend esté corriendo en `http://localhost:8000` antes de intentar realizar diagnósticos.

---

## 6. Mensajes del sistema

La aplicación muestra notificaciones emergentes en la esquina superior derecha para informar el resultado de las acciones. Estas notificaciones desaparecen automáticamente después de unos segundos.

| Color de la notificación | Significado |
|---|---|
| 🟢 **Verde** | La acción se completó con éxito (diagnóstico completado, registro guardado, eliminación exitosa). |
| 🔴 **Roja** | Ocurrió un error (el servidor no responde, el ID ya existe, datos inválidos, etc.). |
| 🔵 **Azul** | Información general del sistema. |

### Errores comunes y su solución

| Mensaje de error | Causa | Solución |
|---|---|---|
| "No se pudo conectar con el servidor." | El backend no está corriendo. | Inicia el servidor con `uvicorn main:app --reload` en la carpeta `backend/`. |
| "El ID debe iniciar con minúscula y contener solo letras, números o guion bajo." | El ID ingresado en el formulario no cumple el formato requerido. | Usa un ID válido como `mi_sintoma_nuevo`. No uses mayúsculas, espacios ni caracteres especiales. |
| "Ya existe un elemento con ese ID." | Estás intentando crear un registro con un ID que ya existe en la base de conocimiento. | Elige un ID diferente o edita el registro existente. |
| "El elemento no existe." | Se intenta acceder a un registro que fue eliminado o que nunca existió. | Recarga la lista o regresa a la sección correspondiente. |
| "No se encontró el elemento referenciado." | Se intenta asociar una falla o recomendación que no existe en el catálogo. | Crea primero la falla o recomendación antes de intentar asociarla. |
| "No se pudo cambiar el estado del bot." | El backend no puede conectarse a la API de Telegram (token inválido o sin internet). | Verifica las credenciales en el archivo `.env` del backend. |

---

## 7. Preguntas frecuentes

**¿Puedo seleccionar más de un síntoma en el diagnóstico?**
Sí. Puedes seleccionar todos los síntomas que apliquen. El motor de inferencia analizará el conjunto completo y buscará todas las fallas compatibles con esa combinación de síntomas.

**¿Qué pasa si no selecciono ningún síntoma y presiono "Analizar"?**
El botón "Analizar" permanece deshabilitado (en gris) mientras no haya al menos un síntoma seleccionado. No es posible enviar un diagnóstico vacío.

**¿El historial se guarda permanentemente?**
Sí. Los diagnósticos se persisten en un archivo en el servidor (`historial.json`) y permanecen disponibles entre sesiones. Solo se eliminan si el usuario los borra manualmente.

**¿Qué significa el ID en los formularios del Módulo de Administración?**
El ID es un identificador interno que usa el motor de inferencia Prolog para relacionar los elementos entre sí. Debe comenzar con una letra minúscula y solo puede contener letras minúsculas, números y guiones bajos (ejemplo: `falla_disco_duro`, `rec_limpieza_termica`). Una vez creado, el ID no puede modificarse.

**¿Por qué no puedo eliminar la recomendación "rec_servicio_tecnico"?**
Esta recomendación es usada por el sistema como respaldo cuando no puede determinar una falla específica. Eliminarla dejaría al motor de inferencia sin una respuesta válida para ese caso, por lo que está protegida.

**¿Se necesita conexión a internet para usar la aplicación?**
No, para las funciones principales (diagnóstico, historial, administración de la base de conocimiento). Todo el procesamiento ocurre localmente. Solo se requiere conexión a internet si el bot de Telegram está activado, ya que necesita comunicarse con los servidores de Telegram para enviar los mensajes.

**¿Qué ocurre si el motor Prolog no está disponible?**
La tarjeta de estado en la página Inicio mostrará "Sistema degradado" con la etiqueta "✕ Prolog". En ese caso, los diagnósticos no podrán procesarse correctamente. Verifica que SWI-Prolog esté instalado en el sistema y que el backend se haya iniciado correctamente.

**¿Puedo usar la aplicación desde otro dispositivo en la misma red?**
Sí, si el backend fue iniciado con `--host 0.0.0.0`. En ese caso, usa la IP local del servidor en lugar de `localhost` (ejemplo: `http://192.168.1.100:8000`). También deberás actualizar la constante `BASE_URL` en `frontend/js/api.js` con esa dirección.
