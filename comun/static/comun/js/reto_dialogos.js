// JS compartido (app comun): patrón repetido en los 10 retos para las
// ventanas emergentes de "Salir / Rendirse" y de "reto completado".
// Vive aparte de recode.js (que es para hablar con el servidor) para no
// amontonar funciones sin relación en un mismo archivo.
//
// Regla de los 10 retos (R8): al salir siempre se confirma en una
// <dialog>; al completar el reto nunca se redirige solo, se abre otra
// <dialog> con un botón para volver.
window.ReCode = window.ReCode || {};
ReCode.dialogos = {
    // Abre una <dialog> como modal; si el navegador no soporta
    // showModal() (muy viejo), la deja visible sin bloquear el resto de
    // la página en vez de no mostrar nada.
    abrir(dialogo) {
        if (!dialogo) return;
        if (typeof dialogo.showModal === "function") {
            dialogo.showModal();
        } else {
            dialogo.setAttribute("open", "");
        }
    },

    cerrar(dialogo) {
        if (dialogo && dialogo.open) dialogo.close();
    },

    // Pide confirmación antes de salir del reto (sin guardar nada).
    // `dialogo` es la <dialog> de confirmación; si el navegador no la
    // soporta, cae a un confirm() nativo. `alConfirmar` es a dónde ir
    // (URL) o, si el reto necesita algo más que navegar (p. ej. limpiar
    // el tablero primero), una función.
    pedirSalida(dialogo, mensaje, alConfirmar, evento) {
        if (evento) evento.preventDefault();
        if (dialogo && typeof dialogo.showModal === "function") {
            dialogo.showModal();
        } else if (window.confirm(mensaje)) {
            if (typeof alConfirmar === "function") alConfirmar();
            else window.location.href = alConfirmar;
        }
    },

    // La flecha de "regresar" de la barra superior también debe pedir
    // confirmación mientras se está jugando. `hayProgreso` es una
    // función que cada reto define (p. ej. "¿ya coloqué algo?").
    conectarFlechaSalir(dialogo, mensaje, alConfirmar, hayProgreso) {
        const flecha = document.querySelector(".volver");
        if (!flecha) return;
        flecha.addEventListener("click", (evento) => {
            if (hayProgreso()) ReCode.dialogos.pedirSalida(dialogo, mensaje, alConfirmar, evento);
        });
    },

    // Escapa texto antes de meterlo en innerHTML (evita inyectar HTML
    // cuando el texto viene del servidor o lo escribió el alumno).
    escaparHTML(texto) {
        const d = document.createElement("div");
        d.textContent = texto;
        return d.innerHTML;
    },

    // Conecta #dialogo-salir / #btn-salir / #btn-cancelar-salida /
    // #btn-confirmar-salida (ya vienen armados desde comun/reto_base.html)
    // con el patrón de los 10 retos: cancelar sigue jugando, confirmar
    // navega a ReCode.reto.volverUrl sin guardar nada.
    //
    // Cada reto solo necesita llamar esto una vez desde su juego.js:
    //   ReCode.dialogos.inicializarSalir({
    //       hayProgreso: () => /* ¿ya hizo algo que se perdería? */,
    //       puedeSalir: () => /* opcional: false si ya terminó el reto */,
    //       alCancelar: () => /* opcional: algo extra al seguir jugando, p. ej. refocar un input */,
    //   });
    inicializarSalir({ hayProgreso = () => true, puedeSalir = () => true, alCancelar, mensaje } = {}) {
        const dialogo = document.getElementById("dialogo-salir");
        const btnSalir = document.getElementById("btn-salir");
        const btnCancelar = document.getElementById("btn-cancelar-salida");
        const btnConfirmar = document.getElementById("btn-confirmar-salida");
        if (!dialogo || !btnSalir || !btnCancelar || !btnConfirmar) {
            console.error("ReCode.dialogos.inicializarSalir: falta #dialogo-salir o sus botones (revisa que reto.html extienda comun/reto_base.html).");
            return;
        }
        const MENSAJE_SALIR = mensaje || dialogo.querySelector("p")?.textContent
            || "Se perderá el progreso de este reto y no obtendrás bitcoins. ¿Seguro que quieres salir?";
        const volverUrl = window.ReCode?.reto?.volverUrl;

        function pedirSalida(evento) {
            if (!puedeSalir()) return;
            ReCode.dialogos.pedirSalida(dialogo, MENSAJE_SALIR, volverUrl, evento);
        }
        btnSalir.addEventListener("click", pedirSalida);
        btnCancelar.addEventListener("click", () => {
            ReCode.dialogos.cerrar(dialogo);
            if (alCancelar) alCancelar();
        });
        btnConfirmar.addEventListener("click", () => {
            window.location.href = volverUrl; // no se guarda nada ni se dan bitcoins
        });
        // La flecha de regresar de la barra superior también pide confirmación mientras se juega.
        ReCode.dialogos.conectarFlechaSalir(dialogo, MENSAJE_SALIR, volverUrl, () => puedeSalir() && hayProgreso());
    },
};
