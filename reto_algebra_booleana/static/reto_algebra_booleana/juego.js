// Álgebra booleana (CU-05): una expresión a la vez, se elige la respuesta.
(() => {
    const pasos = ReCode.reto.datos.pasos;
    let actual = 0;

    function mostrar() {
        const p = pasos[actual];
        document.getElementById("pregunta").textContent = p.pregunta;
        document.getElementById("avance").textContent = `Puerta ${actual + 1} de ${pasos.length}`;
        const caja = document.getElementById("opciones");
        caja.innerHTML = "";
        p.opciones.forEach(op => {
            const b = document.createElement("button");
            b.type = "button";
            b.textContent = op;
            b.onclick = () => responder(op);
            caja.appendChild(b);
        });
    }

    async function responder(op) {
        const r = await ReCode.enviarRespuesta(actual, op);
        if (r.completado) {
            document.getElementById("juego").innerHTML = "";
        } else if (r.correcto) {
            actual++;
            mostrar();
        }
    }

    mostrar();
})();
