// script.js - Lógica del frontend

// La SPA se sirve desde el mismo Flask, asi que las rutas son relativas.
const API = "";

// Helper: crea (POST) o actualiza (PUT) un recurso y avisa si el backend lo rechaza.
async function enviarRecurso(base, id, datos) {
  const url = id ? `${API}/${base}/${id}` : `${API}/${base}`;
  const respuesta = await fetch(url, {
    method: id ? "PUT" : "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  const data = await respuesta.json().catch(() => ({}));
  if (!respuesta.ok) alert("Error: " + (data.error || "no se pudo guardar"));
  return respuesta.ok;
}

// Helper: elimina un recurso y avisa si el backend lo rechaza (ej. clave foranea).
async function borrarRecurso(base, id) {
  const respuesta = await fetch(`${API}/${base}/${id}`, { method: "DELETE" });
  const data = await respuesta.json().catch(() => ({}));
  if (!respuesta.ok) alert("Error: " + (data.error || "no se pudo eliminar"));
  return respuesta.ok;
}


// Helper: trae una lista del backend SIN romper si la respuesta no es un array.
// Si algo falla, avisa, lo loguea en consola y devuelve [] para no frenar la UI.
async function obtenerJSON(url) {
  try {
    const r = await fetch(`${API}${url}`);
    const data = await r.json().catch(() => null);
    if (!r.ok || !Array.isArray(data)) {
      console.error("Respuesta inesperada de", url, "->", r.status, data);
      alert(`No se pudieron cargar los datos de ${url} (revisá la consola).`);
      return [];
    }
    return data;
  } catch (e) {
    console.error("Falló el fetch de", url, e);
    alert(`No se pudo conectar con ${url}. ¿El servidor está en el puerto 5000?`);
    return [];
  }
}

// ============================================================
// NAVEGACIÓN
// ============================================================

function mostrarSeccion(nombre) {
  // Ocultar todas las secciones
  document.querySelectorAll(".seccion").forEach(s => s.classList.remove("activa"));
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));

  // Mostrar la sección elegida
  document.getElementById("seccion-" + nombre).classList.add("activa");

  // Marcar el nav item como activo
  event.currentTarget.classList.add("active");

  // Cargar los datos de esa sección
  if (nombre === "inicio")         cargarInicio();
  if (nombre === "estudiantes")    cargarEstudiantes();
  if (nombre === "actividades")    cargarActividades();
  if (nombre === "inscripciones")  cargarInscripciones();
  if (nombre === "disciplinas")    cargarDisciplinas();
  if (nombre === "espacios")       cargarEspacios();
  if (nombre === "reportes")       cargarTodosLosReportes();
}

// ============================================================
// INICIO - ESTADÍSTICAS
// ============================================================

async function cargarInicio() {
  const estudiantes   = await fetch(`${API}/estudiantes`).then(r => r.json());
  const actividades   = await fetch(`${API}/actividades`).then(r => r.json());
  const inscripciones = await fetch(`${API}/inscripciones`).then(r => r.json());

  document.getElementById("stat-estudiantes").textContent = estudiantes.length;
  document.getElementById("stat-actividades").textContent = actividades.filter(a => a.estado === "abierta").length;
  document.getElementById("stat-inscripciones").textContent = inscripciones.filter(i => i.estado === "confirmada").length;
}

// ============================================================
// ESTUDIANTES
// ============================================================

async function cargarEstudiantes() {
  const datos = await fetch(`${API}/estudiantes`).then(r => r.json());
  const tbody = document.getElementById("tabla-estudiantes");
  tbody.innerHTML = "";

  datos.forEach(e => {
    tbody.innerHTML += `
      <tr>
        <td>${e.documento}</td>
        <td>${e.nombre}</td>
        <td>${e.apellido}</td>
        <td>${e.email}</td>
        <td>${e.carrera}</td>
        <td>${e.facultad}</td>
        <td>
          <div class="acciones">
            <button class="btn-icon" onclick="editarEstudiante(${e.id_estudiante})"><i class="ti ti-edit"></i></button>
            <button class="btn-icon" onclick="borrarEstudiante(${e.id_estudiante})"><i class="ti ti-trash"></i></button>
          </div>
        </td>
      </tr>
    `;
  });
}

