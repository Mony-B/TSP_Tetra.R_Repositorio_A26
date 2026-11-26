// Relacionar conceptos (CU-13).
// Girar los carretes es solo del navegador; "Probar combinación" es lo
// único que llega al servidor, que decide si la combinación alineada es
// válida y no estaba resuelta en la ronda.
(() => {
    const { rondas, total_rondas: totalRondas } = ReCode.reto.datos;
    const resultado = document.getElementById("resultado");
    const acciones = document.getElementById("acciones-conceptos");
    const dialogoExito = document.getElementById("dialogo-exito");

    let ronda = 0;
    let idx = [0, 0, 0];
    let resueltas = 0;
    let bloqueado = false;

    function columnas() {
        const r = rondas[ronda];
        return [r.conceptos, r.palabras, r.definiciones];
    }

    function pintarValor(carrete) {
        const col = columnas()[carrete];
        document.getElementById(`valor-${carrete}`).innerHTML = `<span>${ReCode.dialogos.escaparHTML(col[idx[carrete]])}</span>`;
    }

    function pintarCarretes() {
        [0, 1, 2].forEach(pintarValor);
        document.getElementById("ronda-num").textContent = ronda + 1;
        pintarPistas();
    }

    // Reinicia la animación del carrete que se acaba de girar (si se gira
    // rápido varias veces seguidas, fuerza el reflow para que no se quede
    // a medias).
    function animarCarrete(carrete) {
        const el = document.getElementById(`valor-${carrete}`);
        el.classList.remove("girando");
        void el.offsetWidth;
        el.classList.add("girando");
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
        pintarValor(carrete);
        animarCarrete(carrete);
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
            document.getElementById("exito-mensaje").innerHTML = "<strong>¡Reto completado!</strong>";
            document.getElementById("exito-premio").innerHTML = premio;
            ReCode.dialogos.abrir(dialogoExito);
            return;
        }

        if (r.siguiente_ronda !== undefined) {
            ronda = r.siguiente_ronda;
            idx = [0, 0, 0];
            resueltas = 0;
            pintarCarretes();
            [0, 1, 2].forEach(animarCarrete);
            mensaje(`Ronda ${ronda} superada. Avanzaste a la ronda ${ronda + 1}.`);
            return;
        }

        mensaje("Combinación correcta. Sigue girando para encontrar las que faltan.");
    }

    document.querySelectorAll(".flecha").forEach((b) => {
        b.addEventListener("click", () => girar(Number(b.dataset.carrete), Number(b.dataset.dir)));
    });
    document.getElementById("btn-probar").addEventListener("click", probar);

    ReCode.dialogos.inicializarSalir({
        hayProgreso: () => ronda > 0 || resueltas > 0,
        puedeSalir: () => !bloqueado,
    });

    pintarCarretes();
})();
