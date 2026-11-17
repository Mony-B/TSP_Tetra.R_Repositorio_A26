// Tiro parabólico (CU-12).
// El ángulo y la fuerza se mandan al servidor, que calcula la trayectoria
// real (y si acierta) y regresa los coeficientes y(x) = b·x − a·x² junto
// con el alcance; el navegador solo los usa para animar el disparo.
(() => {
    const datos = ReCode.reto.datos;
    const raiz = document.getElementById("parabolica");
    const disparoUrl = raiz.dataset.disparoUrl;
    const reintentarUrl = raiz.dataset.reintentarUrl;
    const lienzo = document.getElementById("lienzo");
    const ctx = lienzo.getContext("2d");
    const W = lienzo.width, H = lienzo.height;
    const GROUND = H - 30;
    const LAUNCH_X = W * 0.08;

    const anguloInput = document.getElementById("angulo");
    const fuerzaInput = document.getElementById("fuerza");
    const resultado = document.getElementById("resultado");
    const accionesNormal = document.getElementById("acciones-parabolica");
    const accionesAgotado = document.getElementById("acciones-agotado");
    const btnDisparar = document.getElementById("btn-disparar");
    const dialogo = document.getElementById("dialogo-salir");

    let intentosRestantes = datos.intentos_restantes;
    let intentosUsados = datos.intentos - intentosRestantes;
    let disparando = false;
    let terminado = false;

    anguloInput.min = datos.angulo_min; anguloInput.max = datos.angulo_max;
    anguloInput.value = Math.round((datos.angulo_min + datos.angulo_max) / 2);
    fuerzaInput.min = datos.fuerza_min; fuerzaInput.max = datos.fuerza_max;
    fuerzaInput.value = Math.round((datos.fuerza_min + datos.fuerza_max) / 2);

    function pintarPuntos() {
        const caja = document.getElementById("puntos");
        caja.innerHTML = "";
        for (let i = 0; i < datos.intentos; i++) {
            const span = document.createElement("span");
            span.className = "punto" + (i < intentosUsados ? " usado" : "");
            caja.appendChild(span);
        }
    }

    function actualizarEtiquetas() {
        document.getElementById("valor-angulo").textContent = anguloInput.value;
        document.getElementById("valor-fuerza").textContent = fuerzaInput.value;
    }

    function dibujarEscena(puntosTrayectoria) {
        ctx.clearRect(0, 0, W, H);
        ctx.strokeStyle = "#333"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(0, GROUND); ctx.lineTo(W, GROUND); ctx.stroke();

        // Objetivo fijo.
        const tx = LAUNCH_X + datos.objetivo_x, ty = GROUND - datos.objetivo_y;
        ctx.strokeStyle = "#00aa00"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(tx, ty, datos.objetivo_radio, 0, Math.PI * 2); ctx.stroke();
        ctx.beginPath(); ctx.arc(tx, ty, 6, 0, Math.PI * 2); ctx.stroke();

        if (puntosTrayectoria && puntosTrayectoria.length > 1) {
            ctx.strokeStyle = "#00ff00"; ctx.lineWidth = 2.5;
            ctx.beginPath();
            puntosTrayectoria.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
            ctx.stroke();
            const [ultimoX, ultimoY] = puntosTrayectoria[puntosTrayectoria.length - 1];
            ctx.fillStyle = "#fff";
            ctx.beginPath(); ctx.arc(ultimoX, ultimoY, 5, 0, Math.PI * 2); ctx.fill();
        }
    }

    function mensaje(html, error = false) {
        resultado.innerHTML = `<p class="mensaje ${error ? "error" : ""}">${html}</p>`;
    }

    function puntosDeTrayectoria(a, b, alcance) {
        const pasos = 80;
        const max = Math.min(alcance, (W - LAUNCH_X - 4));
        const puntos = [];
        for (let i = 0; i <= pasos; i++) {
            const x = (max * i) / pasos;
            const y = b * x - a * x * x;
            puntos.push([LAUNCH_X + x, GROUND - y]);
        }
        return puntos;
    }

    function animar(a, b, alcance, alFinalizar) {
        const puntos = puntosDeTrayectoria(a, b, alcance);
        let i = 0;
        disparando = true;
        function paso() {
            dibujarEscena(puntos.slice(0, i + 1));
            i++;
            if (i < puntos.length) {
                requestAnimationFrame(paso);
            } else {
                disparando = false;
                alFinalizar();
            }
        }
        paso();
    }

    async function disparar() {
        if (disparando || terminado) return;
        btnDisparar.disabled = true;
        let r;
        try {
            r = await ReCode.postJSON(disparoUrl, {
                angulo: Number(anguloInput.value),
                fuerza: Number(fuerzaInput.value),
            });
        } catch (err) {
            mensaje(err.message, true);
            btnDisparar.disabled = false;
            return;
        }
        animar(r.a, r.b, r.alcance, () => {
            intentosRestantes = r.intentos_restantes;
            intentosUsados = datos.intentos - intentosRestantes;
            pintarPuntos();
            if (r.acerto) return exito(r);
            if (r.agotado) return agotado(r);
            mensaje(r.mensaje, true);
            btnDisparar.disabled = false;
        });
    }

    function exito(r) {
        terminado = true;
        const saldo = document.getElementById("bitcoins-alumno");
        if (saldo) saldo.textContent = r.bitcoins_total;
        const premio = r.ya_otorgado
            ? "Ya habías completado este reto antes, así que no se otorgan bitcoins de nuevo."
            : `Ganaste <strong>₿ ${r.bitcoins_otorgados}</strong>.`;
        accionesNormal.hidden = true;
        resultado.innerHTML = `
            <div class="mensaje">
                <p><strong>¡Impacto!</strong> ${premio}</p>
                <div class="info-matematica">
                    <p>Ecuación del disparo: <b>y(x) = ${r.b.toFixed(3)}x − ${r.a.toFixed(5)}x²</b></p>
                    <p>Vértice (altura máxima): <b>(${r.vertice.x.toFixed(1)}, ${r.vertice.y.toFixed(1)})</b></p>
                    <p>Raíces (nivel del suelo): <b>x₁ = ${r.raices.x1}, x₂ = ${r.raices.x2.toFixed(1)}</b></p>
                    <p>El coeficiente de x² es negativo, por eso la parábola abre hacia abajo; el vértice es la altura máxima y las raíces marcan dónde la trayectoria toca el suelo.</p>
                </div>
            </div>
            <a class="boton" href="${ReCode.reto.volverUrl}">Volver a los retos</a>`;
    }

    function agotado(r) {
        mensaje(r.mensaje, true);
        accionesNormal.hidden = true;
        accionesAgotado.hidden = false;
    }

    async function reintentar() {
        try {
            const r = await ReCode.postJSON(reintentarUrl);
            intentosRestantes = r.intentos_restantes;
            intentosUsados = 0;
            terminado = false;
            pintarPuntos();
            dibujarEscena();
            resultado.innerHTML = "";
            accionesAgotado.hidden = true;
            accionesNormal.hidden = false;
            btnDisparar.disabled = false;
        } catch (err) {
            mensaje(err.message, true);
        }
    }

    // --- FE-1: salir / rendirse con confirmación ----------------------------

    function pedirSalida(e) {
        if (e) e.preventDefault();
        if (terminado) return;
        if (typeof dialogo.showModal === "function") {
            dialogo.showModal();
        } else if (window.confirm("Se perderá el progreso de este intento y no obtendrás bitcoins. ¿Salir?")) {
            window.location.href = ReCode.reto.volverUrl;
        }
    }

    document.getElementById("btn-salir").addEventListener("click", pedirSalida);
    document.getElementById("btn-salir-agotado").addEventListener("click", pedirSalida);
    const flecha = document.querySelector(".btn-regresar");
    if (flecha) flecha.addEventListener("click", (e) => { if (intentosUsados > 0 && !terminado) pedirSalida(e); });
    document.getElementById("btn-cancelar-salida").addEventListener("click", () => dialogo.close());
    document.getElementById("btn-confirmar-salida").addEventListener("click", () => {
        window.location.href = ReCode.reto.volverUrl;
    });
    btnDisparar.addEventListener("click", disparar);
    document.getElementById("btn-reintentar").addEventListener("click", reintentar);
    anguloInput.addEventListener("input", actualizarEtiquetas);
    fuerzaInput.addEventListener("input", actualizarEtiquetas);

    pintarPuntos();
    actualizarEtiquetas();
    dibujarEscena();
})();