async function abrirModal(id) {
  // Si es el modal de estudiante, cargar las carreras
  if (id === "modal-estudiante") {
    await cargarOpcionesCarreras();
    limpiarFormEstudiante();
  }
  if (id === "modal-actividad") {
    await cargarOpcionesDisciplinas();
    await cargarOpcionesEspacios();
    limpiarFormActividad();
  }
  if (id === "modal-inscripcion") {
    await cargarOpcionesEstudiantes();
    await cargarOpcionesActividades();
  }
  if (id === "modal-asistencia") {
    await cargarOpcionesInscripciones();
  }
  if (id === "modal-disciplina") {
    limpiarFormDisciplina();
  }
  if (id === "modal-espacio") {
    limpiarFormEspacio();
  }

  document.getElementById(id).classList.add("abierto");
}

function cerrarModal(id) {
  document.getElementById(id).classList.remove("abierto");
}

function limpiarFormEstudiante() {
  document.getElementById("est-id").value = "";
  document.getElementById("est-documento").value = "";
  document.getElementById("est-nombre").value = "";
  document.getElementById("est-apellido").value = "";
  document.getElementById("est-email").value = "";
  document.getElementById("titulo-modal-estudiante").textContent = "Nuevo estudiante";
}

async function cargarOpcionesCarreras() {
  const carreras = await fetch(`${API}/carreras`).then(r => r.json());
  const select = document.getElementById("est-carrera");
  select.innerHTML = "";
  carreras.forEach(c => {
    select.innerHTML += `<option value="${c.id_carrera}">${c.nombre} — ${c.facultad}</option>`;
  });
}

async function guardarEstudiante() {
  const id = document.getElementById("est-id").value;
  const datos = {
    documento:  document.getElementById("est-documento").value,
    nombre:     document.getElementById("est-nombre").value,
    apellido:   document.getElementById("est-apellido").value,
    email:      document.getElementById("est-email").value,
    id_carrera: document.getElementById("est-carrera").value,
  };

  if (!datos.documento || !datos.nombre || !datos.apellido || !datos.email) {
    alert("Por favor completá todos los campos.");
    return;
  }

  const ok = await enviarRecurso("estudiantes", id, datos);
  if (!ok) return;

  cerrarModal("modal-estudiante");
  cargarEstudiantes();
}

async function editarEstudiante(id) {
  await cargarOpcionesCarreras();
  const datos = await fetch(`${API}/estudiantes`).then(r => r.json());
  const est = datos.find(e => e.id_estudiante === id);

  document.getElementById("est-id").value       = est.id_estudiante;
  document.getElementById("est-documento").value = est.documento;
  document.getElementById("est-nombre").value    = est.nombre;
  document.getElementById("est-apellido").value  = est.apellido;
  document.getElementById("est-email").value     = est.email;
  document.getElementById("titulo-modal-estudiante").textContent = "Editar estudiante";

  document.getElementById("modal-estudiante").classList.add("abierto");
}

async function borrarEstudiante(id) {
  if (!confirm("¿Seguro que querés eliminar este estudiante?")) return;
  if (await borrarRecurso("estudiantes", id)) cargarEstudiantes();
}

// ============================================================
// ACTIVIDADES
// ============================================================

async function cargarActividades() {
  const datos = await fetch(`${API}/actividades`).then(r => r.json());
  const tbody = document.getElementById("tabla-actividades");
  tbody.innerHTML = "";

  datos.forEach(a => {
    const porcentaje = 0; // se podría calcular
    tbody.innerHTML += `
      <tr>
        <td>${a.nombre}</td>
        <td>${a.disciplina}</td>
        <td>${a.espacio}</td>
        <td>${capitalizar(a.dia_semana)}</td>
        <td>${a.horario}</td>
        <td><span class="cupo-text">${a.cupo_maximo}</span></td>
        <td><span class="badge badge-${a.estado}">${capitalizar(a.estado)}</span></td>
        <td>
          <div class="acciones">
            <button class="btn-icon" onclick="editarActividad(${a.id_actividad})"><i class="ti ti-edit"></i></button>
            <button class="btn-icon" onclick="borrarActividad(${a.id_actividad})"><i class="ti ti-trash"></i></button>
          </div>
        </td>
      </tr>
    `;
  });
}

