// El término oculto (CU-09), estilo Wordle.
// El navegador solo conoce el largo, los intentos y la pista; Django revisa
// cada palabra y regresa los colores (verde / amarillo / gris).
(() => {
    const { letras, intentos, pista } = ReCode.reto.datos;
    const raiz = document.getElementById("termino");
    const reiniciarUrl = raiz.dataset.reiniciarUrl;
    const cuadricula = document.getElementById("cuadricula");
    const teclado = document.getElementById("teclado");
    const resultado = document.getElementById("resultado");
    const btnReintentar = document.getElementById("btn-reintentar");
    const btnSalir = document.getElementById("btn-salir");
    const dialogo = document.getElementById("dialogo-salir");
    const dialogoExito = document.getElementById("dialogo-exito");
    const dialogoAgotado = document.getElementById("dialogo-agotado");

    const RENGLONES = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"];
    const PRIORIDAD = { gris: 1, amarillo: 2, verde: 3 };

    let fila = 0;          // intento actual (renglón de la cuadrícula)
    let escrito = "";      // letras del intento actual
    let bloqueado = false; // true mientras espera al servidor o cuando acabó

    // --- Dibujo -------------------------------------------------------------

    function armarCuadricula() {
        cuadricula.innerHTML = "";
        for (let f = 0; f < intentos; f++) {
            const div = document.createElement("div");
            div.className = "fila";
            for (let c = 0; c < letras; c++) {
                const celda = document.createElement("div");
                celda.className = "celda";
                div.appendChild(celda);
            }
            cuadricula.appendChild(div);
        }
    }

    function armarTeclado() {
        teclado.innerHTML = "";
        RENGLONES.forEach((renglon, i) => {
            const div = document.createElement("div");
            div.className = "renglon";
            if (i === 2) div.appendChild(tecla("ENTER", "Enviar", true));
            for (const letra of renglon) div.appendChild(tecla(letra, letra));
            if (i === 2) div.appendChild(tecla("BORRAR", "⌫", true));
            teclado.appendChild(div);
        });
    }

    function tecla(valor, texto, ancha = false) {
        const b = document.createElement("button");
        b.type = "button";
        b.textContent = texto;
        b.dataset.tecla = valor;
        if (ancha) b.classList.add("ancha");
        b.addEventListener("click", () => presionar(valor));
        return b;
    }

    function celdas(f) {
        return cuadricula.children[f].children;
    }

    function pintarEscrito() {
        const cs = celdas(fila);
        for (let i = 0; i < letras; i++) {
            cs[i].textContent = escrito[i] || "";
            cs[i].classList.toggle("escrita", Boolean(escrito[i]));
        }
    }

    function pintarColores(f, intento, colores) {
        const cs = celdas(f);
        colores.forEach((color, i) => {
            cs[i].textContent = intento[i];
            cs[i].classList.add(color);
            const boton = teclado.querySelector(`[data-tecla="${intento[i]}"]`);
            if (!boton) return;
            const actual = boton.dataset.color;
            if (!actual || PRIORIDAD[color] > PRIORIDAD[actual]) {
                if (actual) boton.classList.remove(actual);
                boton.classList.add(color);
                boton.dataset.color = color;
            }
        });
    }

    function mostrarIntentos(restantes) {
        document.getElementById("intentos").textContent = `Intentos: ${restantes} de ${intentos}`;
    }

    function mensaje(html, error = false) {
        resultado.innerHTML = `<p class="mensaje ${error ? "error" : ""}">${html}</p>`;
    }

    function sacudir() {
        const div = cuadricula.children[fila];
        div.classList.remove("sacudir");
        void div.offsetWidth; // reinicia la animación
        div.classList.add("sacudir");
    }

    // --- Juego --------------------------------------------------------------

    function presionar(valor) {
        if (bloqueado) return;
        if (valor === "ENTER") return enviar();
        if (valor === "BORRAR") {
            escrito = escrito.slice(0, -1);
        } else if (/^[A-Z]$/.test(valor) && escrito.length < letras) {
            escrito += valor;
        }
        pintarEscrito();
    }

    async function enviar() {
        if (escrito.length !== letras) {
            mensaje(`El término tiene ${letras} letras.`, true);
            sacudir();
            return;
        }
        bloqueado = true;
        let r;
        try {
            r = await ReCode.postJSON(ReCode.reto.revisarUrl, { respuesta: escrito });
        } catch (err) {
            mensaje(err.message, true);
            sacudir();
            bloqueado = false;
            return;
        }

        const saldo = document.getElementById("bitcoins-alumno");
        if (saldo) saldo.textContent = r.bitcoins_total;

        pintarColores(fila, r.intento, r.colores);
        mostrarIntentos(r.intentos_restantes);
        fila++;
        escrito = "";

        if (r.correcto) return exito(r);
        if (r.agotado) return agotado(r);
        mensaje(r.mensaje, true);
        bloqueado = false;
    }

    // Paso 6-7 del flujo normal: significado + bitcoins y regreso a los retos.
    function exito(r) {
        document.getElementById("acciones").hidden = true;
        const premio = r.ya_otorgado
            ? "La recompensa de este reto ya se te había otorgado antes."
            : `Obtuviste <strong>₿ ${r.bitcoins_otorgados}</strong>.`;
        document.getElementById("exito-mensaje").innerHTML = `<strong>${r.mensaje}</strong>`;
        document.getElementById("exito-significado").innerHTML = r.significado;
        document.getElementById("exito-premio").innerHTML = premio;
        ReCode.dialogos.abrir(dialogoExito);
    }

    // FA-1: intentos agotados -> ventana emergente con Reintentar o Salir.
    // El botón "Salir / Rendirse" normal (fuera del diálogo) nunca se oculta.
    function agotado(r) {
        document.getElementById("agotado-mensaje").textContent = r.mensaje;
        ReCode.dialogos.abrir(dialogoAgotado);
    }

    async function reintentar() {
        try {
            const r = await ReCode.postJSON(reiniciarUrl);
            ReCode.dialogos.cerrar(dialogoAgotado);
            iniciar(r.intentos_restantes);
        } catch (err) {
            mensaje(err.message, true);
        }
    }

    function iniciar(restantes = intentos) {
        fila = 0;
        escrito = "";
        bloqueado = false;
        resultado.innerHTML = "";
        armarCuadricula();
        armarTeclado();
        mostrarIntentos(restantes);
    }

    // --- FE-1: salir / rendirse con confirmación ----------------------------
    // Diálogo y mensaje de salida compartidos con los demás retos
    // (comun/reto_base.html + comun/js/reto_dialogos.js). "Salir / Rendirse"
    // dentro de la ventana de agotado reusa el mismo flujo (FA-1.4.5).
    ReCode.dialogos.inicializarSalir({
        hayProgreso: () => fila > 0 && !bloqueado,
    });
    document.getElementById("btn-salir-agotado").addEventListener("click", () => btnSalir.click());

    btnReintentar.addEventListener("click", reintentar);

    // Teclado físico.
    document.addEventListener("keydown", (e) => {
        if (e.ctrlKey || e.metaKey || e.altKey || dialogo.open) return;
        if (e.key === "Enter") { e.preventDefault(); presionar("ENTER"); }
        else if (e.key === "Backspace") { e.preventDefault(); presionar("BORRAR"); }
        else if (/^[a-zA-Z]$/.test(e.key)) presionar(e.key.toUpperCase());
    });

    if (pista) document.getElementById("pista").textContent = `Pista: ${pista}`;
    iniciar();
})();
