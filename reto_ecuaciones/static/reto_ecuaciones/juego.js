// Ecuaciones (CU-07): el alumno escribe x y Django lo revisa.
(() => {
    const pasos = ReCode.reto.datos.pasos;
    let actual = 0;
    const input = document.getElementById("respuesta");

    function mostrar() {
        document.getElementById("ecuacion").textContent = pasos[actual].ecuacion;
        document.getElementById("avance").textContent = `Ecuación ${actual + 1} de ${pasos.length}`;
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
