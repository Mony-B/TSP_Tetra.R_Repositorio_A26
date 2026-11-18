// Tiro parabólico (CU-12).
// El ángulo y la fuerza se mandan al servidor, que calcula la trayectoria
// real (y si acierta) y regresa los coeficientes y(x) = b·x − a·x² junto
// con el alcance; el navegador solo los usa para animar el disparo y para
// dibujar la guía de vista previa (misma fórmula, nunca decide el acierto).
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
    // Misma gravedad didáctica que usa el servidor para calcular a y b
    // (unidades de lienzo, no metros reales); solo sirve para dibujar la
    // guía de vista previa en el navegador.
    const GRAVEDAD = 700;

    // Color de acento del reto (el mismo que su tarjeta en la selección):
    // se lee de --accent, puesto en <body> por reto_base.html según la app.
    const ACENTO = getComputedStyle(document.body).getPropertyValue("--accent").trim() || "#59c7ff";
    function acentoAlpha(alpha) {
        const n = parseInt(ACENTO.replace("#", ""), 16);
        const r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    const anguloInput = document.getElementById("angulo");
    const fuerzaInput = document.getElementById("fuerza");
    const resultado = document.getElementById("resultado");
    const accionesNormal = document.getElementById("acciones-parabolica");
    const dialogoExito = document.getElementById("dialogo-exito");
    const dialogoAgotado = document.getElementById("dialogo-agotado");
    const btnDisparar = document.getElementById("btn-disparar");
    const btnReintentar = document.getElementById("btn-reintentar");

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

    // --- Vista previa: misma fórmula que el servidor, antes de disparar ----

    function parametrosPrevia() {
        const theta = (Number(anguloInput.value) * Math.PI) / 180;
        const velocidad = 110 + Number(fuerzaInput.value) * 6;
        const a = GRAVEDAD / (2 * velocidad * velocidad * Math.cos(theta) ** 2);
        const b = Math.tan(theta);
        return { a, b };
    }

    function actualizarEcuacionPrevia() {
        const { a, b } = parametrosPrevia();
        document.getElementById("ecuacion-previa").textContent =
            `y(x) = −${a.toFixed(5)}x² + ${b.toFixed(3)}x + 0`;
        document.getElementById("coef-a").textContent = "−" + a.toFixed(5);
        document.getElementById("coef-b").textContent = b.toFixed(3);
    }

    function puntosDeTrayectoria(a, b, alcance, proporcion = 1) {
        const pasos = 80;
        const max = Math.min(alcance, (W - LAUNCH_X - 4)) * proporcion;
        const puntos = [];
        for (let i = 0; i <= pasos; i++) {
            const x = (max * i) / pasos;
            const y = b * x - a * x * x;
            puntos.push([LAUNCH_X + x, GROUND - y]);
        }
        return puntos;
    }

    function dibujarCuadricula() {
        const paso = 50;
        ctx.save();
        ctx.lineWidth = 1;
        ctx.strokeStyle = acentoAlpha(0.14);
        for (let x = LAUNCH_X; x < W; x += paso) {
            ctx.beginPath(); ctx.moveTo(x, 8); ctx.lineTo(x, GROUND); ctx.stroke();
        }
        for (let x = LAUNCH_X - paso; x >= 0; x -= paso) {
            ctx.beginPath(); ctx.moveTo(x, 8); ctx.lineTo(x, GROUND); ctx.stroke();
        }
        for (let y = GROUND; y >= 10; y -= paso) {
            ctx.beginPath(); ctx.moveTo(5, y); ctx.lineTo(W - 4, y); ctx.stroke();
        }
        ctx.strokeStyle = acentoAlpha(0.45); ctx.lineWidth = 1.3;
        ctx.beginPath(); ctx.moveTo(LAUNCH_X, 8); ctx.lineTo(LAUNCH_X, GROUND); ctx.lineTo(W - 4, GROUND); ctx.stroke();
        ctx.restore();
    }

    function dibujarEscena(proyectil, puntosTrayectoria) {
        ctx.clearRect(0, 0, W, H);
        dibujarCuadricula();

        ctx.strokeStyle = "#333"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(0, GROUND); ctx.lineTo(W, GROUND); ctx.stroke();

        // Objetivo fijo.
        const tx = LAUNCH_X + datos.objetivo_x, ty = GROUND - datos.objetivo_y;
        ctx.strokeStyle = acentoAlpha(0.6); ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(tx, ty, datos.objetivo_radio, 0, Math.PI * 2); ctx.stroke();
        ctx.beginPath(); ctx.arc(tx, ty, 6, 0, Math.PI * 2); ctx.stroke();

        // Guía punteada de vista previa (solo el inicio), igual que el
        // prototipo: ayuda a visualizar hacia dónde apunta el disparo sin
        // revelar si acertará.
        if (!disparando && !puntosTrayectoria) {
            const { a, b } = parametrosPrevia();
            const alcancePrevia = a ? b / a : 0;
            const guia = puntosDeTrayectoria(a, b, alcancePrevia, 0.28);
            ctx.save();
            ctx.setLineDash([5, 7]);
            ctx.strokeStyle = acentoAlpha(0.6); ctx.lineWidth = 2;
            ctx.beginPath();
            guia.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
            ctx.stroke();
            ctx.restore();
        }

        if (puntosTrayectoria && puntosTrayectoria.length > 1) {
            ctx.strokeStyle = ACENTO; ctx.lineWidth = 2.5;
            ctx.beginPath();
            puntosTrayectoria.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
            ctx.stroke();
        }
        if (proyectil) {
            ctx.fillStyle = "#fff";
            ctx.beginPath(); ctx.arc(proyectil[0], proyectil[1], 5, 0, Math.PI * 2); ctx.fill();
        }
    }

    function mensaje(html, error = false) {
        resultado.innerHTML = `<p class="mensaje ${error ? "error" : ""}">${html}</p>`;
    }

    function animar(a, b, alcance, alFinalizar) {
        const puntos = puntosDeTrayectoria(a, b, alcance);
        let i = 0;
        disparando = true;
        function paso() {
            const trayectoHastaAqui = puntos.slice(0, i + 1);
            dibujarEscena(puntos[i], trayectoHastaAqui);
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
        document.getElementById("exito-premio").innerHTML = premio;
        document.getElementById("exito-ecuacion").textContent =
            `y(x) = ${r.b.toFixed(3)}x − ${r.a.toFixed(5)}x²`;
        document.getElementById("exito-vertice").textContent =
            `(${r.vertice.x.toFixed(1)}, ${r.vertice.y.toFixed(1)})`;
        document.getElementById("exito-raices").textContent =
            `x₁ = ${r.raices.x1}, x₂ = ${r.raices.x2.toFixed(1)}`;
        accionesNormal.hidden = true;
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
            const r = await ReCode.postJSON(reintentarUrl);
            intentosRestantes = r.intentos_restantes;
            intentosUsados = 0;
            terminado = false;
            pintarPuntos();
            dibujarEscena();
            resultado.innerHTML = "";
            ReCode.dialogos.cerrar(dialogoAgotado);
            btnDisparar.disabled = false;
        } catch (err) {
            mensaje(err.message, true);
        }
    }

    // --- FE-1: salir / rendirse con confirmación ----------------------------
    // Diálogo y mensaje de salida compartidos con los demás retos
    // (comun/reto_base.html + comun/js/reto_dialogos.js). "Salir / Rendirse"
    // dentro de la ventana de agotado reusa el mismo flujo (FA-1.4.5).
    const btnSalir = document.getElementById("btn-salir");
    ReCode.dialogos.inicializarSalir({
        hayProgreso: () => intentosUsados > 0,
        puedeSalir: () => !terminado,
        mensaje: "Se perderá el progreso de este intento y no obtendrás bitcoins. ¿Seguro que quieres salir?",
    });
    document.getElementById("btn-salir-agotado").addEventListener("click", () => btnSalir.click());

    btnDisparar.addEventListener("click", disparar);
    btnReintentar.addEventListener("click", reintentar);
    anguloInput.addEventListener("input", () => {
        actualizarEtiquetas();
        actualizarEcuacionPrevia();
        if (!disparando) dibujarEscena();
    });
    fuerzaInput.addEventListener("input", () => {
        actualizarEtiquetas();
        actualizarEcuacionPrevia();
        if (!disparando) dibujarEscena();
    });

    pintarPuntos();
    actualizarEtiquetas();
    actualizarEcuacionPrevia();
    dibujarEscena();
})();
