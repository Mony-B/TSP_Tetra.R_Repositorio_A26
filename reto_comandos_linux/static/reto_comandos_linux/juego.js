// Comandos de Linux (CU-06): terminal simulada + puerta con contraseña.
// El navegador solo manda lo que escribe el alumno; Django interpreta cada
// comando contra el sistema de archivos simulado y valida la contraseña.
(() => {
    const { prompt: promptInicial } = ReCode.reto.datos;
    const raiz = document.getElementById("linux");
    const comandoUrl = raiz.dataset.comandoUrl;
    const terminal = document.getElementById("terminal");
    const lineas = document.getElementById("lineas");
    const prompt = document.getElementById("prompt");
    const inputComando = document.getElementById("comando");
    const inputClave = document.getElementById("clave");
    const resultado = document.getElementById("resultado");
    const dialogo = document.getElementById("dialogo-salir");
    const SEGUNDOS_REDIRECCION = 10;

    let promptTexto = promptInicial;
    let oculto = false;    // la siguiente línea es una contraseña (su): no se muestra
    let ocupado = false;   // esperando al servidor
    let terminado = false; // la puerta ya se abrió

    // --- Terminal -----------------------------------------------------------

    function textoPrompt() {
        return oculto ? "Contraseña:" : promptTexto;
    }

    function pintarPrompt() {
        prompt.textContent = textoPrompt();
        inputComando.type = oculto ? "password" : "text";
    }

    function escribir(texto, clase = "") {
        const div = document.createElement("div");
        div.className = `linea ${clase}`;
        div.textContent = texto;
        lineas.appendChild(div);
        terminal.scrollTop = terminal.scrollHeight;
    }

    document.getElementById("form-comando").addEventListener("submit", async (e) => {
        e.preventDefault();
        if (ocupado || terminado) return;
        const comando = inputComando.value;
        inputComando.value = "";
        escribir(oculto ? textoPrompt() : `${textoPrompt()} ${comando}`);
        if (!comando.trim() && !oculto) return; // solo Enter: nuevo prompt (FA-1)

        ocupado = true;
        try {
            const r = await ReCode.postJSON(comandoUrl, { comando });
            if (r.limpiar) lineas.innerHTML = "";
            if (r.salida) escribir(r.salida, r.error ? "error" : "");
            promptTexto = r.prompt;
            oculto = r.oculto;
            pintarPrompt();
        } catch (err) {
            escribir(err.message, "error");
        } finally {
            ocupado = false;
            inputComando.focus();
        }
    });

    terminal.addEventListener("click", () => {
        if (!window.getSelection().toString()) inputComando.focus();
    });

    // --- Puerta -------------------------------------------------------------

    function mensaje(html, error = false) {
        resultado.innerHTML = `<p class="mensaje ${error ? "error" : ""}">${html}</p>`;
    }

    function escapar(texto) {
        const d = document.createElement("div");
        d.textContent = texto;
        return d.innerHTML;
    }

    document.getElementById("form-puerta").addEventListener("submit", async (e) => {
        e.preventDefault();
        if (ocupado || terminado) return;
        const clave = inputClave.value.trim();
        if (!clave) {
            mensaje("Escribe la contraseña de la puerta.", true);
            return;
        }
        ocupado = true;
        try {
            const r = await ReCode.postJSON(ReCode.reto.revisarUrl, { respuesta: clave });
            const saldo = document.getElementById("bitcoins-alumno");
            if (saldo) saldo.textContent = r.bitcoins_total;
            if (r.correcto) return exito(r);
            mensaje(escapar(r.mensaje), true); // FA-3: la puerta sigue cerrada, sin límite
            inputClave.select();
        } catch (err) {
            mensaje(escapar(err.message), true);
        } finally {
            ocupado = false;
        }
    });

    // Pasos 7-8: mensaje de victoria, bitcoins (solo la primera vez) y regreso.
    function exito(r) {
        terminado = true;
        document.getElementById("icono-puerta").textContent = "🔓";
        document.getElementById("puerta").classList.add("abierta");
        inputComando.disabled = true;
        inputClave.disabled = true;
        document.getElementById("btn-abrir").disabled = true;
        document.getElementById("acciones").hidden = true;

        const premio = r.ya_otorgado
            ? "La recompensa de este reto ya se te había otorgado antes."
            : `Obtuviste <strong>₿ ${r.bitcoins_otorgados}</strong>.`;
        resultado.innerHTML = `
            <div class="mensaje">
                <p><strong>${escapar(r.mensaje)}</strong> Superaste el reto.</p>
                <p>${premio}</p>
                <p class="etiqueta">Regresando a los retos en <span id="cuenta">${SEGUNDOS_REDIRECCION}</span> s…</p>
            </div>
            <a class="boton" href="${ReCode.reto.volverUrl}">Volver a los retos</a>`;
        let quedan = SEGUNDOS_REDIRECCION;
        const reloj = setInterval(() => {
            quedan--;
            const cuenta = document.getElementById("cuenta");
            if (cuenta) cuenta.textContent = quedan;
            if (quedan <= 0) {
                clearInterval(reloj);
                window.location.href = ReCode.reto.volverUrl;
            }
        }, 1000);
    }

    // --- FE-1: salir / rendirse con confirmación ----------------------------

    function pedirSalida(e) {
        if (e) e.preventDefault();
        if (typeof dialogo.showModal === "function") {
            dialogo.showModal();
        } else if (window.confirm("Se perderá el progreso de este reto y no obtendrás bitcoins. ¿Salir?")) {
            window.location.href = ReCode.reto.volverUrl;
        }
    }

    document.getElementById("btn-salir").addEventListener("click", pedirSalida);
    // La flecha de regresar de la plantilla también pide confirmación mientras se juega.
    const flecha = document.querySelector(".btn-regresar");
    if (flecha) flecha.addEventListener("click", (e) => { if (!terminado) pedirSalida(e); });
    document.getElementById("btn-cancelar-salida").addEventListener("click", () => {
        dialogo.close();
        inputComando.focus();
    });
    document.getElementById("btn-confirmar-salida").addEventListener("click", () => {
        window.location.href = ReCode.reto.volverUrl; // no se guarda nada ni se dan bitcoins
    });

    pintarPrompt();
    inputComando.focus();
})();