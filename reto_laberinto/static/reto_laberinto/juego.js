// Laberinto de sombras (CU-14).
// El movimiento y el dibujo del laberinto (con niebla alrededor del
// personaje) son enteramente del navegador, igual que en el prototipo
// validado. Lo único que llega al servidor es la respuesta que el
// personaje toca al chocar con una pared-respuesta: el servidor decide si
// es correcta, nunca el navegador.
(() => {
    "use strict";
    const raiz = document.getElementById("laberinto");
    const revisarUrl = raiz.dataset.revisarUrl;
    const canvas = document.getElementById("lienzo");
    const ctx = canvas.getContext("2d");
    const progreso = document.getElementById("progreso");
    const preguntaEl = document.getElementById("pregunta");
    const toast = document.getElementById("toast");
    const acciones = document.getElementById("acciones-laberinto");
    const dialogo = document.getElementById("dialogo-salir");
    const dialogoExito = document.getElementById("dialogo-exito");

    // Laberinto más pequeño y con más atajos que el prototipo original
    // (21×17, 12 enlaces extra): ese tamaño resultaba abrumador para
    // explorar. Con menos celdas y más enlaces, los pasillos son más
    // cortos y hay más rutas alternativas visibles sin perder el efecto
    // de laberinto en penumbra.
    // El lienzo (ver reto.html) mide exactamente W*T × H*T: así el grid
    // cubre el lienzo completo (y por lo tanto el marco de .escenario,
    // que lo escala con width:100%) sin dejar franjas vacías alrededor;
    // no hace falta ningún margen (OX/OY) porque no sobra espacio que
    // repartir.
    const W = 15, H = 11, T = 40, OX = 0, OY = 0;

    let actual = ReCode.reto.datos; // {numero, total, pregunta, opciones}
    let grid = [], player = { x: 1, y: 1 }, exits = [];
    let visited = new Set(), moving = false, finished = false, flash = 0;
    let toastTimer = null;
    const key = (x, y) => y * W + x;
    const rand = (n) => Math.floor(Math.random() * n);

    function makeMaze() {
        grid = Array.from({ length: H }, () => Array(W).fill(1));
        let stack = [[1, 1]];
        grid[1][1] = 0;
        while (stack.length) {
            const [x, y] = stack[stack.length - 1];
            const dirs = [[2, 0], [-2, 0], [0, 2], [0, -2]].sort(() => Math.random() - 0.5);
            let found = false;
            for (const [dx, dy] of dirs) {
                const nx = x + dx, ny = y + dy;
                if (nx > 0 && nx < W - 1 && ny > 0 && ny < H - 1 && grid[ny][nx]) {
                    grid[y + dy / 2][x + dx / 2] = 0;
                    grid[ny][nx] = 0;
                    stack.push([nx, ny]);
                    found = true;
                    break;
                }
            }
            if (!found) stack.pop();
        }
        // Enlaces extra para dar rutas alternativas sin perder el laberinto
        // (más que el original: con el grid más chico, hacen falta más
        // atajos proporcionalmente para que se sienta menos denso).
        for (let i = 0; i < 40; i++) {
            const x = 2 + rand(W - 4), y = 2 + rand(H - 4);
            if (grid[y][x] === 1 && ((grid[y][x - 1] === 0 && grid[y][x + 1] === 0) || (grid[y - 1][x] === 0 && grid[y + 1][x] === 0))) {
                grid[y][x] = 0;
            }
        }
        player = { x: 1, y: 1 };
        const distancias = Array.from({ length: H }, () => Array(W).fill(-1));
        const cola = [[1, 1]];
        distancias[1][1] = 0;
        for (let i = 0; i < cola.length; i++) {
            const [x, y] = cola[i];
            for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
                const nx = x + dx, ny = y + dy;
                if (nx >= 0 && ny >= 0 && nx < W && ny < H && !grid[ny][nx] && distancias[ny][nx] < 0) {
                    distancias[ny][nx] = distancias[y][x] + 1;
                    cola.push([nx, ny]);
                }
            }
        }
        // Umbral de distancia más bajo que el original (10): con el grid
        // más chico, pocas celdas quedarían a esa distancia del inicio.
        const lados = [[], [], [], []];
        for (let y = 1; y < H - 1; y += 2) {
            if (distancias[y][1] > 6) lados[0].push({ x: 1, y, lado: 0, d: distancias[y][1] });
            if (distancias[y][W - 2] > 6) lados[1].push({ x: W - 2, y, lado: 1, d: distancias[y][W - 2] });
        }
        for (let x = 1; x < W - 1; x += 2) {
            if (distancias[1][x] > 6) lados[2].push({ x, y: 1, lado: 2, d: distancias[1][x] });
            if (distancias[H - 2][x] > 6) lados[3].push({ x, y: H - 2, lado: 3, d: distancias[H - 2][x] });
        }
        for (const l of lados) l.sort((a, b) => b.d - a.d);
        let elegidos = [];
        const orden = [0, 1, 2, 3].sort(() => Math.random() - 0.5);
        for (const lado of orden) {
            const c = lados[lado].find((p) => !elegidos.some((z) => Math.abs(z.x - p.x) + Math.abs(z.y - p.y) < 7));
            if (c) elegidos.push(c);
            if (elegidos.length === 3) break;
        }
        if (elegidos.length < 3) {
            const todos = lados.flat().sort((a, b) => b.d - a.d);
            for (const c of todos) {
                if (!elegidos.some((z) => Math.abs(z.x - c.x) + Math.abs(z.y - c.y) < 6)) elegidos.push(c);
                if (elegidos.length === 3) break;
            }
        }
        const opciones = [...actual.opciones].sort(() => Math.random() - 0.5);
        exits = elegidos.slice(0, 3).map((p, i) => ({
            ...p,
            wallX: p.lado === 0 ? 0 : p.lado === 1 ? W - 1 : p.x,
            wallY: p.lado === 2 ? 0 : p.lado === 3 ? H - 1 : p.y,
            label: opciones[i],
        }));
        visited = new Set([key(1, 1)]);
        flash = 0;
    }

    function actualizarCabecera() {
        progreso.textContent = finished
            ? "ESCAPASTE DEL LABERINTO"
            : `SECTOR ${String(actual.numero).padStart(2, "0")} / ${String(actual.total).padStart(2, "0")}`;
        preguntaEl.textContent = finished ? "Has encontrado la salida." : actual.pregunta;
    }

    function decir(mensaje, ms = 1900) {
        toast.textContent = mensaje;
        toast.classList.add("mostrar");
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => toast.classList.remove("mostrar"), ms);
    }

    function iniciar() {
        finished = false;
        moving = false;
        makeMaze();
        actualizarCabecera();
        decir("Busca las tres salidas. Solo una abre el siguiente sector.", 2600);
    }

    async function step(dx, dy) {
        if (finished || moving || dialogo.open) return;
        const nx = player.x + dx, ny = player.y + dy;
        if (nx < 0 || nx >= W || ny < 0 || ny >= H) return;
        const encontrado = exits.find((e) => e.wallX === nx && e.wallY === ny && player.x === e.x && player.y === e.y);
        if (!encontrado && grid[ny][nx]) return;
        if (!encontrado) {
            player.x = nx; player.y = ny;
            visited.add(key(nx, ny));
            return;
        }
        moving = true;
        let r;
        try {
            r = await ReCode.postJSON(revisarUrl, { respuesta: encontrado.label });
        } catch (err) {
            decir(err.message, 2200);
            moving = false;
            return;
        }
        const saldo = document.getElementById("bitcoins-alumno");
        if (saldo) saldo.textContent = r.bitcoins_total;

        if (r.correcto) {
            flash = 1;
            // El mensaje de acierto duraba 1200ms pero el siguiente paso
            // llegaba a los 900ms y lo tapaba a la mitad; ahora se espera
            // a que termine de verse antes de mostrar el siguiente aviso.
            decir("✓ " + r.mensaje, 1200);
            setTimeout(() => {
                if (r.siguiente) {
                    actual = r.siguiente;
                    makeMaze();
                    actualizarCabecera();
                    decir(`Nuevo sector desbloqueado. Explora sus caminos.`, 2000);
                    moving = false;
                } else {
                    finished = true;
                    actualizarCabecera();
                    terminarConExito(r);
                }
            }, 1300);
        } else {
            flash = -1;
            decir("✕ " + r.mensaje, 1500);
            setTimeout(() => {
                player = { x: 1, y: 1 };
                visited = new Set([key(1, 1)]);
                moving = false;
            }, 1100);
        }
    }

    function terminarConExito(r) {
        const premio = r.ya_otorgado
            ? "La recompensa de este reto ya se te había otorgado antes."
            : `Obtuviste <strong>₿ ${r.bitcoins_otorgados}</strong>.`;
        acciones.hidden = true;
        document.getElementById("exito-mensaje").innerHTML = "<strong>¡Has escapado del laberinto!</strong>";
        document.getElementById("exito-premio").innerHTML = premio;
        ReCode.dialogos.abrir(dialogoExito);
    }

    ReCode.dialogos.inicializarSalir({
        hayProgreso: () => visited.size > 1,
        puedeSalir: () => !finished,
    });

    // --- Controles -----------------------------------------------------------

    // Controles más ágiles que el prototipo (85ms/135ms): el requisito
    // (R64) solo pide poder mover al personaje, no fija una velocidad,
    // así que se acorta la espera entre pasos para que se sienta más
    // responsivo sin cambiar la mecánica.
    let lastMove = 0;
    document.addEventListener("keydown", (e) => {
        if (dialogo.open) return;
        const dir = { ArrowUp: [0, -1], ArrowDown: [0, 1], ArrowLeft: [-1, 0], ArrowRight: [1, 0], w: [0, -1], s: [0, 1], a: [-1, 0], d: [1, 0] }[e.key];
        if (dir) {
            e.preventDefault();
            if (performance.now() - lastMove > 55) { step(...dir); lastMove = performance.now(); }
        }
    });
    let hold = null;
    document.querySelectorAll(".dpad button").forEach((b) => {
        const dx = Number(b.dataset.dx), dy = Number(b.dataset.dy);
        b.addEventListener("pointerdown", (e) => {
            e.preventDefault();
            step(dx, dy);
            clearInterval(hold);
            hold = setInterval(() => step(dx, dy), 90);
        });
        ["pointerup", "pointercancel", "pointerleave"].forEach((ev) => b.addEventListener(ev, () => clearInterval(hold)));
    });

    // --- Dibujo ---------------------------------------------------------------

    function render() {
        ctx.fillStyle = "#02060c";
        ctx.fillRect(0, 0, W * T, H * T);
        ctx.save();
        ctx.translate(OX, OY);
        const px = player.x * T + T / 2, py = player.y * T + T / 2;
        for (let y = 0; y < H; y++) {
            for (let x = 0; x < W; x++) {
                const cx = x * T + T / 2, cy = y * T + T / 2;
                const dist = Math.hypot(cx - px, cy - py);
                const light = Math.max(0, 1 - dist / (T * 5.5));
                const conocido = visited.has(key(x, y));
                if (dist > T * 6 && !conocido) continue;
                if (grid[y][x]) {
                    ctx.fillStyle = `rgba(8,20,34,${0.24 + light * 0.65})`;
                    ctx.fillRect(x * T, y * T, T, T);
                    if (light > 0.025) {
                        ctx.strokeStyle = `rgba(89,199,255,${0.1 + light * 0.8})`;
                        ctx.shadowColor = "#59c7ff"; ctx.shadowBlur = light * 16; ctx.lineWidth = 1.8;
                        ctx.strokeRect(x * T + 2, y * T + 2, T - 4, T - 4);
                        ctx.shadowBlur = 0;
                    }
                } else {
                    ctx.fillStyle = `rgba(12,27,45,${0.18 + light * 0.6})`;
                    ctx.fillRect(x * T, y * T, T, T);
                    if (conocido) {
                        ctx.fillStyle = `rgba(89,199,255,${light * 0.16})`;
                        ctx.fillRect(x * T + T / 2 - 2, y * T + T / 2 - 2, 4, 4);
                    }
                }
            }
        }
        for (const e of exits) {
            const cx = e.wallX * T + T / 2, cy = e.wallY * T + T / 2;
            const dist = Math.hypot(cx - px, cy - py);
            const a = Math.max(0, 1 - dist / (T * 6));
            if (a <= 0) continue;
            ctx.save();
            ctx.shadowColor = "#59c7ff"; ctx.shadowBlur = 20 * a;
            ctx.strokeStyle = `rgba(89,199,255,${a})`; ctx.lineWidth = 3;
            ctx.strokeRect(e.wallX * T + 3, e.wallY * T + 3, T - 6, T - 6);
            ctx.fillStyle = `rgba(89,199,255,${0.25 * a})`;
            ctx.fillRect(e.wallX * T + 5, e.wallY * T + 5, T - 10, T - 10);
            ctx.restore();
            ctx.font = "bold 12px monospace";
            const texto = e.label;
            const tw = ctx.measureText(texto).width + 18;
            let lx, ly;
            if (e.lado === 0) { lx = 4; ly = cy - 11; }
            else if (e.lado === 1) { lx = W * T - tw - 4; ly = cy - 11; }
            else if (e.lado === 2) { lx = cx - tw / 2; ly = 4; }
            else { lx = cx - tw / 2; ly = H * T - 25; }
            lx = Math.min(W * T - tw, Math.max(0, lx));
            ctx.fillStyle = `rgba(9,20,35,${0.98 * a})`;
            ctx.fillRect(lx, ly, tw, 21);
            ctx.strokeStyle = `rgba(89,199,255,${a})`;
            ctx.strokeRect(lx, ly, tw, 21);
            ctx.fillStyle = `rgba(232,246,255,${a})`;
            ctx.fillText(texto, lx + 9, ly + 15);
        }
        const halo = ctx.createRadialGradient(px, py, 2, px, py, T * 4.8);
        halo.addColorStop(0, "rgba(89,199,255,.20)");
        halo.addColorStop(1, "rgba(89,199,255,0)");
        ctx.fillStyle = halo;
        ctx.beginPath(); ctx.arc(px, py, T * 4.8, 0, Math.PI * 2); ctx.fill();
        ctx.shadowColor = "#59c7ff"; ctx.shadowBlur = 15;
        ctx.fillStyle = "#223c5b"; ctx.fillRect(px - 9, py + 1, 18, 12);
        ctx.fillStyle = "#ffd7ae"; ctx.fillRect(px - 7, py - 10, 14, 13);
        ctx.fillStyle = "#17233c"; ctx.fillRect(px - 9, py - 13, 18, 6); ctx.fillRect(px - 9, py - 9, 4, 6);
        ctx.fillStyle = "#09202c"; ctx.fillRect(px - 5, py - 4, 3, 3); ctx.fillRect(px + 3, py - 4, 3, 3);
        ctx.fillStyle = "#ff527e"; ctx.fillRect(px - 2, py + 5, 4, 4);
        ctx.fillStyle = "#15203b"; ctx.fillRect(px - 8, py + 13, 6, 5); ctx.fillRect(px + 2, py + 13, 6, 5);
        ctx.shadowBlur = 0;
        const fog = ctx.createRadialGradient(px, py, T * 0.7, px, py, T * 6.1);
        fog.addColorStop(0, "rgba(0,0,0,0)");
        fog.addColorStop(0.45, "rgba(0,0,0,.08)");
        fog.addColorStop(0.82, "rgba(0,0,0,.87)");
        fog.addColorStop(1, "rgba(0,0,0,.99)");
        ctx.fillStyle = fog;
        ctx.fillRect(0, 0, W * T, H * T);
        ctx.restore();
        if (flash !== 0) {
            ctx.fillStyle = flash > 0 ? "rgba(89,199,255,.18)" : "rgba(255,30,60,.2)";
            ctx.fillRect(0, 0, W * T, H * T);
            flash *= 0.85;
            if (Math.abs(flash) < 0.02) flash = 0;
        }
        if (finished) {
            ctx.fillStyle = "#59c7ff"; ctx.textAlign = "center"; ctx.font = "bold 32px monospace";
            ctx.shadowColor = "#59c7ff"; ctx.shadowBlur = 20;
            ctx.fillText("✦ SALIDA ENCONTRADA ✦", (W * T) / 2, (H * T) / 2);
            ctx.textAlign = "left"; ctx.shadowBlur = 0;
        }
        requestAnimationFrame(render);
    }

    iniciar();
    render();
})();
