// Derrotar al Kernel (CU-13)
// Pantallas de la batalla final. El navegador solo dibuja y manda respuestas:
// las correctas, el daño al Kernel y el tiempo límite se validan en Django.
(function (ReCode) {
  'use strict';

  const raiz = document.getElementById('batalla-final');
  const urls = {
    iniciar: raiz.dataset.urlIniciar,
    siguiente: raiz.dataset.urlSiguiente,
    responder: raiz.dataset.urlResponder,
    tiempo: raiz.dataset.urlTiempo,
    pausa: raiz.dataset.urlPausa,
    abandonar: raiz.dataset.urlAbandonar,
  };

  const PANTALLAS = ['intro', 'batalla', 'victoria', 'cierre', 'abandono'];
  const DURACION_JUMPSCARE = 2800; // ms entre impacto y bloqueo, y después se oculta
  const FASE_BLOQUEO = 900;

  const $ = (id) => document.getElementById(id);

  const estado = {
    reto: null,
    resta: 0,
    total: 0,
    pausado: false,
    resuelto: true,
    temporizador: null,
    respuesta: null, // lo que el alumno lleva elegido para el reto actual
  };

  // --- Utilidades ------------------------------------------------------------

  function mostrar(nombre) {
    PANTALLAS.forEach((p) => {
      $('pantalla-' + p).hidden = p !== nombre;
    });
  }

  function crear(etiqueta, clase, texto) {
    const el = document.createElement(etiqueta);
    if (clase) el.className = clase;
    if (texto !== undefined) el.textContent = texto;
    return el;
  }

  function crearBoton(clase, texto, alHacerClic) {
    const boton = crear('button', clase, texto);
    boton.type = 'button';
    boton.addEventListener('click', alHacerClic);
    return boton;
  }

  // --- Kernel (SVG construido con DOM, sin innerHTML) -------------------------

  const SVG_NS = 'http://www.w3.org/2000/svg';
  const KERNEL = [
    ['rect', { x: 40, y: 40, width: 120, height: 120, rx: 14, fill: '#10151e', stroke: '#ff3b4e', 'stroke-width': 3 }],
    ['path', { d: 'M60 40v-18M85 40v-18M115 40v-18M140 40v-18M60 160v18M85 160v18M115 160v18M140 160v18M40 60h-18M40 85h-18M40 115h-18M40 140h-18M160 60h18M160 85h18M160 115h18M160 140h18', stroke: '#ff3b4e', 'stroke-width': 3 }],
    ['rect', { x: 58, y: 58, width: 84, height: 84, rx: 8, fill: '#1a0b10', stroke: '#5a1a24' }],
    ['circle', { cx: 100, cy: 92, r: 22, fill: '#ff3b4e', class: 'ojo' }],
    ['circle', { cx: 100, cy: 92, r: 9, fill: '#12060a' }],
    ['circle', { cx: 104, cy: 88, r: 3, fill: '#fff' }],
    ['path', { d: 'M72 126h56', stroke: '#ff3b4e', 'stroke-width': 3, 'stroke-dasharray': '6 5' }],
  ];

  function dibujarKernel(svg) {
    KERNEL.forEach(([etiqueta, atributos]) => {
      const el = document.createElementNS(SVG_NS, etiqueta);
      Object.entries(atributos).forEach(([clave, valor]) => el.setAttribute(clave, valor));
      svg.appendChild(el);
    });
  }

  // --- Vida del Kernel (R79) --------------------------------------------------

  function pintarVida(vida, delta) {
    $('vida-barra').style.width = vida + '%';
    $('vida-texto').textContent = vida + '%';
    $('vida').setAttribute('aria-valuenow', String(vida));
    const marca = $('vida-delta');
    if (delta) {
      marca.textContent = (delta < 0 ? '−' : '+') + Math.abs(delta) + '%';
      marca.className = 'bf-delta ' + (delta < 0 ? 'bueno' : 'malo');
    } else {
      marca.textContent = '';
      marca.className = 'bf-delta';
    }
  }

  // --- Temporizador (R78b): el servidor es quien lo hace valer -----------------

  function pintarReloj() {
    const segundos = Math.ceil(estado.resta);
    $('reto-reloj').textContent = segundos + ' s';
    $('reto-reloj').classList.toggle('urgente', segundos <= 5);
    $('tiempo-barra').style.width = (estado.resta / estado.total) * 100 + '%';
  }

  function detenerReloj() {
    clearInterval(estado.temporizador);
    estado.temporizador = null;
  }

  function arrancarReloj(total) {
    detenerReloj();
    estado.total = total;
    estado.resta = total;
    estado.pausado = false;
    pintarReloj();
    estado.temporizador = setInterval(() => {
      if (estado.pausado || estado.resuelto) return;
      estado.resta -= 0.1;
      if (estado.resta <= 0) {
        estado.resta = 0;
        pintarReloj();
        detenerReloj();
        avisarTiempoAgotado(0);
        return;
      }
      pintarReloj();
    }, 100);
  }

  async function avisarTiempoAgotado(intento) {
    estado.resuelto = true;
    try {
      resolver(await ReCode.postJSON(urls.tiempo));
    } catch (error) {
      // El reloj del servidor puede ir unos instantes detrás del del navegador.
      if (intento < 4) {
        setTimeout(() => avisarTiempoAgotado(intento + 1), 800);
      } else {
        $('reto-aviso').textContent = error.message;
        $('reto-aviso').className = 'bf-aviso malo';
      }
    }
  }

  // --- Tipos de reto ------------------------------------------------------------

  function actualizarBotonResponder(valido) {
    $('btn-responder').disabled = !valido;
  }

  function dibujarOpcion(reto, cuerpo) {
    const lista = crear('div', 'bf-opciones');
    reto.opciones.forEach((texto, indice) => {
      const boton = crearBoton('bf-opcion', texto, () => {
        lista.querySelectorAll('.bf-opcion').forEach((b) => b.classList.remove('sel'));
        boton.classList.add('sel');
        estado.respuesta = indice;
        actualizarBotonResponder(true);
      });
      lista.appendChild(boton);
    });
    cuerpo.appendChild(lista);
    estado.respuesta = null;
    actualizarBotonResponder(false);
  }

  function dibujarOrden(reto, cuerpo) {
    const orden = reto.pasos.slice();
    const lista = crear('div', 'bf-pasos');

    function pintar() {
      lista.replaceChildren();
      orden.forEach((texto, i) => {
        const fila = crear('div', 'bf-paso');
        fila.appendChild(crear('span', 'bf-paso-num', String(i + 1)));
        fila.appendChild(crear('span', '', texto));
        const botones = crear('span', 'bf-paso-botones');
        const subir = crearBoton('bf-mini', '↑', () => mover(i, -1));
        const bajar = crearBoton('bf-mini', '↓', () => mover(i, 1));
        subir.disabled = i === 0;
        bajar.disabled = i === orden.length - 1;
        subir.setAttribute('aria-label', 'Subir paso');
        bajar.setAttribute('aria-label', 'Bajar paso');
        botones.append(subir, bajar);
        fila.appendChild(botones);
        lista.appendChild(fila);
      });
      estado.respuesta = orden.slice();
    }

    function mover(i, direccion) {
      const j = i + direccion;
      [orden[i], orden[j]] = [orden[j], orden[i]];
      pintar();
    }

    cuerpo.appendChild(lista);
    pintar();
    actualizarBotonResponder(true);
  }

  function dibujarTerminal(reto, cuerpo) {
    const caja = crear('div', 'bf-terminal');
    caja.appendChild(crear('div', 'bf-terminal-ruta', 'alumno@recode:' + reto.directorio));
    const entrada = crear('div', 'bf-terminal-entrada');
    entrada.appendChild(crear('span', '', '$'));
    const campo = document.createElement('input');
    campo.type = 'text';
    campo.autocomplete = 'off';
    campo.spellcheck = false;
    campo.setAttribute('aria-label', 'Comando');
    campo.addEventListener('input', () => {
      estado.respuesta = campo.value;
      actualizarBotonResponder(campo.value.trim() !== '');
    });
    campo.addEventListener('keydown', (evento) => {
      if (evento.key === 'Enter' && campo.value.trim() !== '') responder();
    });
    entrada.appendChild(campo);
    caja.appendChild(entrada);
    cuerpo.appendChild(caja);
    estado.respuesta = '';
    actualizarBotonResponder(false);
    campo.focus();
  }

  function dibujarClasificar(reto, cuerpo) {
    const clases = {};
    const lista = crear('div', 'bf-clases');
    reto.elementos.forEach((elemento) => {
      const fila = crear('div', 'bf-clase');
      fila.appendChild(crear('span', 'bf-clase-texto', elemento));
      const categorias = crear('div', 'bf-clase-cats');
      reto.categorias.forEach((nombre, indice) => {
        const boton = crearBoton('bf-cat', nombre, () => {
          categorias.querySelectorAll('.bf-cat').forEach((b) => b.classList.remove('sel'));
          boton.classList.add('sel');
          clases[elemento] = indice;
          actualizarBotonResponder(Object.keys(clases).length === reto.elementos.length);
        });
        categorias.appendChild(boton);
      });
      fila.appendChild(categorias);
      lista.appendChild(fila);
    });
    cuerpo.appendChild(lista);
    estado.respuesta = clases;
    actualizarBotonResponder(false);
  }

  const DIBUJANTES = {
    opcion: dibujarOpcion,
    orden: dibujarOrden,
    terminal: dibujarTerminal,
    clasificar: dibujarClasificar,
  };

  // --- Flujo de la batalla -------------------------------------------------------

  function presentar(reto, ronda) {
    estado.reto = reto;
    estado.resuelto = false;
    $('reto-ronda').textContent = 'Ronda ' + ronda;
    $('reto-tipo').textContent = reto.nombre_tipo;
    $('reto-materia').textContent = reto.materia;
    $('reto-enunciado').textContent = reto.enunciado;
    $('reto-aviso').textContent = '';
    $('reto-aviso').className = 'bf-aviso';
    $('btn-siguiente').hidden = true;
    $('btn-responder').hidden = false;
    const cuerpo = $('reto-cuerpo');
    cuerpo.replaceChildren();
    DIBUJANTES[reto.tipo](reto, cuerpo);
    arrancarReloj(reto.tiempo); // el reloj empieza al presentar el reto
  }

  async function iniciar() {
    try {
      const datos = await ReCode.postJSON(urls.iniciar);
      pintarVida(datos.vida, 0);
      mostrar('batalla');
      presentar(datos.reto, datos.ronda);
    } catch (error) {
      $('btn-iniciar').textContent = error.message;
    }
  }

  async function siguiente() {
    try {
      const datos = await ReCode.postJSON(urls.siguiente);
      presentar(datos.reto, datos.ronda);
    } catch (error) {
      $('reto-aviso').textContent = error.message;
      $('reto-aviso').className = 'bf-aviso malo';
    }
  }

  async function responder() {
    if (estado.resuelto || $('btn-responder').disabled) return;
    estado.resuelto = true;
    detenerReloj();
    $('btn-responder').disabled = true;
    try {
      resolver(await ReCode.postJSON(urls.responder, { respuesta: estado.respuesta }));
    } catch (error) {
      $('reto-aviso').textContent = error.message;
      $('reto-aviso').className = 'bf-aviso malo';
    }
  }

  // Muestra el resultado de un reto: acierto, fallo con jumpscare, o victoria.
  function resolver(datos) {
    detenerReloj();
    estado.resuelto = true;
    pintarVida(datos.vida, datos.delta);
    $('btn-responder').hidden = true;
    if (datos.victoria) {
      // R81: el Kernel llegó a 0%, Re:Code queda completado.
      setTimeout(() => mostrar('victoria'), 700);
      return;
    }
    const aviso = $('reto-aviso');
    if (datos.correcto) {
      aviso.textContent = '✔ Reto superado · el Kernel pierde ' + Math.abs(datos.delta) + '%';
      aviso.className = 'bf-aviso bueno';
      $('btn-siguiente').hidden = false;
    } else {
      aviso.textContent = '✘ ' + datos.motivo + ' · el Kernel recupera ' + datos.delta + '%';
      aviso.className = 'bf-aviso malo';
      jumpscare(datos.motivo, () => {
        $('btn-siguiente').hidden = false;
      });
    }
  }

  // --- Jumpscare (R82b): en cada fallo, en dos fases ---------------------------------

  function jumpscare(motivo, alTerminar) {
    const capa = $('jumpscare');
    $('jumpscare-motivo').textContent = motivo + '. El Kernel recupera vida.';
    capa.classList.remove('fase-bloqueo');
    capa.hidden = false;
    setTimeout(() => capa.classList.add('fase-bloqueo'), FASE_BLOQUEO);
    setTimeout(() => {
      capa.hidden = true;
      capa.classList.remove('fase-bloqueo');
      alTerminar();
    }, DURACION_JUMPSCARE);
  }

  // --- Abandono (R80) ------------------------------------------------------------------

  function pausar(valor) {
    estado.pausado = valor;
    if (estado.resuelto) return; // sin reto corriendo no hay reloj que pausar
    ReCode.postJSON(urls.pausa, { pausar: valor }).catch(() => {});
  }

  function pedirAbandono() {
    pausar(true);
    $('dialogo-abandono').showModal();
  }

  function cancelarAbandono() {
    $('dialogo-abandono').close();
  }

  async function confirmarAbandono() {
    $('dialogo-abandono').close('abandonar');
    detenerReloj();
    estado.resuelto = true;
    try {
      await ReCode.postJSON(urls.abandonar);
    } catch (error) {
      // Aunque falle el aviso, la pantalla no marca Re:Code como completado.
    }
    mostrar('abandono');
  }

  // --- Arranque --------------------------------------------------------------------------

  ['kernel-intro', 'kernel-batalla'].forEach((id) => dibujarKernel($(id)));
  $('btn-iniciar').addEventListener('click', iniciar);
  $('btn-responder').addEventListener('click', responder);
  $('btn-siguiente').addEventListener('click', siguiente);
  $('btn-abandonar').addEventListener('click', pedirAbandono);
  $('btn-cancelar-abandono').addEventListener('click', cancelarAbandono);
  $('btn-confirmar-abandono').addEventListener('click', confirmarAbandono);
  $('btn-cierre').addEventListener('click', () => mostrar('cierre'));
  // Cancelar (botón o Esc) deja la batalla como estaba y reanuda el reloj.
  $('dialogo-abandono').addEventListener('close', (evento) => {
    if (evento.target.returnValue !== 'abandonar') pausar(false);
    evento.target.returnValue = '';
  });
})(window.ReCode);
