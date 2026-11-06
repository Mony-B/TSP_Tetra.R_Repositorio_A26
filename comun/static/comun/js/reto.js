// Pantalla de reto (app comun): el contenido ya es interactivo desde que
// carga la página (no hay animación de encendido que bloquee los clics).
// Lo único que hace este script es bajar la pantalla hasta el resultado
// cuando el reto lo muestra.
(function () {
    const resultado = document.getElementById("resultado");
    if (resultado && "MutationObserver" in window) {
        new MutationObserver(() => {
            if (resultado.textContent.trim()) resultado.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }).observe(resultado, { childList: true, subtree: true });
    }
})();
