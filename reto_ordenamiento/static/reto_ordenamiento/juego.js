// Resolver reto de ordenamiento (CU-11).
// Colocar y retirar pasos de la línea solo ocurre en el navegador; el
// servidor únicamente revisa la secuencia completa cuando se presiona
// "Verificar".
(() => {
    const { pasos, total } = ReCode.reto.datos;
    const pozo = document.getElementById("pozo");
    const linea = document.getElementById("linea");
    const resultado = document.getElementById("resultado");
    const acciones = document.getElementById("acciones-ordenamiento");
    const dialogo = document.getElementById("dialogo-salir");

    const textoDe = {};
    pasos.forEach((p) => { textoDe[p.id] = p.texto; });

    let secuencia = Array(total).fill(null); // id de paso en cada espacio
    let bloqueado = false;

    function colocados() {
        return new Set(secuencia.filter((v) => v !== null));
    }

    function render(marcas = {}) {
        // Pozo: pasos aún no colocados, en el orden desordenado fijo.
        pozo.innerHTML = "";
        const usados = colocados();
        const libres = pasos.filter((p) => !usados.has(p.id));
        if (!libres.length) {
            const span = document.createElement("span");
            span.className = "pozo-vacio";
            span.textContent = "Todos los pasos están en la línea.";
            pozo.appendChild(span);
        } else {
            libres.forEach((p) => {
                const b = document.createElement("button");
                b.type = "button";
                b.className = "paso-boton";
                b.textContent = p.texto;
                b.disabled = bloqueado;
                b.addEventListener("click", () => colocar(p.id));
                pozo.appendChild(b);
            });
        }

        // Línea de secuencia.
        linea.innerHTML = "";
        secuencia.forEach((id, posicion) => {
            const li = document.createElement("li");
            li.className = "espacio" + (id !== null ? " lleno" : "") + (marcas[posicion] ? " " + marcas[posicion] : "");
            const num = document.createElement("span");
            num.className = "espacio-num";
            num.textContent = posicion + 1;
            const cuerpo = document.createElement("div");
            cuerpo.className = "espacio-cuerpo";
            if (id === null) {
                const vacio = document.createElement("span");
                vacio.className = "vacio";
                vacio.textContent = "Espacio libre";
                cuerpo.appendChild(vacio);
            } else {
                const b = document.createElement("button");
                b.type = "button";
                b.className = "paso-boton";
                b.disabled = bloqueado;
                b.innerHTML = `<span></span><span class="quitar">Retirar</span>`;
                b.firstChild.textContent = textoDe[id];
                b.addEventListener("click", () => retirar(posicion));
                cuerpo.appendChild(b);
            }
            li.append(num, cuerpo);
            linea.appendChild(li);
        });
    }

    function mensaje(html, error = false) {
        resultado.innerHTML = `<p class="mensaje ${error ? "error" : ""}">${html}</p>`;
    }

    function colocar(id) {
        if (bloqueado) return;
        const posicion = secuencia.indexOf(null);
        if (posicion === -1) return;
        secuencia[posicion] = id;
        render();
        mensaje(`Paso colocado en el espacio ${posicion + 1}. Cuando estés conforme, presiona Verificar.`);
    }

    function retirar(posicion) {
        if (bloqueado) return;
        secuencia[posicion] = null;
        render();
        mensaje(`Retiraste el paso del espacio ${posicion + 1}.`);
    }

    async function verificar() {
        if (bloqueado) return;
        let r;
        try {
            r = await ReCode.postJSON(ReCode.reto.revisarUrl, { secuencia });
        } catch (err) {
            mensaje(err.message, true);
            return;
        }

        if (r.vacios && r.vacios.length) {
            const marcas = {};
            r.vacios.forEach((i) => { marcas[i] = "falta"; });
            render(marcas);
            const lista = r.vacios.map((i) => i + 1).join(", ");
            mensaje(
                r.vacios.length === 1
                    ? `Falta llenar el espacio ${lista}.`
                    : `Faltan llenar los espacios ${lista}.`,
                true,
            );
            return;
        }
        if (!r.correcto) {
            render();
            mensaje("Al menos un paso no está en el orden correcto. Corrige y vuelve a verificar.", true);
            return;
        }

        // Éxito.
        bloqueado = true;
        const marcas = {};
        secuencia.forEach((_, i) => { marcas[i] = "correcto"; });
        render(marcas);
        const saldo = document.getElementById("bitcoins-alumno");
        if (saldo) saldo.textContent = r.bitcoins_total;
        const premio = r.ya_otorgado
            ? "Este reto ya estaba completado, así que no se otorgan bitcoins de nuevo."
            : `Ganaste <strong>₿ ${r.bitcoins_otorgados}</strong>.`;
        acciones.hidden = true;
        resultado.innerHTML = `
            <p class="mensaje"><strong>¡Algoritmo restaurado!</strong> ${premio}</p>
            <a class="boton" href="${ReCode.reto.volverUrl}">Volver a los retos</a>`;
    }

    // --- FE-1: salir / rendirse con confirmación --------------------------

    function pedirSalida(e) {
        if (e) e.preventDefault();
        if (bloqueado) return;
        if (typeof dialogo.showModal === "function") {
            dialogo.showModal();
        } else if (window.confirm("Se perderá el progreso de este reto y no obtendrás bitcoins. ¿Salir?")) {
            window.location.href = ReCode.reto.volverUrl;
        }
    }

    document.getElementById("btn-salir").addEventListener("click", pedirSalida);
    const flecha = document.querySelector(".btn-regresar");
    if (flecha) flecha.addEventListener("click", (e) => { if (colocados().size > 0 && !bloqueado) pedirSalida(e); });
    document.getElementById("btn-cancelar-salida").addEventListener("click", () => dialogo.close());
    document.getElementById("btn-confirmar-salida").addEventListener("click", () => {
        window.location.href = ReCode.reto.volverUrl;
    });
    document.getElementById("btn-verificar").addEventListener("click", verificar);

    render();
})();
