// Ecuaciones lineales (CU-07) "Resolver ecuaciones lineales en una matriz".
// El navegador solo muestra las matrices y las pistas y manda los valores escritos.
// Quien valida que sean enteros y evalúa las pistas es la vista de Django (views.revisar).
function iniciarMatriz() {
    const raiz = document.getElementById("matriz");
    const datosTag = document.getElementById("matriz-datos");
    if (!raiz || !datosTag) { console.error("Matriz: falta #matriz o #matriz-datos en reto.html"); return; }
    const datos = JSON.parse(datosTag.textContent);
    if (!datos.matriz || !datos.pistas || !datos.celdas) {
        raiz.insertAdjacentHTML("afterbegin",
            '<p class="matriz-mensaje error">Datos del reto desactualizados: reemplaza ejercicios.py por la versión nueva y reinicia el servidor.</p>');
        console.error("Matriz: datos_publicos incompleto. ¿ejercicios.py viejo?", datos);
        return;
    }
    const revisarUrl = raiz.dataset.revisarUrl;
    const $ = id => document.getElementById(id);
    const cajas = {};                       // nombre de celda -> <input>

    $("matriz-mision").textContent = datos.mision;

    // --- Matrices --------------------------------------------------------------
    function celdaFija(valor) {
        const d = document.createElement("div");
        d.className = "celda";
        d.textContent = valor;
        return d;
    }
    function indice(texto) {                 // encabezado de índice fila/columna
        const d = document.createElement("div");
        d.className = "indice";
        d.textContent = texto;
        return d;
    }
    function encabezado(rejilla) {
        rejilla.appendChild(indice("F\\C"));
        [0, 1, 2].forEach(j => rejilla.appendChild(indice(`[${j}]`)));
    }
    const nombreEn = {};                     // "fila,col" -> nombre de la caja
    datos.celdas.forEach(c => { nombreEn[`${c.fila},${c.col}`] = c.nombre; });
    encabezado($("matriz-referencia"));
    encabezado($("matriz-respuesta"));

    datos.matriz.forEach((fila, i) => {
        $("matriz-referencia").appendChild(indice(`[${i}]`));
        $("matriz-respuesta").appendChild(indice(`[${i}]`));
        fila.forEach((valor, j) => {
            const esIncognita = typeof valor === "string";
            // Referencia: valores conocidos y nombre de las cajas por completar.
            const ref = celdaFija(esIncognita ? `Caja ${valor}` : valor);
            if (esIncognita) ref.classList.add("celda-incognita");
            $("matriz-referencia").appendChild(ref);

            // Respuesta: conocidos fijos y un cuadro de texto por incógnita.
            if (!esIncognita) { $("matriz-respuesta").appendChild(celdaFija(valor)); return; }
            const caja = document.createElement("input");
            caja.type = "text";
            caja.inputMode = "numeric";
            caja.autocomplete = "off";
            caja.className = "celda celda-caja";
            caja.setAttribute("aria-label", `Valor de ${valor}`);
            caja.placeholder = valor;
            caja.addEventListener("input", () => { caja.classList.remove("celda-mala"); pintarVivas(); });
            caja.addEventListener("keydown", e => { if (e.key === "Enter") $("btn-verificar").click(); });
            cajas[valor] = caja;
            $("matriz-respuesta").appendChild(caja);
        });
    });

    // --- Listas de pistas --------------------------------------------------------
    // Original: tal como son. Viva: copia con lo que vas escribiendo (solo lo muestra, NO evalúa).
    datos.pistas.forEach(texto => {
        const li = document.createElement("li");
        li.textContent = texto;
        $("pistas-originales").appendChild(li);
    });
    function pintarVivas() {
        const ul = $("pistas-vivas");
        ul.innerHTML = "";
        datos.pistas.forEach(texto => {
            const li = document.createElement("li");
            li.textContent = texto.replace(/Matriz\[(\d)\]\[(\d)\]/g, (ref, i, j) => {
                const valor = datos.matriz[i][j];
                if (typeof valor !== "string") return String(valor);
                const escrito = cajas[valor].value.trim();
                return escrito === "" ? ref : escrito;
            });
            ul.appendChild(li);
        });
    }
    function marcarPistasMalas(numeros) {
        [...$("pistas-originales").children, ...$("pistas-vivas").children].forEach((li, i) => {
            const n = (i % datos.pistas.length) + 1;
            li.classList.toggle("pista-mala", numeros.includes(n));
        });
    }
    function limpiarMarcas() {
        marcarPistasMalas([]);
        Object.values(cajas).forEach(c => c.classList.remove("celda-mala"));
    }

    // --- Verificar (el servidor decide) --------------------------------------------
    function valoresComoTexto() {
        return datos.celdas.map(c => `${c.nombre}=${cajas[c.nombre].value.trim()}`).join(",");
    }
    function mostrarAviso(texto) {
        const a = $("matriz-aviso");
        a.textContent = texto;
        a.hidden = !texto;
    }
    function numerosDe(mensaje) {            // "Pistas que no se cumplen: 1, 2 y 6."
        const m = mensaje.match(/:\s*([\d, y]+)\.?$/);
        return m ? (m[1].match(/\d+/g) || []).map(Number) : [];
    }
    function nombresDe(mensaje) {            // "Cuadros por corregir: A, B y F."
        const m = mensaje.match(/Cuadros por corregir:\s*(.+?)\.?$/);
        return m ? m[1].split(/,| y /).map(s => s.trim()).filter(Boolean) : [];
    }

    $("btn-verificar").addEventListener("click", async () => {
        $("btn-verificar").disabled = true;
        limpiarMarcas();
        mostrarAviso("");
        try {
            const r = await ReCode.postJSON(revisarUrl, { paso: 0, respuesta: valoresComoTexto() });
            const monedero = $("bitcoins-alumno");
            if (monedero && r.bitcoins_total !== undefined) monedero.textContent = r.bitcoins_total;
            if (r.correcto) { mostrarExito(r); return; }
            const msg = r.mensaje || datos.mensaje_incorrecto;
            if (msg.startsWith(datos.mensaje_invalido)) {                 // FA-2
                nombresDe(msg).forEach(n => cajas[n] && cajas[n].classList.add("celda-mala"));
            } else {                                                       // FA-1
                marcarPistasMalas(numerosDe(msg));
            }
            mostrarAviso(`Error. ${msg}`);
            $("btn-verificar").disabled = false;
        } catch (e) {
            mostrarAviso(e.message);
            $("btn-verificar").disabled = false;
        }
    });

    function mostrarExito(r) {
        Object.values(cajas).forEach(c => { c.readOnly = true; });
        $("matriz-mision").hidden = true;
        $("matriz-escena").hidden = true;
        $("resultado-exito").hidden = false;
        $("exito-recompensa").textContent = r.bitcoins_otorgados
            ? `+${r.bitcoins_otorgados} ₿`
            : "La recompensa de este reto ya fue otorgada anteriormente.";
    }

    // --- Salir / Rendirse (FE-1): no se guarda nada -------------------------------
    $("btn-salir").addEventListener("click", () => { $("confirmar-salir").hidden = false; });
    $("btn-salir-no").addEventListener("click", () => { $("confirmar-salir").hidden = true; });

    pintarVivas();
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciarMatriz);
} else {
    iniciarMatriz();
}