async function cargarOpcionesDisciplinas() {
  const disciplinas = await obtenerJSON("/disciplinas");
  const select = document.getElementById("act-disciplina");
  select.innerHTML = "";
  disciplinas.forEach(d => {
    select.innerHTML += `<option value="${d.id_disciplina}">${d.nombre}</option>`;
  });
}

async function cargarOpcionesEspacios() {
  const espacios = await obtenerJSON("/espacios");
  const select = document.getElementById("act-espacio");
  select.innerHTML = "";
  espacios.forEach(e => {
    select.innerHTML += `<option value="${e.id_espacio}">${e.nombre}</option>`;
  });
}

function limpiarFormActividad() {
  document.getElementById("act-id").value = "";
  document.getElementById("act-nombre").value = "";
  document.getElementById("act-cupo").value = "";
  document.getElementById("act-horario").value = "";
  document.getElementById("titulo-modal-actividad").textContent = "Nueva actividad";
}

async function guardarActividad() {
  const id = document.getElementById("act-id").value;
  const datos = {
    nombre:        document.getElementById("act-nombre").value,
    id_disciplina: document.getElementById("act-disciplina").value,
    id_espacio:    document.getElementById("act-espacio").value,
    cupo_maximo:   document.getElementById("act-cupo").value,
    dia_semana:    document.getElementById("act-dia").value,
    horario:       document.getElementById("act-horario").value,
    estado:        document.getElementById("act-estado").value,
  };

  if (!datos.nombre || !datos.cupo_maximo || !datos.horario) {
    alert("Por favor completá todos los campos.");
    return;
  }

  const ok = await enviarRecurso("actividades", id, datos);
  if (!ok) return;

  cerrarModal("modal-actividad");
  cargarActividades();
}

async function editarActividad(id) {
  await cargarOpcionesDisciplinas();
  await cargarOpcionesEspacios();
  const datos = await obtenerJSON("/actividades");
  const act = datos.find(a => a.id_actividad === id);

  document.getElementById("act-id").value      = act.id_actividad;
  document.getElementById("act-nombre").value   = act.nombre;
  document.getElementById("act-cupo").value     = act.cupo_maximo;
  document.getElementById("act-dia").value      = act.dia_semana;
  document.getElementById("act-horario").value  = act.horario;
  document.getElementById("act-estado").value   = act.estado;
  document.getElementById("act-disciplina").value = act.id_disciplina;
  document.getElementById("act-espacio").value    = act.id_espacio;
  document.getElementById("titulo-modal-actividad").textContent = "Editar actividad";

  document.getElementById("modal-actividad").classList.add("abierto");
}

async function borrarActividad(id) {
  if (!confirm("¿Seguro que querés eliminar esta actividad?")) return;
  if (await borrarRecurso("actividades", id)) cargarActividades();
}

// ============================================================
// INSCRIPCIONES
// ============================================================

async function cargarInscripciones() {
  const datos = await fetch(`${API}/inscripciones`).then(r => r.json());
  const tbody = document.getElementById("tabla-inscripciones");
  tbody.innerHTML = "";

  datos.forEach(i => {
    tbody.innerHTML += `
      <tr>
        <td>${i.nombre} ${i.apellido}</td>
        <td>${i.actividad}</td>
        <td>${i.fecha_inscripcion ? i.fecha_inscripcion.substring(0, 10) : "—"}</td>
        <td><span class="badge badge-${i.estado}">${capitalizar(i.estado)}</span></td>
        <td>${i.posicion_espera || "—"}</td>
        <td>
          <div class="acciones">
            <button class="btn-icon" onclick="cancelarInscripcion(${i.id_inscripcion})"><i class="ti ti-x"></i></button>
          </div>
        </td>
      </tr>
    `;
  });
}

