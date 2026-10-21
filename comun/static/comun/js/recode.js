// JS compartido (app comun): enviar respuestas a Django y mostrar el resultado.
window.ReCode = {
    csrf() {
        const m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
        return m ? decodeURIComponent(m[1]) : "";
    },

    async postJSON(url, datos = {}) {
        const resp = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": this.csrf() },
            body: JSON.stringify(datos),
        });
        const json = await resp.json();
        if (!resp.ok) throw new Error(json.error || "Error del servidor");
        return json;
    },

    async getJSON(url) {
        const resp = await fetch(url);
        return resp.json();
    },

    // --- Retos ---------------------------------------------------------------
    reto: null,

    configurarReto(config) {
        this.reto = config;
    },

    // Manda la respuesta de un paso. Django revisa y contesta:
    // { correcto, completado, mensaje, bitcoins_otorgados, bitcoins_total }
    async enviarRespuesta(paso, respuesta) {
        const r = await this.postJSON(this.reto.revisarUrl, { paso, respuesta });
        const bitcoins = document.getElementById("bitcoins-alumno");
        if (bitcoins) bitcoins.textContent = r.bitcoins_total;
        this.mostrarResultado(r);
        return r;
    },

    mostrarResultado(r) {
        const caja = document.getElementById("resultado");
        if (!caja) return;
        let html = `<p class="mensaje ${r.correcto ? "" : "error"}">${r.mensaje || (r.correcto ? "Correcto." : "Incorrecto, intenta otra vez.")}</p>`;
        if (r.completado) {
            const extra = r.bitcoins_otorgados ? ` +₿ ${r.bitcoins_otorgados}` : "";
            html = `<p class="mensaje">Reto completado.${extra}</p>` +
                   `<a class="boton" href="${this.reto.volverUrl}">Volver</a>`;
        }
        caja.innerHTML = html;
    },
};
