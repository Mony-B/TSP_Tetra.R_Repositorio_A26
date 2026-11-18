// Catálogo de la red corrupta (CU03): abre el panel de una pista, maneja
// la confirmación de compra (FA-2), el ofrecimiento de Snake cuando falta
// saldo (FA-1) y el minijuego en sí. Todo lo que el servidor necesita
// saber ya lo manda red_corrupta.html en window.RedCorrupta.
(() => {
    "use strict";
    const panel = document.getElementById("panel-pista");
    const vistas = {
        bloqueada: document.getElementById("vista-bloqueada"),
        insuficiente: document.getElementById("vista-insuficiente"),
        revelada: document.getElementById("vista-revelada"),
        snake: document.getElementById("vista-snake"),
    };
    const panelContexto = document.getElementById("panel-contexto");
    const panelTermino = document.getElementById("panel-termino");
    const textoDefinicion = document.getElementById("texto-definicion");
    const snakeEstado = document.getElementById("snake-estado");
    const snakeMeta = document.getElementById("snake-meta");
    const snakeMensaje = document.getElementById("snake-mensaje");
    const snakeLienzo = document.getElementById("snake-lienzo");
    const btnReintentar = document.getElementById("btn-reintentar-snake");

    let pistaActual = null; // botón .pista que abrió el panel

    function mostrarVista(nombre) {
        Object.entries(vistas).forEach(([k, el]) => { el.hidden = k !== nombre; });
    }

    function urlPara(base, id) {
        return base.replace("__ID__", encodeURIComponent(id));
    }

    function abrirPanel(boton) {
        pistaActual = boton;
        const contexto = boton.closest(".subtema").querySelector("h3").textContent;
        panelContexto.textContent = contexto;
        panelTermino.textContent = boton.dataset.termino;
        snakeMensaje.classList.remove("mostrar");
        btnReintentar.hidden = true;

        if (boton.dataset.obtenida === "1") {
            textoDefinicion.textContent = boton.dataset.definicion;
            mostrarVista("revelada");
        } else {
            mostrarVista("bloqueada");
        }
        panel.showModal();
    }

    document.querySelectorAll(".pista").forEach((b) => b.addEventListener("click", () => abrirPanel(b)));

    function actualizarBitcoins(total) {
        const el = document.getElementById("bitcoins-alumno");
        if (el) el.textContent = total;
    }

    function marcarObtenida(termino, definicion) {
        pistaActual.dataset.obtenida = "1";
        pistaActual.dataset.definicion = definicion;
        pistaActual.classList.add("obtenida");
        pistaActual.querySelector(".candado").textContent = "✓";
        textoDefinicion.textContent = definicion;
    }

    // --- FA-2: cancelar antes de confirmar la compra ------------------------
    document.getElementById("btn-cancelar-compra").addEventListener("click", () => panel.close());

    // --- Compra (flujo normal 3-5 / FA-1) -----------------------------------
    document.getElementById("btn-confirmar-compra").addEventListener("click", async () => {
        const boton = document.getElementById("btn-confirmar-compra");
        boton.disabled = true;
        try {
            const r = await ReCode.postJSON(urlPara(window.RedCorrupta.comprarUrlBase, pistaActual.dataset.id));
            actualizarBitcoins(r.bitcoins_total);
            if (r.ok) {
                marcarObtenida(r.termino, r.definicion);
                mostrarVista("revelada");
            } else {
                mostrarVista("insuficiente");
            }
        } finally {
            boton.disabled = false;
        }
    });

    // --- FA-1: saldo insuficiente, ofrece Snake -----------------------------
    document.getElementById("btn-rechazar-snake").addEventListener("click", () => panel.close());
    document.getElementById("btn-aceptar-snake").addEventListener("click", () => {
        mostrarVista("snake");
        iniciarSnake();
    });

    function iniciarSnake() {
        snakeMensaje.classList.remove("mostrar");
        btnReintentar.hidden = true;
        const { nivel, meta } = Snake.iniciar(snakeLienzo, {
            onProgreso: (comidos) => { snakeMeta.textContent = `${comidos}/${meta}`; },
            onVictoria: onSnakeVictoria,
            onDerrota: onSnakeDerrota,
        });
        snakeEstado.innerHTML = `Nivel ${nivel}: come <span id="snake-meta">0/${meta}</span> datos sin chocar.`;
    }

    async function onSnakeVictoria() {
        snakeMensaje.textContent = "Acceso concedido. Extrayendo dato...";
        snakeMensaje.classList.add("mostrar");
        try {
            const r = await ReCode.postJSON(urlPara(window.RedCorrupta.snakeUrlBase, pistaActual.dataset.id));
            actualizarBitcoins(r.bitcoins_total);
            marcarObtenida(r.termino, r.definicion);
            mostrarVista("revelada");
        } catch (err) {
            snakeMensaje.textContent = "No se pudo entregar la pista. Vuelve a intentarlo.";
        }
    }

    function onSnakeDerrota() {
        snakeMensaje.textContent = "Conexión perdida. Puedes reintentar de inmediato, sin espera.";
        snakeMensaje.classList.add("mostrar");
        btnReintentar.hidden = false;
    }

    // FA-1 (4a.5): reintento inmediato, sin bloqueo ni cambio de saldo.
    btnReintentar.addEventListener("click", iniciarSnake);

    // FA-3: abandono voluntario de Snake, sin pista ni cambio de saldo.
    document.getElementById("btn-abandonar-snake").addEventListener("click", () => {
        Snake.detener();
        panel.close();
    });

    document.getElementById("btn-cerrar-revelada").addEventListener("click", () => panel.close());

    // Cerrar el dialog por cualquier vía (Esc incluido) siempre detiene Snake,
    // para no dejar el ciclo de juego corriendo de fondo.
    panel.addEventListener("close", () => Snake.detener());
})();