async function cargarOpcionesEstudiantes() {
  const estudiantes = await fetch(`${API}/estudiantes`).then(r => r.json());
  const select = document.getElementById("ins-estudiante");
  select.innerHTML = "";
  estudiantes.forEach(e => {
    select.innerHTML += `<option value="${e.id_estudiante}">${e.nombre} ${e.apellido} — ${e.documento}</option>`;
  });
}

async function cargarOpcionesActividades() {
  const actividades = await fetch(`${API}/actividades`).then(r => r.json());
  const select = document.getElementById("ins-actividad");
  select.innerHTML = "";
  actividades.filter(a => a.estado === "abierta").forEach(a => {
    select.innerHTML += `<option value="${a.id_actividad}">${a.nombre}</option>`;
  });
}

async function guardarInscripcion() {
  const datos = {
    id_estudiante: document.getElementById("ins-estudiante").value,
    id_actividad:  document.getElementById("ins-actividad").value,
  };

  const respuesta = await fetch(`${API}/inscripciones`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos)
  });

  const resultado = await respuesta.json();

  if (!respuesta.ok) {
    alert("Error: " + resultado.error);
    return;
  }

  alert(resultado.mensaje);
  cerrarModal("modal-inscripcion");
  cargarInscripciones();
}

async function cancelarInscripcion(id) {
  if (!confirm("¿Seguro que querés cancelar esta inscripción?")) return;
  if (await borrarRecurso("inscripciones", id)) cargarInscripciones();
}

// ============================================================
// ASISTENCIAS
// ============================================================

async function cargarOpcionesInscripciones() {
  const inscripciones = await fetch(`${API}/inscripciones`).then(r => r.json());
  const select = document.getElementById("asi-inscripcion");
  select.innerHTML = "";
  inscripciones.filter(i => i.estado === "confirmada").forEach(i => {
    select.innerHTML += `<option value="${i.id_inscripcion}">${i.nombre} ${i.apellido} — ${i.actividad}</option>`;
  });

  // Poner la fecha de hoy por defecto
  document.getElementById("asi-fecha").value = new Date().toISOString().substring(0, 10);
}

async function guardarAsistencia() {
  const datos = {
    id_inscripcion: document.getElementById("asi-inscripcion").value,
    fecha:          document.getElementById("asi-fecha").value,
    presente:       document.getElementById("asi-presente").value === "1",
  };

  const respuesta = await fetch(`${API}/asistencias`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos)
  });

  const resultado = await respuesta.json();

  if (!respuesta.ok) {
    alert("Error: " + resultado.error);
    return;
  }

  alert(resultado.mensaje);
  cerrarModal("modal-asistencia");
}

// ============================================================
// DISCIPLINAS
// ============================================================

async function cargarDisciplinas() {
  const datos = await obtenerJSON("/disciplinas");
  const tbody = document.getElementById("tabla-disciplinas");
  tbody.innerHTML = "";

  datos.forEach(d => {
    tbody.innerHTML += `
      <tr>
        <td>${d.nombre}</td>
        <td>
          <div class="acciones">
            <button class="btn-icon" onclick="editarDisciplina(${d.id_disciplina}, '${d.nombre}')"><i class="ti ti-edit"></i></button>
            <button class="btn-icon" onclick="borrarDisciplina(${d.id_disciplina})"><i class="ti ti-trash"></i></button>
          </div>
        </td>
      </tr>
    `;
  });
}

function limpiarFormDisciplina() {
  document.getElementById("dis-id").value = "";
  document.getElementById("dis-nombre").value = "";
  document.getElementById("titulo-modal-disciplina").textContent = "Nueva disciplina";
}

async function guardarDisciplina() {
  const id = document.getElementById("dis-id").value;
  const datos = { nombre: document.getElementById("dis-nombre").value };

  if (!datos.nombre) { alert("Ingresá un nombre."); return; }

  const ok = await enviarRecurso("disciplinas", id, datos);
  if (!ok) return;

  cerrarModal("modal-disciplina");
  cargarDisciplinas();
}

function editarDisciplina(id, nombre) {
  document.getElementById("dis-id").value    = id;
  document.getElementById("dis-nombre").value = nombre;
  document.getElementById("titulo-modal-disciplina").textContent = "Editar disciplina";
  document.getElementById("modal-disciplina").classList.add("abierto");
}

