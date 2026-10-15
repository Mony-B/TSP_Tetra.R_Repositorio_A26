// Sopa de conceptos (CU-10): se toca la primera y la última letra de la palabra
// y Django revisa si es uno de los conceptos.
(() => {
    const { sopa, pasos } = ReCode.reto.datos;
    const n = sopa.length;
    const tablero = document.getElementById("sopa");
    const celdas = [];
    let inicio = null;

    tablero.style.gridTemplateColumns = `repeat(${n}, auto)`;
    sopa.forEach((fila, f) => {
        celdas.push([]);
        [...fila].forEach((letra, c) => {
            const b = document.createElement("button");
            b.type = "button";
            b.textContent = letra;
            b.onclick = () => tocar(f, c);
            tablero.appendChild(b);
            celdas[f].push(b);
        });
    });

    document.getElementById("definiciones").innerHTML =
        pasos.map((p, i) => `<li id="def-${i}">${p.definicion}</li>`).join("");

    // Celdas en línea recta entre dos puntos (horizontal, vertical o diagonal)
    function linea(a, b) {
        const df = Math.sign(b[0] - a[0]), dc = Math.sign(b[1] - a[1]);
        const largo = Math.max(Math.abs(b[0] - a[0]), Math.abs(b[1] - a[1]));
        const recta = a[0] === b[0] || a[1] === b[1] ||
                      Math.abs(b[0] - a[0]) === Math.abs(b[1] - a[1]);
        if (!recta) return null;
        return Array.from({ length: largo + 1 }, (_, i) => [a[0] + df * i, a[1] + dc * i]);
    }

    async function tocar(f, c) {
        if (!inicio) {
            inicio = [f, c];
            celdas[f][c].classList.add("inicio");
            return;
        }
        celdas[inicio[0]][inicio[1]].classList.remove("inicio");
        const camino = linea(inicio, [f, c]);
        inicio = null;
        if (!camino || camino.length < 2) return;

        const palabra = camino.map(([x, y]) => sopa[x][y]).join("");
        const r = await ReCode.enviarRespuesta(null, palabra);
        if (r.correcto) {
            camino.forEach(([x, y]) => celdas[x][y].classList.add("encontrada"));
            document.getElementById(`def-${r.paso}`).classList.add("hecha");
        }
    }
})();
