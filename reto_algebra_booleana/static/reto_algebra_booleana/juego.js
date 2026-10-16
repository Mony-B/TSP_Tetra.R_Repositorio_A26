// Álgebra booleana (CU-05) "Puertas lógicas".
// El navegador solo muestra los LEDs en vivo y manda el estado de los interruptores.
// Quien decide si el foco prende o truena es la vista de Django (views.revisar).
function iniciarPuertas() {
    const raiz = document.getElementById("puertas");
    const datosTag = document.getElementById("puertas-datos");
    if (!raiz || !datosTag) { console.error("Puertas lógicas: falta #puertas o #puertas-datos en reto.html"); return; }
    const datos = JSON.parse(datosTag.textContent);
    if (!datos.pasos || !datos.pasos[0] || !datos.pasos[0].variables) {
        raiz.insertAdjacentHTML("afterbegin",
            '<p class="puertas-mensaje error">Datos del reto desactualizados: reemplaza ejercicios.py por la versión nueva y reinicia el servidor.</p>');
        console.error("Puertas lógicas: datos_publicos no trae pasos[].variables. ¿ejercicios.py viejo?", datos);
        return;
    }
    const revisarUrl = raiz.dataset.revisarUrl;

    const $ = id => document.getElementById(id);
    const escena = $("escena");
    const resultado = $("resultado-puertas");
    const confirmar = $("confirmar-salir");
    const foco = $("foco");
    const circuito = $("circuito");

    const pasos = datos.pasos;
    let actual = 0;
    let estado = {};

    $("puertas-enunciado").textContent = datos.instrucciones;

    // --- Interruptores y LEDs ------------------------------------------------
    let leds = {};
    let interruptores = {};

    function crearInterruptor(nombre, indice) {
        if (indice > 0) {
            const op = document.createElement("span");
            op.className = "puertas-operador";
            op.textContent = pasos[actual].operador;
            circuito.appendChild(op);
        }
        const col = document.createElement("div");
        col.className = "puertas-columna";

        const led = document.createElement("span");
        led.className = "led";
        led.setAttribute("aria-hidden", "true");

        const etiqueta = document.createElement("span");
        etiqueta.className = "puertas-variable";
        etiqueta.textContent = nombre;

        const sw = document.createElement("button");
        sw.type = "button";
        sw.className = "interruptor";
        sw.setAttribute("role", "switch");
        sw.setAttribute("aria-label", `Interruptor ${nombre}`);
        sw.innerHTML = '<span class="int-1">1</span><span class="int-0">0</span>';
        sw.addEventListener("click", () => {
            estado[nombre] = estado[nombre] ? 0 : 1;
            pintar();
        });

        col.append(led, etiqueta, sw);
        circuito.appendChild(col);
        leds[nombre] = led;
        interruptores[nombre] = sw;
    }
    // Arma la puerta `actual`: interruptores nuevos, en su estado inicial.
    function cargarPuerta() {
        const paso = pasos[actual];
        circuito.innerHTML = "";
        leds = {};
        interruptores = {};
        estado = {};
        paso.variables.forEach(v => { estado[v] = paso.inicial ? paso.inicial[v] : 0; });
        paso.variables.forEach(crearInterruptor);
        $("puertas-leyenda").textContent = paso.leyenda;
        $("puertas-avance").textContent = `Puerta ${actual + 1} de ${pasos.length}`;
        pintar();
        mostrarEscena();
    }

    function pintar() {
        pasos[actual].variables.forEach(n => {
            const on = estado[n] === 1;
            leds[n].classList.toggle("led-on", on);
            interruptores[n].classList.toggle("interruptor-on", on);
            interruptores[n].setAttribute("aria-checked", on ? "true" : "false");
        });
    }

    function estadoComoTexto() {
        return pasos[actual].variables.map(n => `${n}=${estado[n]}`).join(",");
    }

    // --- Pantallas -----------------------------------------------------------
    function ponerFoco(modo) {            // "parpadea" | "encendido" | "roto"
        foco.classList.remove("foco-parpadea", "foco-encendido", "foco-roto");
        foco.classList.add(`foco-${modo}`);
    }

    function mostrarEscena() {
        resultado.hidden = true;
        confirmar.hidden = true;
        escena.hidden = false;
        $("btn-verificar").disabled = false;
        ponerFoco("parpadea");
    }

    function mostrarResultado(r) {
        // El foco se queda visible dentro de la escena; ocultamos solo los controles.
        $("btn-verificar").disabled = true;
        const ok = r.correcto;
        ponerFoco(ok ? "encendido" : "roto");
        resultado.hidden = false;

        $("puertas-mensaje").textContent = r.mensaje || (ok ? "Correcto." : "Incorrecto.");
        $("puertas-mensaje").className = "puertas-mensaje" + (ok ? "" : " error");

        const rec = $("puertas-recompensa");
        if (ok) {
            rec.hidden = false;
            rec.textContent = r.bitcoins_otorgados
                ? `Recompensa: +₿ ${r.bitcoins_otorgados}`
                : "La recompensa de este reto ya fue otorgada anteriormente.";
        } else {
            rec.hidden = true;
        }
        const fin = ok && r.completado;
        $("btn-reintentar").hidden = ok;
        $("btn-siguiente-puerta").hidden = !(ok && !r.completado);
        $("btn-siguiente").hidden = !fin;
        // La recompensa solo se muestra al terminar la última puerta.
        if (ok && !r.completado) rec.hidden = true;
    }

    // --- Verificar (el servidor decide) ----------------------------------------
    $("btn-verificar").addEventListener("click", async () => {
        $("btn-verificar").disabled = true;
        try {
            const r = await ReCode.postJSON(revisarUrl, { paso: actual, respuesta: estadoComoTexto() });
            const monedero = $("bitcoins-alumno");
            if (monedero && r.bitcoins_total !== undefined) monedero.textContent = r.bitcoins_total;
            mostrarResultado(r);
        } catch (e) {
            $("btn-verificar").disabled = false;
            resultado.hidden = false;
            $("puertas-mensaje").textContent = e.message;
            $("puertas-mensaje").className = "puertas-mensaje error";
            $("btn-reintentar").hidden = true;
            $("btn-siguiente-puerta").hidden = true;
            $("btn-siguiente").hidden = true;
        }
    });

    // --- Reintentar (FA-1): vuelve al paso 2, empieza de cero (nota 1) ------------
    $("btn-reintentar").addEventListener("click", cargarPuerta);

    // Puerta superada: pasa a la siguiente.
    $("btn-siguiente-puerta").addEventListener("click", () => {
        actual++;
        cargarPuerta();
    });

    // --- Salir / Rendirse (FE-1) ---------------------------------------------
    $("btn-salir").addEventListener("click", () => { confirmar.hidden = false; });
    $("btn-seguir").addEventListener("click", () => { confirmar.hidden = true; });

    cargarPuerta();
}

// El script puede cargarse antes de que exista el HTML del reto: esperamos al DOM.
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciarPuertas);
} else {
    iniciarPuertas();
}
