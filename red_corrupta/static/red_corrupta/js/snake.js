// Snake: el único minijuego de hackeo de la red corrupta (CU03, FA-1).
// Mecánica fija (clásico: comer, crecer, no chocar); el nivel (cuántos
// datos hay que comer para ganar) varía entre partidas, como pide el
// requisito especial 4. No manda nada al servidor mientras se juega: el
// navegador decide solo cuándo se gana o se pierde (igual que decide
// solo el movimiento dentro del laberinto de sombras); quien llama a
// Snake.iniciar() es responsable de avisar al servidor si hay victoria.
window.Snake = (() => {
    "use strict";
    const COLS = 20, ROWS = 20;
    const NIVELES = [
        { meta: 6, velocidad: 150 },
        { meta: 9, velocidad: 130 },
        { meta: 12, velocidad: 110 },
    ];

    let canvas, ctx, celda;
    let serpiente, direccion, siguienteDireccion, comida, comidos, nivel;
    let temporizador = null;
    let callbacks = {};
    let activo = false;

    function celdaLibre() {
        let c;
        do {
            c = { x: Math.floor(Math.random() * COLS), y: Math.floor(Math.random() * ROWS) };
        } while (serpiente.some((s) => s.x === c.x && s.y === c.y));
        return c;
    }

    function reiniciarEstado() {
        serpiente = [{ x: 9, y: 10 }, { x: 8, y: 10 }, { x: 7, y: 10 }];
        direccion = { x: 1, y: 0 };
        siguienteDireccion = direccion;
        comidos = 0;
        comida = celdaLibre();
    }

    function paso() {
        direccion = siguienteDireccion;
        const cabeza = { x: serpiente[0].x + direccion.x, y: serpiente[0].y + direccion.y };

        const chocoPared = cabeza.x < 0 || cabeza.x >= COLS || cabeza.y < 0 || cabeza.y >= ROWS;
        const chocoCuerpo = serpiente.some((s) => s.x === cabeza.x && s.y === cabeza.y);
        if (chocoPared || chocoCuerpo) {
            terminar(false);
            return;
        }

        serpiente.unshift(cabeza);
        if (cabeza.x === comida.x && cabeza.y === comida.y) {
            comidos += 1;
            if (callbacks.onProgreso) callbacks.onProgreso(comidos, NIVELES[nivel].meta);
            if (comidos >= NIVELES[nivel].meta) {
                terminar(true);
                return;
            }
            comida = celdaLibre();
        } else {
            serpiente.pop();
        }
        dibujar();
    }

    function dibujar() {
        ctx.fillStyle = "#060509";
        ctx.fillRect(0, 0, COLS * celda, ROWS * celda);

        ctx.fillStyle = "#ff2fb0";
        ctx.shadowColor = "#ff2fb0";
        ctx.shadowBlur = 6;
        ctx.fillRect(comida.x * celda + 2, comida.y * celda + 2, celda - 4, celda - 4);
        ctx.shadowBlur = 0;

        serpiente.forEach((s, i) => {
            ctx.fillStyle = i === 0 ? "#19ffb4" : "rgba(25,255,180,0.75)";
            ctx.fillRect(s.x * celda + 1, s.y * celda + 1, celda - 2, celda - 2);
        });
    }

    function terminar(gano) {
        detenerTemporizador();
        activo = false;
        if (gano && callbacks.onVictoria) callbacks.onVictoria();
        else if (!gano && callbacks.onDerrota) callbacks.onDerrota();
    }

    function detenerTemporizador() {
        if (temporizador) clearInterval(temporizador);
        temporizador = null;
    }

    function cambiarDireccion(dx, dy) {
        if (!activo) return;
        // No se puede invertir sobre el propio cuerpo en el mismo instante.
        if (direccion.x === -dx && direccion.y === -dy) return;
        siguienteDireccion = { x: dx, y: dy };
    }

    function manejarTecla(e) {
        const mapa = {
            ArrowUp: [0, -1], ArrowDown: [0, 1], ArrowLeft: [-1, 0], ArrowRight: [1, 0],
            w: [0, -1], s: [0, 1], a: [-1, 0], d: [1, 0],
        };
        const dir = mapa[e.key];
        if (dir) { e.preventDefault(); cambiarDireccion(dir[0], dir[1]); }
    }

    let toqueInicio = null;
    function manejarToqueInicio(e) {
        const t = e.touches[0];
        toqueInicio = { x: t.clientX, y: t.clientY };
    }
    function manejarToqueFin(e) {
        if (!toqueInicio) return;
        const t = e.changedTouches[0];
        const dx = t.clientX - toqueInicio.x, dy = t.clientY - toqueInicio.y;
        if (Math.abs(dx) > Math.abs(dy)) cambiarDireccion(dx > 0 ? 1 : -1, 0);
        else if (Math.abs(dy) > 10 || Math.abs(dx) > 10) cambiarDireccion(0, dy > 0 ? 1 : -1);
        toqueInicio = null;
    }

    function iniciar(lienzo, cbs) {
        canvas = lienzo;
        ctx = canvas.getContext("2d");
        celda = canvas.width / COLS;
        callbacks = cbs || {};
        nivel = Math.floor(Math.random() * NIVELES.length);
        reiniciarEstado();
        dibujar();
        activo = true;
        detenerTemporizador();
        temporizador = setInterval(paso, NIVELES[nivel].velocidad);

        document.addEventListener("keydown", manejarTecla);
        canvas.addEventListener("touchstart", manejarToqueInicio, { passive: true });
        canvas.addEventListener("touchend", manejarToqueFin, { passive: true });

        return { nivel: nivel + 1, meta: NIVELES[nivel].meta };
    }

    function detener() {
        activo = false;
        detenerTemporizador();
        document.removeEventListener("keydown", manejarTecla);
        if (canvas) {
            canvas.removeEventListener("touchstart", manejarToqueInicio);
            canvas.removeEventListener("touchend", manejarToqueFin);
        }
    }

    return { iniciar, detener };
})();