async function borrarDisciplina(id) {
  if (!confirm("¿Seguro que querés eliminar esta disciplina?")) return;
  if (await borrarRecurso("disciplinas", id)) cargarDisciplinas();
}

// ============================================================
// ESPACIOS
// ============================================================

async function cargarEspacios() {
  const datos = await fetch(`${API}/espacios`).then(r => r.json());
  const tbody = document.getElementById("tabla-espacios");
  tbody.innerHTML = "";

  datos.forEach(e => {
    tbody.innerHTML += `
      <tr>
        <td>${e.nombre}</td>
        <td>${e.ubicacion}</td>
        <td>
          <div class="acciones">
            <button class="btn-icon" onclick="editarEspacio(${e.id_espacio}, '${e.nombre}', '${e.ubicacion}')"><i class="ti ti-edit"></i></button>
            <button class="btn-icon" onclick="borrarEspacio(${e.id_espacio})"><i class="ti ti-trash"></i></button>
          </div>
        </td>
      </tr>
    `;
  });
}

function limpiarFormEspacio() {
  document.getElementById("esp-id").value = "";
  document.getElementById("esp-nombre").value = "";
  document.getElementById("esp-ubicacion").value = "";
  document.getElementById("titulo-modal-espacio").textContent = "Nuevo espacio";
}

async function guardarEspacio() {
  const id = document.getElementById("esp-id").value;
  const datos = {
    nombre:    document.getElementById("esp-nombre").value,
    ubicacion: document.getElementById("esp-ubicacion").value,
  };

  if (!datos.nombre || !datos.ubicacion) { alert("Completá todos los campos."); return; }

  const ok = await enviarRecurso("espacios", id, datos);
  if (!ok) return;

  cerrarModal("modal-espacio");
  cargarEspacios();
}

function editarEspacio(id, nombre, ubicacion) {
  document.getElementById("esp-id").value        = id;
  document.getElementById("esp-nombre").value    = nombre;
  document.getElementById("esp-ubicacion").value = ubicacion;
  document.getElementById("titulo-modal-espacio").textContent = "Editar espacio";
  document.getElementById("modal-espacio").classList.add("abierto");
}

async function borrarEspacio(id) {
  if (!confirm("¿Seguro que querés eliminar este espacio?")) return;
  if (await borrarRecurso("espacios", id)) cargarEspacios();
}

// ============================================================
// REPORTES
// ============================================================

async function cargarTodosLosReportes() {
  await cargarReporte("inscriptos-por-actividad");
  await cargarReporte("cupos-disponibles");
  await cargarReporte("inscriptos-por-disciplina");
  await cargarReporte("inscriptos-por-carrera");
  await cargarReporte("ocupacion");
  await cargarReporte("asistencia");
  await cargarReporte("inasistencias");
}

async function cargarReporte(nombre) {
  const datos = await fetch(`${API}/reportes/${nombre}`).then(r => r.json());
  const contenedor = document.getElementById("reporte-" + nombre);
  contenedor.innerHTML = "";

  if (datos.length === 0) {
    contenedor.innerHTML = `<p style="color:#9aaab8; font-size:11px;">Sin datos aún</p>`;
    return;
  }

  // Construir tabla dinámica con las columnas que devuelva la query
  const columnas = Object.keys(datos[0]);
  let html = "<table><thead><tr>";
  columnas.forEach(col => { html += `<th>${col.replace(/_/g, " ")}</th>`; });
  html += "</tr></thead><tbody>";

  datos.forEach(fila => {
    html += "<tr>";
    columnas.forEach(col => { html += `<td>${fila[col] ?? "—"}</td>`; });
    html += "</tr>";
  });

  html += "</tbody></table>";
  contenedor.innerHTML = html;
}

// ============================================================
// UTILIDADES
// ============================================================

function capitalizar(texto) {
  if (!texto) return "";
  return texto.charAt(0).toUpperCase() + texto.slice(1);
}

// ============================================================
// ARRANQUE
// ============================================================

cargarInicio();