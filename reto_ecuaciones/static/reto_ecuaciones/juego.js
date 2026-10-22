// Ecuaciones lineales (CU-07) "Resolver ecuaciones lineales en una matriz".
// El navegador solo muestra las matrices y las pistas y manda los valores
// escritos. Quien valida que sean naturales y evalúa las pistas es la vista de
// Django (views.revisar).
function iniciarMatriz() {
  const raiz = document.getElementById('matriz');
  const datosTag = document.getElementById('matriz-datos');
  if (!raiz || !datosTag) {
    console.error('Matriz: falta #matriz o #matriz-datos en reto.html');
    return;
  }
  const datos = JSON.parse(datosTag.textContent);
  if (!datos.matriz || !datos.pistas || !datos.celdas) {
    raiz.insertAdjacentHTML(
      'afterbegin',
      '<p class="matriz-mensaje error">Datos del reto desactualizados: ' +
        'reemplaza ejercicios.py por la versión nueva y reinicia el ' +
        'servidor.</p>'
    );
    console.error('Matriz: datos_publicos incompleto. ¿ejercicios.py viejo?', datos);
    return;
  }
  const revisarUrl = raiz.dataset.revisarUrl;
  const $ = id => document.getElementById(id);
  const cajas = {};  // nombre de celda -> <input>

  $('matriz-mision').textContent = datos.mision;

  // --- Matrices ------------------------------------------------------------
  function celdaFija(valor) {
    const celda = document.createElement('div');
    celda.className = 'celda';
    celda.textContent = valor;
    return celda;
  }
  function indice(texto) {  // encabezado de índice fila/columna
    const celda = document.createElement('div');
    celda.className = 'indice';
    celda.textContent = texto;
    return celda;
  }
  function encabezado(rejilla) {
    rejilla.appendChild(indice('F\\C'));
    [0, 1, 2].forEach(j => rejilla.appendChild(indice(`[${j}]`)));
  }
  encabezado($('matriz-referencia'));
  encabezado($('matriz-respuesta'));

  datos.matriz.forEach((fila, i) => {
    $('matriz-referencia').appendChild(indice(`[${i}]`));
    $('matriz-respuesta').appendChild(indice(`[${i}]`));
    fila.forEach(valor => {
      const esIncognita = typeof valor === 'string';
      // Referencia: valores conocidos y nombre de las cajas por completar.
      const referencia = celdaFija(esIncognita ? `Caja ${valor}` : valor);
      if (esIncognita) {
        referencia.classList.add('celda-incognita');
      }
      $('matriz-referencia').appendChild(referencia);

      // Respuesta: conocidos fijos y un cuadro de texto por incógnita.
      if (!esIncognita) {
        $('matriz-respuesta').appendChild(celdaFija(valor));
        return;
      }
      const caja = document.createElement('input');
      caja.type = 'text';
      caja.inputMode = 'numeric';
      caja.autocomplete = 'off';
      caja.className = 'celda celda-caja';
      caja.setAttribute('aria-label', `Valor de ${valor}`);
      caja.placeholder = valor;
      caja.addEventListener('input', () => {
        caja.classList.remove('celda-mala');
        pintarVivas();
      });
      caja.addEventListener('keydown', evento => {
        if (evento.key === 'Enter') {
          $('btn-verificar').click();
        }
      });
      cajas[valor] = caja;
      $('matriz-respuesta').appendChild(caja);
    });
  });

  // --- Listas de pistas ----------------------------------------------------
  // Original: tal como son. Viva: copia con lo que vas escribiendo (solo lo
  // muestra, NO evalúa).
  datos.pistas.forEach(texto => {
    const item = document.createElement('li');
    item.textContent = texto;
    $('pistas-originales').appendChild(item);
  });
  function pintarVivas() {
    const lista = $('pistas-vivas');
    lista.innerHTML = '';
    datos.pistas.forEach(texto => {
      const item = document.createElement('li');
      item.textContent = texto.replace(/Matriz\[(\d)\]\[(\d)\]/g, (ref, i, j) => {
        const valor = datos.matriz[i][j];
        if (typeof valor !== 'string') {
          return String(valor);
        }
        const escrito = cajas[valor].value.trim();
        return escrito === '' ? ref : escrito;
      });
      lista.appendChild(item);
    });
  }
  function todasLasPistas() {
    return [...$('pistas-originales').children, ...$('pistas-vivas').children];
  }
  function marcarPistasMalas(numeros) {
    todasLasPistas().forEach((item, i) => {
      const numero = (i % datos.pistas.length) + 1;
      item.classList.toggle('pista-mala', numeros.includes(numero));
    });
  }
  function limpiarMarcas() {
    marcarPistasMalas([]);
    Object.values(cajas).forEach(caja => caja.classList.remove('celda-mala'));
  }

  // --- Verificar (el servidor decide) --------------------------------------
  function valoresComoTexto() {
    return datos.celdas
      .map(celda => `${celda.nombre}=${cajas[celda.nombre].value.trim()}`)
      .join(',');
  }
  function mostrarError(texto) {
    $('matriz-aviso').textContent = texto;
    $('matriz-error').hidden = !texto;
  }
  function numerosDe(mensaje) {  // 'Pistas que no se cumplen: 1, 2 y 6.'
    const coincidencia = mensaje.match(/:\s*([\d, y]+)\.?$/);
    return coincidencia ? (coincidencia[1].match(/\d+/g) || []).map(Number) : [];
  }
  function nombresDe(mensaje) {  // 'Cuadros por corregir: A, B y F.'
    const coincidencia = mensaje.match(/Cuadros por corregir:\s*(.+?)\.?$/);
    return coincidencia
      ? coincidencia[1].split(/,| y /).map(nombre => nombre.trim()).filter(Boolean)
      : [];
  }

  $('btn-verificar').addEventListener('click', async () => {
    $('btn-verificar').disabled = true;
    limpiarMarcas();
    mostrarError('');
    try {
      const respuesta = await ReCode.postJSON(revisarUrl, {
        paso: 0,
        respuesta: valoresComoTexto()
      });
      const monedero = $('bitcoins-alumno');
      if (monedero && respuesta.bitcoins_total !== undefined) {
        monedero.textContent = respuesta.bitcoins_total;
      }
      if (respuesta.correcto) {
        mostrarExito(respuesta);
        return;
      }
      const mensaje = respuesta.mensaje || datos.mensaje_incorrecto;
      if (mensaje.startsWith(datos.mensaje_invalido)) {  // FA-2
        nombresDe(mensaje).forEach(nombre => {
          if (cajas[nombre]) {
            cajas[nombre].classList.add('celda-mala');
          }
        });
      } else {  // FA-1
        marcarPistasMalas(numerosDe(mensaje));
      }
      mostrarError(`Error. ${mensaje}`);
      $('btn-verificar').disabled = false;
    } catch (error) {
      mostrarError(error.message);
      $('btn-verificar').disabled = false;
    }
  });

  // Reintentar: quita el error y deja al alumno corregir (los valores se
  // conservan, no hay límite de intentos).
  $('btn-reintentar').addEventListener('click', () => {
    limpiarMarcas();
    mostrarError('');
    const primera = datos.celdas.find(celda => !/^\d+$/.test(cajas[celda.nombre].value.trim()));
    cajas[(primera || datos.celdas[0]).nombre].focus();
  });

  // Paso 6: las pistas se marcan como cumplidas y se muestra la victoria.
  function mostrarExito(respuesta) {
    Object.values(cajas).forEach(caja => {
      caja.readOnly = true;
    });
    todasLasPistas().forEach(item => item.classList.add('pista-cumplida'));
    $('matriz-mision').hidden = true;
    $('matriz-acciones').hidden = true;
    $('resultado-exito').hidden = false;
    $('exito-recompensa').textContent = respuesta.bitcoins_otorgados
      ? `+${respuesta.bitcoins_otorgados} ₿`
      : 'La recompensa de este reto ya fue otorgada anteriormente.';
  }

  // --- Salir / Rendirse (FE-1): no se guarda nada --------------------------
  $('btn-salir').addEventListener('click', () => {
    $('confirmar-salir').hidden = false;
  });
  $('btn-salir-no').addEventListener('click', () => {
    $('confirmar-salir').hidden = true;
  });

  pintarVivas();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', iniciarMatriz);
} else {
  iniciarMatriz();
}
