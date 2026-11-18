// Relacionar conceptos (CU-13).
// Girar los carretes es solo del navegador; "Probar combinación" es lo
// único que llega al servidor, que decide si la combinación alineada es
// válida y no estaba resuelta en la ronda.
(() => {
    const { rondas, total_rondas: totalRondas } = ReCode.reto.datos;
    const resultado = document.getElementById("resultado");
    const acciones = document.getElementById("acciones-conceptos");
    const dialogo = document.getElementById("dialogo-salir");
    const dialogoExito = document.getElementById("dialogo-exito");

    let ronda = 0;
    let idx = [0, 0, 0];
    let resueltas = 0;
    let bloqueado = false;

    function columnas() {
        const r = rondas[ronda];
        return [r.conceptos, r.palabras, r.definiciones];
    }

    function pintarCarretes() {
        const cols = columnas();
        cols.forEach((col, i) => {
            document.getElementById(`valor-${i}`).textContent = col[idx[i]];
        });
        document.getElementById("ronda-num").textContent = ronda + 1;
        pintarPistas();
    }

    function pintarPistas() {
        const total = rondas[ronda].total;
        const caja = document.getElementById("combo-pista");
        caja.innerHTML = "";
        for (let i = 0; i < total; i++) {
            const span = document.createElement("span");
            span.className = "punto" + (i < resueltas ? " hecho" : "");
            caja.appendChild(span);
        }
    }

    function girar(carrete, dir) {
        if (bloqueado) return;
        const col = columnas()[carrete];
        idx[carrete] = (idx[carrete] + dir + col.length) % col.length;
        pintarCarretes();
    }

    function mensaje(html, error = false) {
        resultado.innerHTML = `<p class="mensaje ${error ? "error" : ""}">${html}</p>`;
    }

    async function probar() {
        if (bloqueado) return;
        const cols = columnas();
        const valores = { concepto: cols[0][idx[0]], palabra: cols[1][idx[1]], definicion: cols[2][idx[2]] };
        let r;
        try {
            r = await ReCode.postJSON(ReCode.reto.revisarUrl, valores);
        } catch (err) {
            mensaje(err.message, true);
            return;
        }

        if (!r.correcto) {
            mensaje(
                r.ya_resuelta
                    ? "Esa combinación ya estaba resuelta en esta ronda."
                    : "No forma una combinación válida todavía. El progreso no cambia.",
                true,
            );
            return;
        }

        resueltas = r.resueltas;
        pintarPistas();

        if (r.bitcoins_total !== undefined) {
            // Reto completado (última ronda).
            bloqueado = true;
            const saldo = document.getElementById("bitcoins-alumno");
            if (saldo) saldo.textContent = r.bitcoins_total;
            const premio = r.ya_otorgado
                ? "Ya habías completado el reto, por lo que no se otorgan bitcoins de nuevo."
                : `Ganaste <strong>₿ ${r.bitcoins_otorgados}</strong>.`;
            acciones.hidden = true;
            document.getElementById("exito-premio").innerHTML = `<strong>¡Reto completado!</strong> ${premio}`;
            ReCode.dialogos.abrir(dialogoExito);
            return;
        }

        if (r.siguiente_ronda !== undefined) {
            ronda = r.siguiente_ronda;
            idx = [0, 0, 0];
            resueltas = 0;
            pintarCarretes();
            mensaje(`Ronda ${ronda} superada. Avanzaste a la ronda ${ronda + 1}.`);
            return;
        }

        mensaje("Combinación correcta. Sigue girando para encontrar las que faltan.");
    }

    // --- FE-1: salir / rendirse con confirmación ----------------------------
    const MENSAJE_SALIR = "Se perderá el progreso de esta ronda y no obtendrás bitcoins. ¿Salir?";
    function pedirSalida(e) {
        if (bloqueado) return;
        ReCode.dialogos.pedirSalida(dialogo, MENSAJE_SALIR, ReCode.reto.volverUrl, e);
    }

    document.querySelectorAll(".flecha").forEach((b) => {
        b.addEventListener("click", () => girar(Number(b.dataset.carrete), Number(b.dataset.dir)));
    });
    document.getElementById("btn-probar").addEventListener("click", probar);
    document.getElementById("btn-salir").addEventListener("click", pedirSalida);
    ReCode.dialogos.conectarFlechaSalir(dialogo, MENSAJE_SALIR, ReCode.reto.volverUrl, () => (ronda > 0 || resueltas > 0) && !bloqueado);
    document.getElementById("btn-cancelar-salida").addEventListener("click", () => ReCode.dialogos.cerrar(dialogo));
    document.getElementById("btn-confirmar-salida").addEventListener("click", () => {
        window.location.href = ReCode.reto.volverUrl;
    });

    pintarCarretes();
})();
