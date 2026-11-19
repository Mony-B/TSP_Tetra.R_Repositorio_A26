// Examen final de materia (CU04): temporizador estricto, selección visual
// de respuesta, abandono con confirmación y el jumpscare de tiempo agotado.
// Nada de esto calcula el resultado -eso solo lo hace el servidor al
// recibir el POST de "Enviar respuestas" (ver batalla/views.py)-; agotar
// el tiempo o abandonar nunca manda ese POST, así que el servidor nunca
// se entera y no guarda ningún progreso ni otorga bitcoins (R39/R75).
(() => {
    "use strict";
    const form = document.getElementById("form-examen");
    const reloj = document.getElementById("reloj");
    const jumpscare = document.getElementById("jumpscare");

    // --- Selección visual de respuesta (el <input type=radio> real manda
    // el valor; .sel es solo para que se vea marcada, igual que en los
    // demás retos con .opt) -----------------------------------------------
    document.querySelectorAll(".pregunta").forEach((fieldset) => {
        fieldset.querySelectorAll("input[type=radio]").forEach((radio) => {
            radio.addEventListener("change", () => {
                fieldset.querySelectorAll(".opt").forEach((et) => et.classList.remove("sel"));
                radio.closest(".opt").classList.add("sel");
            });
        });
    });

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

    // FA-1: tiempo agotado -> jumpscare, nunca se manda el formulario.
    function agotarTiempo() {
        detenerExamen();
        jumpscare.hidden = false;
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
