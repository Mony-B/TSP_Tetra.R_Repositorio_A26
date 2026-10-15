// Obtener el término (CU-09): pistas + huecos; Django revisa el término.
(() => {
    const pasos = ReCode.reto.datos.pasos;
    let actual = 0;
    const input = document.getElementById("respuesta");

    function mostrar() {
        const p = pasos[actual];
        document.getElementById("pistas").innerHTML = p.pistas.map(t => `<li>${t}</li>`).join("");
        document.getElementById("huecos").textContent = "_ ".repeat(p.letras).trim();
        document.getElementById("avance").textContent = `Término ${actual + 1} de ${pasos.length}`;
        input.value = "";
        input.focus();
    }

    document.getElementById("form-respuesta").addEventListener("submit", async (e) => {
        e.preventDefault();
        const r = await ReCode.enviarRespuesta(actual, input.value);
        if (r.completado) {
            document.getElementById("juego").innerHTML = "";
        } else if (r.correcto) {
            actual++;
            mostrar();
        }
    });

    mostrar();
})();
