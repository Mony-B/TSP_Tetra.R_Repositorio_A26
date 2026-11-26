// Examen final de materia (CU04): temporizador estricto, preguntas de una
// en una ("Q.0X/15", como en la maqueta), abandono con confirmación y el
// jumpscare de tiempo agotado en dos fases. Nada de esto calcula el
// resultado -eso solo lo hace el servidor al recibir el POST de "Enviar
// respuestas" (ver batalla/views.py)-; agotar el tiempo o abandonar nunca
// manda ese POST, así que el servidor nunca se entera y no guarda ningún
// progreso ni otorga bitcoins (R39/R75).
(() => {
    "use strict";
    const form = document.getElementById("form-examen");
    const reloj = document.getElementById("reloj");
    const jumpscare = document.getElementById("jumpscare");

    // --- Selección visual de respuesta (el <input type=radio> real manda
    // el valor; .sel es solo para que se vea marcada la casilla) ---------
    document.querySelectorAll(".pregunta").forEach((fieldset) => {
        fieldset.querySelectorAll("input[type=radio]").forEach((radio) => {
            radio.addEventListener("change", () => {
                fieldset.querySelectorAll(".opt").forEach((et) => et.classList.remove("sel"));
                radio.closest(".opt").classList.add("sel");
            });
        });
    });

    // --- Preguntas de una en una ("Q.0X/15") -----------------------------
    const fieldsets = Array.from(document.querySelectorAll(".pregunta"));
    const total = fieldsets.length;
    const contadorActual = document.getElementById("preg-actual");
    const btnAnterior = document.getElementById("btn-anterior");
    const btnSiguiente = document.getElementById("btn-siguiente");
    const btnEnviar = document.getElementById("btn-enviar");
    let actual = 0;

    function mostrarPregunta(i) {
        actual = Math.max(0, Math.min(i, total - 1));
        fieldsets.forEach((fs, idx) => { fs.hidden = idx !== actual; });
        if (contadorActual) contadorActual.textContent = String(actual + 1).padStart(2, "0");
        btnAnterior.disabled = actual === 0;
        const esUltima = actual === total - 1;
        btnSiguiente.hidden = esUltima;
        btnEnviar.hidden = !esUltima;
    }
    if (total > 0) mostrarPregunta(0);

    btnAnterior.addEventListener("click", () => mostrarPregunta(actual - 1));
    btnSiguiente.addEventListener("click", () => mostrarPregunta(actual + 1));

    // --- Temporizador --------------------------------------------------
    let restante = parseInt(reloj.dataset.limite, 10) || 0;
    function pintarReloj() {
        reloj.textContent = `${Math.floor(restante / 60)}:${String(restante % 60).padStart(2, "0")}`;
        reloj.classList.toggle("urgente", restante <= 30);
    }
    pintarReloj();
    const intervalo = setInterval(() => {
        restante--;
        pintarReloj();
        if (restante <= 0) {
            clearInterval(intervalo);
            agotarTiempo();
        }
    }, 1000);

    function detenerExamen() {
        clearInterval(intervalo);
        form.querySelectorAll("input, button").forEach((el) => { el.disabled = true; });
    }

    // FA-1: tiempo agotado -> jumpscare en dos fases, nunca se manda el
    // formulario. El elemento entero estaba [hidden]; aquí es cuando
    // aparece, siempre arrancando en la fase "impacto" (destello + texto
    // de glitch sobre jumpscare_impacto.gif, con sacudida de pantalla).
    // Medio segundo después se asienta en "bloqueo" (jumpscare_bloqueo.gif
    // fijo con el aviso y los botones de Reintentar/Volver).
    function agotarTiempo() {
        detenerExamen();
        jumpscare.hidden = false;
        jumpscare.classList.remove("fase-bloqueo");
        setTimeout(() => jumpscare.classList.add("fase-bloqueo"), 900);
    }
    document.getElementById("btn-reintentar").addEventListener("click", () => window.location.reload());

    // FE-1: abandono voluntario, con confirmación (mismo patrón que
    // "Salir / Rendirse" en los retos, ver comun/js/reto_dialogos.js).
    const dialogoAbandonar = document.getElementById("dialogo-abandonar");
    document.getElementById("btn-abandonar").addEventListener("click", () => {
        ReCode.dialogos.abrir(dialogoAbandonar);
    });
    document.getElementById("btn-cancelar-abandono").addEventListener("click", () => {
        ReCode.dialogos.cerrar(dialogoAbandonar);
    });
    document.getElementById("btn-confirmar-abandono").addEventListener("click", () => {
        detenerExamen();
        window.location.href = window.Examen.volverUrl;
    });
})();
