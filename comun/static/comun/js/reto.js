// Pantalla de reto (app comun): encendido del monitor -> reto.
// El juego de cada app ya está cargado desde el inicio; mientras no está
// "listo" se bloquea el teclado para que no se manden respuestas por accidente.
(function () {
    const body = document.body;
    const $ = (id) => document.getElementById(id);
    const movimientoReducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    let estado = body.dataset.estado || "apagado";
    function ponerEstado(nuevo) {
        estado = nuevo;
        body.dataset.estado = nuevo;
    }

    // Mientras el monitor enciende, el teclado no hace nada.
    window.addEventListener("keydown", (e) => {
        if (estado === "listo") return;
        e.stopImmediatePropagation();
    }, true);

    // ------------------------------------------------------------------
    // Encendido del monitor
    // ------------------------------------------------------------------
    function encender() {
        ponerEstado("encendiendo");
        const titulo = (document.querySelector(".crt-contenido h1") || {}).textContent || "reto";
        const arranque = $("crt-arranque");
        const mensajes = [
            "RE:CODE BIOS v1.0.0  (c) UAZ // CAMPUS",
            "Memoria ............ 640K OK",
            "Unidad A: .......... OK",
            "Señal externa ...... DETECTADA [MARÍA]",
            "Aislando proceso ... OK",
            "",
            `Cargando: ${titulo.trim()}`,
        ];
        if (movimientoReducido) { listo(); return; }

        arranque.textContent = "";
        let i = 0;
        const retraso = 520; // espera a que termine la línea de encendido
        setTimeout(function siguiente() {
            if (i < mensajes.length) {
                arranque.textContent += mensajes[i] + "\n";
                i += 1;
                setTimeout(siguiente, i === 4 ? 320 : 150);
            } else {
                arranque.innerHTML = arranque.textContent.replace(/\n$/, "") + '\n<span class="cursor"></span>';
                setTimeout(listo, 420);
            }
        }, retraso);
    }

    function listo() {
        ponerEstado("listo");
        const entrada = document.querySelector("#juego input:not([type=hidden]), #juego textarea");
        if (entrada) entrada.focus({ preventScroll: true });
    }

    // Cuando el reto muestra un resultado, la pantalla baja hasta él.
    const resultado = $("resultado");
    if (resultado && "MutationObserver" in window) {
        new MutationObserver(() => {
            if (resultado.textContent.trim()) resultado.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }).observe(resultado, { childList: true, subtree: true });
    }

    encender();
})();