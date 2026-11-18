// Resolver reto de ordenamiento (CU-11).
// Colocar y retirar pasos de la línea solo ocurre en el navegador; el
// servidor únicamente revisa la secuencia completa cuando se presiona
// "Verificar".
(() => {
  const { pasos, total } = ReCode.reto.datos;
  const pozo = document.getElementById("pozo");
  const linea = document.getElementById("linea");
  const resultado = document.getElementById("resultado");
  const acciones = document.getElementById("acciones-ordenamiento");
  const dialogo = document.getElementById("dialogo-salir");

  const textoDe = {};
  pasos.forEach((paso) => {
    textoDe[paso.id] = paso.texto;
  });

  const secuencia = Array(total).fill(null); // id de paso en cada espacio
  let bloqueado = false;

  function colocados() {
    return new Set(secuencia.filter((id) => id !== null));
  }

  function dibujar(marcas = {}) {
    // Pozo: pasos aún no colocados, en el orden desordenado fijo.
    pozo.innerHTML = "";
    const usados = colocados();
    const libres = pasos.filter((paso) => !usados.has(paso.id));
    if (!libres.length) {
      const aviso = document.createElement("span");
      aviso.className = "pozo-vacio";
      aviso.textContent = "Todos los pasos están en la línea.";
      pozo.appendChild(aviso);
    } else {
      libres.forEach((paso) => {
        const boton = document.createElement("button");
        boton.type = "button";
        boton.className = "paso-boton";
        boton.textContent = paso.texto;
        boton.disabled = bloqueado;
        boton.addEventListener("click", () => colocar(paso.id));
        pozo.appendChild(boton);
      });
    }

    // Línea de secuencia.
    linea.innerHTML = "";
    secuencia.forEach((id, posicion) => {
      const espacio = document.createElement("li");
      espacio.className = "espacio" + (id !== null ? " lleno" : "") + (marcas[posicion] ? " " + marcas[posicion] : "");
      const numero = document.createElement("span");
      numero.className = "espacio-num";
      numero.textContent = posicion + 1;
      const cuerpo = document.createElement("div");
      cuerpo.className = "espacio-cuerpo";
      if (id === null) {
        const vacio = document.createElement("span");
        vacio.className = "vacio";
        vacio.textContent = "Espacio libre";
        cuerpo.appendChild(vacio);
      } else {
        const boton = document.createElement("button");
        boton.type = "button";
        boton.className = "paso-boton";
        boton.disabled = bloqueado;
        boton.innerHTML = `<span></span><span class="quitar">Retirar</span>`;
        boton.firstChild.textContent = textoDe[id];
        boton.addEventListener("click", () => retirar(posicion));
        cuerpo.appendChild(boton);
      }
      espacio.append(numero, cuerpo);
      linea.appendChild(espacio);
    });
  }

  function mensaje(html, error = false) {
    resultado.innerHTML = `<p class="mensaje ${error ? "error" : ""}">${html}</p>`;
  }

  function colocar(id) {
    if (bloqueado) return;
    const posicion = secuencia.indexOf(null);
    if (posicion === -1) return;
    secuencia[posicion] = id;
    dibujar();
    mensaje(`Paso colocado en el espacio ${posicion + 1}. Cuando estés conforme, presiona Verificar.`);
  }

  function retirar(posicion) {
    if (bloqueado) return;
    secuencia[posicion] = null;
    dibujar();
    mensaje(`Retiraste el paso del espacio ${posicion + 1}.`);
  }

  async function verificar() {
    if (bloqueado) return;
    let respuesta;
    try {
      respuesta = await ReCode.postJSON(ReCode.reto.revisarUrl, { secuencia });
    } catch (error) {
      mensaje(error.message, true);
      return;
    }

    if (respuesta.vacios && respuesta.vacios.length) {
      const marcas = {};
      respuesta.vacios.forEach((posicion) => {
        marcas[posicion] = "falta";
      });
      dibujar(marcas);
      const lista = respuesta.vacios.map((posicion) => posicion + 1).join(", ");
      mensaje(
        respuesta.vacios.length === 1 ? `Falta llenar el espacio ${lista}.` : `Faltan llenar los espacios ${lista}.`,
        true,
      );
      return;
    }
    if (!respuesta.correcto) {
      dibujar();
      mensaje("Al menos un paso no está en el orden correcto. Corrige y vuelve a verificar.", true);
      return;
    }

    // Éxito.
    bloqueado = true;
    const marcas = {};
    secuencia.forEach((_, posicion) => {
      marcas[posicion] = "correcto";
    });
    dibujar(marcas);
    const saldo = document.getElementById("bitcoins-alumno");
    if (saldo) saldo.textContent = respuesta.bitcoins_total;
    const premio = respuesta.ya_otorgado
      ? "Este reto ya estaba completado, así que no se otorgan bitcoins de nuevo."
      : `Ganaste <strong>₿ ${respuesta.bitcoins_otorgados}</strong>.`;
    acciones.hidden = true;
    resultado.innerHTML = `
      <p class="mensaje"><strong>¡Algoritmo restaurado!</strong> ${premio}</p>
      <a class="boton" href="${ReCode.reto.volverUrl}">Volver a los retos</a>`;
  }

  // --- FE-1: salir / rendirse con confirmación --------------------------

  function pedirSalida(evento) {
    if (evento) evento.preventDefault();
    if (bloqueado) return;
    if (typeof dialogo.showModal === "function") {
      dialogo.showModal();
    } else if (window.confirm("Se perderá el progreso de este reto y no obtendrás bitcoins. ¿Salir?")) {
      cerrarReto();
    }
  }

  // FE-1.4: cierra el reto sin guardar nada y muestra el botón para que el
  // alumno regrese manualmente (sin redirección automática, R8).
  function cerrarReto() {
    if (dialogo.open) dialogo.close();
    bloqueado = true;
    secuencia.fill(null);
    dibujar();
    acciones.hidden = true;
    resultado.innerHTML = `
      <p class="mensaje">Saliste del reto. No se guardó el progreso ni se otorgaron bitcoins.</p>
      <a class="boton" href="${ReCode.reto.volverUrl}">Regresar a la selección de retos</a>`;
  }

  document.getElementById("btn-salir").addEventListener("click", pedirSalida);
  const flecha = document.querySelector(".volver");
  if (flecha) {
    flecha.addEventListener("click", (evento) => {
      if (colocados().size > 0 && !bloqueado) pedirSalida(evento);
    });
  }
  document.getElementById("btn-cancelar-salida").addEventListener("click", () => dialogo.close());
  document.getElementById("btn-confirmar-salida").addEventListener("click", cerrarReto);
  document.getElementById("btn-verificar").addEventListener("click", verificar);

  dibujar();
})();
