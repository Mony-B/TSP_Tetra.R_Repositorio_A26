// Clasificar por categorías (CU-08): arrastrar y soltar fichas en las cajas.
// El navegador solo dibuja y manda dónde soltó cada ficha; Django decide si es
// correcto y cuándo se completó el reto (la categoría correcta nunca llega aquí).
(() => {
    const { enunciado, categorias, fichas, grafica, ayuda } = ReCode.reto.datos;
    const raiz = document.getElementById("clasificar");
    const clasificarUrl = raiz.dataset.clasificarUrl;
    const zonasEl = document.getElementById("zonas");
    const bandeja = document.getElementById("bandeja");
    const canvas = document.getElementById("grafica");
    const aviso = document.getElementById("aviso");
    const resultado = document.getElementById("resultado");
    const dialogo = document.getElementById("dialogo-salir");
    const COLORES = ["#1e88e5", "#2e9e44", "#d93a3a", "#c98f00", "#8e44ad", "#00899b"];
    const SEGUNDOS_REDIRECCION = 10;
    const UMBRAL_ARRASTRE = 6; // px; menos que esto se considera un toque

    const colocadas = new Set();   // ids de fichas ya bien clasificadas
    let seleccionada = null;       // ficha elegida con toque / teclado
    let ocupado = false;           // esperando al servidor
    let terminado = false;
    let resaltada = null;          // ficha cuyo punto se destaca en la gráfica
    const elFicha = {};            // id -> botón

    // --- Enunciado y fichas ---------------------------------------------------

    enunciado.forEach((linea) => {
        const d = document.createElement("div");
        d.textContent = linea;
        document.getElementById("enunciado").appendChild(d);
    });
    document.getElementById("total").textContent = fichas.length;

    const zonas = {};
    categorias.forEach((c) => {
        const z = document.createElement("div");
        z.className = `cl-zona ${c.id}`;
        z.dataset.categoria = c.id;
        z.tabIndex = 0;
        z.setAttribute("role", "button");
        z.setAttribute("aria-label", `${c.nombre} ${c.detalle}`);
        const h = document.createElement("h3");
        h.textContent = c.nombre;
        const det = document.createElement("small");
        det.textContent = c.detalle;
        h.appendChild(det);
        const cont = document.createElement("div");
        cont.className = "cl-zona-fichas";
        z.append(h, document.createElement("hr"), cont);
        zonasEl.appendChild(z);
        zonas[c.id] = { el: z, cont };
        z.addEventListener("click", () => soltarSeleccionada(c.id));
        z.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") { e.preventDefault(); soltarSeleccionada(c.id); }
        });
    });

    fichas.forEach((f, i) => {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "cl-ficha";
        b.textContent = `(${f.x}, ${f.y})`;
        b.style.background = COLORES[i % COLORES.length];
        b.dataset.id = f.id;
        bandeja.appendChild(b);
        elFicha[f.id] = b;
        engancharArrastre(b, f);
    });

    // --- Gráfica ----------------------------------------------------------------

    const ctx = canvas.getContext("2d");
    function dibujar() {
        const W = canvas.width, n = grafica.rango * 2, u = W / n;
        const px = (x) => (x + grafica.rango) * u;
        const py = (y) => (grafica.rango - y) * u;
        ctx.setLineDash([]);
        ctx.fillStyle = "#000";
        ctx.fillRect(0, 0, W, W);

        const celda = u / grafica.celdas;           // región solución
        ctx.fillStyle = "rgba(0, 255, 0, 0.22)";
        grafica.sombra.forEach((fila, j) => {
            for (let i = 0; i < fila.length; i++) {
                if (fila[i] === "1") ctx.fillRect(i * celda, j * celda, celda + 0.6, celda + 0.6);
            }
        });

        ctx.lineWidth = 1;                          // cuadrícula, ejes y números
        ctx.font = "9px 'Courier New', monospace";
        ctx.textAlign = "center";
        for (let v = -grafica.rango; v <= grafica.rango; v++) {
            ctx.strokeStyle = v === 0 ? "#00ff00" : "rgba(0, 170, 0, 0.35)";
            ctx.beginPath(); ctx.moveTo(px(v), 0); ctx.lineTo(px(v), W); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, py(v)); ctx.lineTo(W, py(v)); ctx.stroke();
            if (v !== 0 && v % 2 === 0) {
                ctx.fillStyle = "#9f9";
                ctx.fillText(v, px(v), py(0) + 11);
                ctx.fillText(v, px(0) - 9, py(v) + 3);
            }
        }

        ctx.lineWidth = 2;                          // fronteras de la(s) desigualdad(es)
        ctx.strokeStyle = "#00bfff";
        grafica.curvas.forEach((c) => {
            ctx.setLineDash(c.solida ? [] : [6, 4]);
            c.tramos.forEach((t) => {
                ctx.beginPath();
                t.forEach(([x, y], i) => (i ? ctx.lineTo(px(x), py(y)) : ctx.moveTo(px(x), py(y))));
                ctx.stroke();
            });
        });
        ctx.setLineDash([]);

        fichas.forEach((f, i) => {                  // puntos que aún no se clasifican
            if (colocadas.has(f.id)) return;
            ctx.beginPath();
            ctx.arc(px(f.x), py(f.y), f.id === resaltada ? 8 : 5, 0, Math.PI * 2);
            ctx.fillStyle = COLORES[i % COLORES.length];
            ctx.fill();
            ctx.strokeStyle = "#fff";
            ctx.lineWidth = 1.5;
            ctx.stroke();
        });
    }

    function resaltar(id) { resaltada = id; dibujar(); }

    // --- Arrastrar y soltar (ratón y táctil con Pointer Events) ------------------

    function zonaBajo(x, y) {
        const el = document.elementFromPoint(x, y);
        const z = el && el.closest(".cl-zona");
        return z ? z.dataset.categoria : null;
    }

    function engancharArrastre(boton, ficha) {
        let inicio = null, fantasma = null, arrastrado = false;

        boton.addEventListener("pointerdown", (e) => {
            if (terminado || ocupado || colocadas.has(ficha.id) || (e.button && e.button !== 0)) return;
            inicio = { x: e.clientX, y: e.clientY };
            arrastrado = false;
            boton.setPointerCapture(e.pointerId);
            resaltar(ficha.id);
        });

        boton.addEventListener("pointermove", (e) => {
            if (!inicio) return;
            if (!arrastrado && Math.hypot(e.clientX - inicio.x, e.clientY - inicio.y) < UMBRAL_ARRASTRE) return;
            if (!arrastrado) {
                arrastrado = true;
                fantasma = boton.cloneNode(true);
                fantasma.classList.add("arrastrando");
                fantasma.style.width = `${boton.offsetWidth}px`;
                document.body.appendChild(fantasma);
                boton.classList.add("fantasma");
            }
            fantasma.style.left = `${e.clientX - fantasma.offsetWidth / 2}px`;
            fantasma.style.top = `${e.clientY - fantasma.offsetHeight / 2}px`;
            const z = zonaBajo(e.clientX, e.clientY);
            Object.entries(zonas).forEach(([id, o]) => o.el.classList.toggle("encima", id === z));
        });

        function terminar(e, cancelado) {
            if (!inicio) return;
            const huboArrastre = arrastrado;
            inicio = null; arrastrado = false;
            if (boton.hasPointerCapture(e.pointerId)) boton.releasePointerCapture(e.pointerId);
            if (fantasma) { fantasma.remove(); fantasma = null; }
            boton.classList.remove("fantasma");
            Object.values(zonas).forEach((o) => o.el.classList.remove("encima"));
            if (!huboArrastre) return;                       // fue un toque: lo maneja "click"
            boton.dataset.sinClick = "1";                    // evita contarlo también como toque
            setTimeout(() => delete boton.dataset.sinClick, 0);
            const z = cancelado ? null : zonaBajo(e.clientX, e.clientY);
            resaltar(null);
            if (z) enviar(ficha, z);
        }
        boton.addEventListener("pointerup", (e) => terminar(e, false));
        boton.addEventListener("pointercancel", (e) => terminar(e, true));

        // Toque o teclado: elegir la ficha y luego tocar una caja.
        boton.addEventListener("click", () => {
            if (boton.dataset.sinClick || terminado || ocupado || colocadas.has(ficha.id)) return;
            seleccionar(seleccionada === ficha.id ? null : ficha.id);
        });
    }

    function seleccionar(id) {
        seleccionada = id;
        Object.entries(elFicha).forEach(([fid, b]) => b.classList.toggle("seleccionada", fid === id));
        resaltar(id);
        if (id) mostrar("Ahora toca la caja donde crees que va esta ficha.");
    }

    function soltarSeleccionada(categoria) {
        if (!seleccionada || terminado || ocupado) return;
        const ficha = fichas.find((f) => f.id === seleccionada);
        seleccionar(null);
        enviar(ficha, categoria);
    }

    // --- Clasificar (pasos 4-6, FA-1) ---------------------------------------------

    function mostrar(texto, tipo = "") {
        aviso.textContent = texto;
        aviso.className = `cl-mensaje etiqueta ${tipo}`;
    }

    function progreso(puntos) {
        document.getElementById("puntos").textContent = puntos;
        const pct = Math.round((puntos / fichas.length) * 100);
        document.getElementById("progreso-relleno").style.width = `${pct}%`;
        document.getElementById("progreso").setAttribute("aria-valuenow", pct);
    }

    async function enviar(ficha, categoria) {
        if (ocupado || terminado || colocadas.has(ficha.id)) return;
        ocupado = true;
        const boton = elFicha[ficha.id];
        try {
            const r = await ReCode.postJSON(clasificarUrl, { ficha: ficha.id, categoria });
            if (r.correcto) {                                  // el sistema acopla la ficha
                colocadas.add(ficha.id);
                boton.classList.add("colocada");
                boton.disabled = true;
                zonas[categoria].cont.appendChild(boton);
                progreso(r.puntos);
                mostrar("¡Correcto!", "bien");
                dibujar();
                if (r.puntos >= r.total) await completar();
            } else {                                           // FA-1: fallo y la ficha regresa
                boton.classList.remove("fallo");
                void boton.offsetWidth;                        // reinicia la animación
                boton.classList.add("fallo");
                zonas[categoria].el.classList.remove("error");
                void zonas[categoria].el.offsetWidth;
                zonas[categoria].el.classList.add("error");
                mostrar("Incorrecto: esa ficha no va ahí. Inténtalo de nuevo.", "error");
            }
        } catch (err) {
            mostrar(err.message, "error");
        } finally {
            ocupado = false;
        }
    }

    // --- Victoria (pasos 7-9) -----------------------------------------------------

    function escapar(texto) {
        const d = document.createElement("div");
        d.textContent = texto;
        return d.innerHTML;
    }

    async function completar() {
        const r = await ReCode.postJSON(ReCode.reto.revisarUrl, {});
        const saldo = document.getElementById("bitcoins-alumno");
        if (saldo) saldo.textContent = r.bitcoins_total;
        terminado = true;
        document.querySelector(".cl-pie").hidden = true;
        aviso.hidden = true;
        const premio = r.ya_otorgado
            ? "La recompensa de este reto ya se te había otorgado antes."
            : `Obtuviste <strong>₿ ${r.bitcoins_otorgados}</strong>.`;
        resultado.innerHTML = `
            <div class="mensaje">
                <p><strong>${escapar(r.mensaje)}</strong> Clasificaste todas las fichas.</p>
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

    // --- Ayuda, reiniciar y FE-1 (salir / rendirse) ---------------------------------

    document.getElementById("btn-ayuda").addEventListener("click", () => {
        const a = document.getElementById("ayuda");
        a.textContent = ayuda;
        a.hidden = !a.hidden;
    });
    // jugar() siempre reinicia la partida en el servidor, así que recargar basta.
    document.getElementById("btn-reiniciar").addEventListener("click", () => window.location.reload());

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
    document.getElementById("btn-cancelar-salida").addEventListener("click", () => dialogo.close());
    document.getElementById("btn-confirmar-salida").addEventListener("click", () => {
        window.location.href = ReCode.reto.volverUrl; // no se guarda nada ni se dan bitcoins
    });

    dibujar();
})();