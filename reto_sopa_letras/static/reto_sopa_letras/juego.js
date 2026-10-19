/**
 * Sopa de letras (CU-10).
 * Dibuja la sopa y la lista de conceptos que manda Django. El alumno marca una
 * palabra arrastrando o con clic en la primera y la última letra; cada selección
 * se manda al servidor, que es quien dice si es correcta.
 */
(() => {
  'use strict';

  const { sopa, pasos } = ReCode.reto.datos;

  const tablero = document.getElementById('sopa');
  const lista = document.getElementById('conceptos');
  const resultado = document.getElementById('resultado');
  const victoria = document.getElementById('victoria');
  const textoVictoria = document.getElementById('victoria-texto');
  const botonSalir = document.getElementById('btn-salir');
  const dialogo = document.getElementById('dialogo-salir');
  const MENSAJE_SALIR =
    'Se perderá el progreso de este reto y no obtendrás bitcoins. ¿Salir?';

  const celdas = [];
  const itemsConcepto = [];
  let inicio = null;
  let arrastrando = false;
  let bloqueado = false;
  let terminado = false;

  /** Crea un botón por cada letra de la sopa. */
  function crearTablero() {
    tablero.style.setProperty('--columnas', sopa[0].length);
    sopa.forEach((texto, fila) => {
      const filaCeldas = [];
      Array.from(texto).forEach((letra, columna) => {
        const celda = document.createElement('button');
        celda.type = 'button';
        celda.textContent = letra;
        celda.dataset.fila = fila;
        celda.dataset.columna = columna;
        celda.setAttribute(
          'aria-label',
          `Letra ${letra}, fila ${fila + 1}, columna ${columna + 1}`,
        );
        tablero.appendChild(celda);
        filaCeldas.push(celda);
      });
      celdas.push(filaCeldas);
    });
  }

  /** Muestra la lista de conceptos que hay que encontrar. */
  function crearLista() {
    pasos.forEach((paso) => {
      const item = document.createElement('li');
      const palabra = document.createElement('strong');
      const definicion = document.createElement('span');
      palabra.textContent = paso.palabra;
      definicion.textContent = ` ${paso.definicion}`;
      item.append(palabra, definicion);
      lista.appendChild(item);
      itemsConcepto.push(item);
    });
  }

  /** Devuelve {fila, columna} de la letra que contiene el elemento, o null. */
  function posicionDe(elemento) {
    const celda =
      elemento && elemento.closest ? elemento.closest('#sopa button') : null;
    if (!celda) {
      return null;
    }
    return { fila: Number(celda.dataset.fila), columna: Number(celda.dataset.columna) };
  }

  /** Lista las posiciones entre dos letras; null si no van en línea recta. */
  function calcularLinea(desde, hasta) {
    const saltoFila = Math.abs(hasta.fila - desde.fila);
    const saltoColumna = Math.abs(hasta.columna - desde.columna);
    const esDiagonal = saltoFila === saltoColumna;
    if (saltoFila !== 0 && saltoColumna !== 0 && !esDiagonal) {
      return null;
    }
    const pasoFila = Math.sign(hasta.fila - desde.fila);
    const pasoColumna = Math.sign(hasta.columna - desde.columna);
    const largo =
      Math.max(
        Math.abs(hasta.fila - desde.fila),
        Math.abs(hasta.columna - desde.columna),
      ) + 1;
    return Array.from({ length: largo }, (_, i) => ({
      fila: desde.fila + pasoFila * i,
      columna: desde.columna + pasoColumna * i,
    }));
  }

  /** Encierra en un círculo las letras que se están seleccionando. */
  function mostrarSeleccion(posiciones) {
    tablero.querySelectorAll('.seleccion').forEach((celda) => {
      celda.classList.remove('seleccion');
    });
    posiciones.forEach(({ fila, columna }) => {
      celdas[fila][columna].classList.add('seleccion');
    });
  }

  /** Quita la selección temporal. */
  function limpiarSeleccion() {
    inicio = null;
    arrastrando = false;
    mostrarSeleccion([]);
  }

  /** Escribe un mensaje bajo la sopa. */
  function mostrarMensaje(texto, esError) {
    const mensaje = document.createElement('p');
    mensaje.className = esError ? 'mensaje error' : 'mensaje';
    mensaje.textContent = texto;
    resultado.textContent = '';
    resultado.appendChild(mensaje);
  }

  /** Deja marcadas las letras y tacha el concepto encontrado. */
  function marcarEncontrada(linea, indice) {
    linea.forEach(({ fila, columna }) => {
      celdas[fila][columna].classList.add('encontrada');
    });
    if (itemsConcepto[indice]) {
      itemsConcepto[indice].classList.add('hecha');
    }
  }

  /** Muestra la pantalla de victoria con el botón Continuar. */
  function mostrarVictoria(respuesta) {
    terminado = true;
    resultado.textContent = '';
    textoVictoria.textContent = respuesta.bitcoins_otorgados
      ? `¡Felicidades! +${respuesta.bitcoins_otorgados} bitcoins`
      : '¡Felicidades! Ya habías recibido los bitcoins de este reto.';
    victoria.hidden = false;
    botonSalir.hidden = true;
  }

  /** Manda la selección al servidor y muestra lo que conteste. */
  async function terminarEn(fin) {
    const linea = calcularLinea(inicio, fin);
    arrastrando = false;
    if (!linea) {
      limpiarSeleccion();
      mostrarMensaje(
        'Selecciona en línea recta: horizontal, vertical o diagonal.',
        true,
      );
      return;
    }
    mostrarSeleccion(linea);
    bloqueado = true;
    const palabra = linea.map(({ fila, columna }) => sopa[fila][columna]).join('');
    try {
      const respuesta = await ReCode.enviarRespuesta(null, palabra);
      if (respuesta.correcto) {
        marcarEncontrada(linea, respuesta.paso);
      }
      if (respuesta.completado) {
        mostrarVictoria(respuesta);
      }
    } catch {
      mostrarMensaje('No se pudo revisar la palabra. Intenta de nuevo.', true);
    } finally {
      limpiarSeleccion();
      bloqueado = false;
    }
  }

  /** Empieza la selección con el dedo o el ratón. */
  function alPresionar(evento) {
    if (bloqueado || terminado) {
      return;
    }
    const celda = posicionDe(evento.target);
    if (!celda) {
      return;
    }
    evento.preventDefault();
    if (inicio) {
      if (inicio.fila === celda.fila && inicio.columna === celda.columna) {
        limpiarSeleccion();
      } else {
        terminarEn(celda);
      }
      return;
    }
    inicio = celda;
    arrastrando = true;
    mostrarSeleccion([celda]);
  }

  /** Actualiza el círculo mientras se arrastra. */
  function alMover(evento) {
    if (!arrastrando) {
      return;
    }
    const celda = posicionDe(document.elementFromPoint(evento.clientX, evento.clientY));
    if (celda) {
      mostrarSeleccion(calcularLinea(inicio, celda) || [inicio]);
    }
  }

  /** Termina el arrastre; si se soltó en la misma letra, espera el segundo clic. */
  function alSoltar(evento) {
    if (!arrastrando) {
      return;
    }
    arrastrando = false;
    const celda = posicionDe(document.elementFromPoint(evento.clientX, evento.clientY));
    if (!celda) {
      limpiarSeleccion();
    } else if (celda.fila !== inicio.fila || celda.columna !== inicio.columna) {
      terminarEn(celda);
    }
  }

  /** Permite jugar con teclado: Enter o espacio en la primera y la última letra. */
  function alActivarConTeclado(evento) {
    if (evento.detail !== 0 || bloqueado || terminado) {
      return;
    }
    const celda = posicionDe(evento.target);
    if (!celda) {
      return;
    }
    if (!inicio) {
      inicio = celda;
      mostrarSeleccion([celda]);
    } else if (inicio.fila === celda.fila && inicio.columna === celda.columna) {
      limpiarSeleccion();
    } else {
      terminarEn(celda);
    }
  }

  /** Pide confirmación antes de salir (FE-1). */
  function pedirSalida(evento) {
    if (terminado) {
      return;
    }
    evento.preventDefault();
    if (typeof dialogo.showModal === 'function') {
      dialogo.showModal();
    } else if (window.confirm(MENSAJE_SALIR)) {
      window.location.href = ReCode.reto.volverUrl;
    }
  }

  crearTablero();
  crearLista();

  tablero.addEventListener('pointerdown', alPresionar);
  tablero.addEventListener('pointermove', alMover);
  tablero.addEventListener('click', alActivarConTeclado);
  document.addEventListener('pointerup', alSoltar);
  document.addEventListener('pointercancel', limpiarSeleccion);
  document.addEventListener('keydown', (evento) => {
    if (evento.key === 'Escape' && !bloqueado) {
      limpiarSeleccion();
    }
  });

  botonSalir.addEventListener('click', pedirSalida);
  const flecha = document.querySelector('.btn-regresar');
  if (flecha) {
    flecha.addEventListener('click', pedirSalida);
  }
  document.getElementById('btn-cancelar-salida').addEventListener('click', () => {
    dialogo.close();
  });
  document.getElementById('btn-confirmar-salida').addEventListener('click', () => {
    window.location.href = ReCode.reto.volverUrl;
  });
})();
