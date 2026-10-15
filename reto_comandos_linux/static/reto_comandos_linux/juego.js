// Comandos de Linux (CU-06): terminal simulada; Django revisa cada comando.
(() => {
    const pasos = ReCode.reto.datos.pasos;
    let actual = 0;
    const lineas = document.getElementById("lineas");
    const input = document.getElementById("comando");

    function escribir(texto, clase = "") {
        const div = document.createElement("div");
        div.className = `linea ${clase}`;
        div.textContent = texto;
        lineas.appendChild(div);
        const term = document.getElementById("terminal");
        term.scrollTop = term.scrollHeight;
    }

    function tarea() {
        escribir(`# Tarea ${actual + 1}/${pasos.length}: ${pasos[actual].tarea}`, "tarea");
    }

    document.getElementById("form-comando").addEventListener("submit", async (e) => {
        e.preventDefault();
        const comando = input.value;
        if (!comando.trim()) return;
        input.value = "";
        escribir(`alumno@recode:~$ ${comando}`);
        const r = await ReCode.enviarRespuesta(actual, comando);
        escribir(r.mensaje, r.correcto ? "" : "error");
        if (r.completado) {
            input.disabled = true;
        } else if (r.correcto) {
            actual++;
            tarea();
        }
    });

    tarea();
    input.focus();
})();
