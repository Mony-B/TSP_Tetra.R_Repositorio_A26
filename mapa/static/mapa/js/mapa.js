// Pantalla del mapa. Los datos vienen de mapa/views.py (json_script "datos-mapa").
// La selección de edificio se hace con la barra lateral; el mapa solo muestra dónde está.
(function () {
    const DATOS = JSON.parse(document.getElementById("datos-mapa").textContent);
    const EDIFICIOS = DATOS.edificios;
    const KERNEL = DATOS.kernel;
    const I_KERNEL = EDIFICIOS.length;   // el kernel va después de los edificios
    const TOTAL = EDIFICIOS.length + 1;

    const TEXTO_ESTADO = {
        restaurado: "Restaurado", en_progreso: "En progreso",
        corrupto: "Corrupto", bloqueado: "Bloqueado", abierto: "Acceso abierto",
    };

    const $ = (id) => document.getElementById(id);
    let indice = 0;

    // ---- Escalado del lienzo de 1536x1024 al tamaño de la ventana ----
    function escalar() {
        const s = Math.min(window.innerWidth / 1536, window.innerHeight / 1024);
        $("escenario").style.setProperty("--escala", s);
    }
    window.addEventListener("resize", escalar);
    escalar();

    // ---- Barra lateral ----
    function crearItem(ed, i, esKernel) {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "item" + (esKernel ? " bloqueado" : "");
        if (esKernel && ed.abierto) b.classList.add("abierto");
        b.setAttribute("role", "option");
        b.dataset.i = i;

        if (esKernel) {
            if (!ed.abierto) {
                b.insertAdjacentHTML("beforeend",
                    '<svg class="candado" viewBox="0 0 20 20" aria-hidden="true"><rect x="4" y="9" width="12" height="9" rx="1" fill="#cfcfcf"/><path d="M6.5 9V6.5a3.5 3.5 0 0 1 7 0V9" fill="none" stroke="#cfcfcf" stroke-width="1.8"/></svg>');
            }
            const n = document.createElement("span");
            n.className = "nombre"; n.textContent = ed.nombre;
            b.appendChild(n);
        } else {
            b.dataset.estado = ed.estado;
            const partes = [["codigo", ed.codigo], ["nombre", ed.nombre], ["marca", ""], ["flecha", "›"]];
            for (const [cls, txt] of partes) {
                const s = document.createElement("span");
                s.className = cls; s.textContent = txt;
                if (cls === "marca") s.title = TEXTO_ESTADO[ed.estado];
                b.appendChild(s);
            }
        }
        b.addEventListener("click", () => seleccionar(i));
        return b;
    }
    EDIFICIOS.forEach((ed, i) => $("lista").appendChild(crearItem(ed, i, false)));
    $("lista-nucleo").appendChild(crearItem(KERNEL, I_KERNEL, true));

    // ---- Etiquetas fijas sobre el mapa ----
    [...EDIFICIOS, KERNEL].forEach((ed, i) => {
        const c = document.createElement("div");
        c.className = "chip"; c.dataset.i = i; c.textContent = ed.codigo;
        c.style.left = ed.x + "%"; c.style.top = ed.y + "%";
        $("mapa").appendChild(c);
    });

    // ---- Barra de progreso ----
    requestAnimationFrame(() => {
        $("prog-barra").style.width = ($("prog-barra").dataset.valor || 0) + "%";
    });

    // ---- Selección ----
    function seleccionar(i) {
        indice = i;
        const esKernel = i === I_KERNEL;
        const ed = esKernel ? KERNEL : EDIFICIOS[i];
        const estado = esKernel ? (ed.abierto ? "abierto" : "bloqueado") : ed.estado;

        document.querySelectorAll(".item").forEach(el => el.classList.toggle("activo", +el.dataset.i === i));
        document.querySelectorAll(".chip").forEach(c => c.classList.toggle("activo", +c.dataset.i === i));
        for (const id of ["pin", "pulso"]) {
            $(id).style.left = ed.x + "%";
            $(id).style.top = ed.y + "%";
        }

        const vista = $("vista");
        if (ed.imagen) {
            vista.className = "vista";
            vista.style.backgroundImage = `url("${ed.imagen}")`;
            vista.textContent = "";
        } else {
            vista.className = "vista sin-imagen";
            vista.style.backgroundImage = "";
            vista.textContent = "// SEÑAL NO DISPONIBLE";
        }
        void vista.offsetWidth;
        vista.classList.add("cambio");

        $("det-codigo").textContent = esKernel ? "NÚCLEO" : "EDIFICIO " + ed.codigo;
        $("det-nombre").textContent = ed.nombre;
        $("det-desc").textContent = ed.desc;
        $("det-estado").textContent = TEXTO_ESTADO[estado];
        $("det-estado-bloque").dataset.estado = estado;
        $("det-examen").textContent = esKernel
            ? (ed.abierto ? "Batalla final disponible" : "Requiere aprobar todos los exámenes")
            : `${ed.examen} · ${ed.retos}`;

        $("det-villano").textContent = esKernel
            ? ed.villano
            : (ed.villano ? `${ed.villano} (controlado)` : "Señal desconocida");
        $("det-aliado-linea").hidden = !ed.aliado;
        $("det-aliado").textContent = ed.aliado || "";

        const btn = $("btn-entrar");
        btn.classList.toggle("deshabilitado", !ed.url);
        btn.href = ed.url || "#";
        btn.setAttribute("aria-disabled", ed.url ? "false" : "true");
    }

    // ---- Menú de configuración ----
    const menu = $("menu-config");
    const btnConfig = $("btn-config");
    function toggleMenu(abrir) {
        menu.hidden = !abrir;
        btnConfig.setAttribute("aria-expanded", String(abrir));
    }
    btnConfig.addEventListener("click", (e) => { e.stopPropagation(); toggleMenu(menu.hidden); });
    document.addEventListener("click", (e) => { if (!menu.contains(e.target)) toggleMenu(false); });

    // ---- Teclado: ↑/↓ (o W/S) edificios, Enter entra, Esc cierra menú ----
    document.addEventListener("keydown", (e) => {
        const k = e.key.toLowerCase();
        if (k === "arrowdown" || k === "s") { seleccionar((indice + 1) % TOTAL); e.preventDefault(); }
        else if (k === "arrowup" || k === "w") { seleccionar((indice + TOTAL - 1) % TOTAL); e.preventDefault(); }
        else if (k === "enter" && menu.hidden) {
            const b = $("btn-entrar");
            if (!b.classList.contains("deshabilitado")) location.href = b.href;
        }
        else if (k === "escape") toggleMenu(false);
    });

    // ---- Glitch ocasional del logo ----
    setInterval(() => {
        const l = $("logo");
        l.classList.remove("glitch"); void l.offsetWidth; l.classList.add("glitch");
    }, 4500);

    seleccionar(0);
})();