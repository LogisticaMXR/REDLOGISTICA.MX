document.addEventListener("DOMContentLoaded", () => {
    const menuButton = document.querySelector(".menu-toggle");
    const nav = document.querySelector(".main-nav");

    if (menuButton && nav) {
        menuButton.addEventListener("click", () => {
            const open = nav.classList.toggle("open");
            menuButton.setAttribute("aria-expanded", String(open));
        });
    }

    document.querySelectorAll("[data-tracking-form]").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const result = form.parentElement.querySelector("[data-tracking-result]");
            const input = form.querySelector("input[name='guia']");
            const button = form.querySelector("button[type='submit']");
            const guia = input.value.trim();

            if (!result || !guia) return;

            button.disabled = true;
            button.textContent = "Consultando...";
            result.hidden = false;
            result.innerHTML = "";

            try {
                const response = await fetch(`/api/rastrear?guia=${encodeURIComponent(guia)}`);
                const data = await response.json();

                if (!data.ok) {
                    result.innerHTML = `<div class="error-box">${escapeHtml(data.mensaje)}</div>`;
                    return;
                }

                const envio = data.envio;
                const movimientos = envio.movimientos.map((mov) => `
                    <div class="timeline-item">
                        <div class="time">${escapeHtml(mov.fecha)}</div>
                        <strong>${escapeHtml(mov.titulo)}</strong>
                        <p>${escapeHtml(mov.detalle)}</p>
                    </div>
                `).join("");

                result.innerHTML = `
                    <div class="result-head">
                        <div>
                            <h3>${escapeHtml(envio.estado)}</h3>
                            <div class="result-guide">Guía ${escapeHtml(envio.guia)} · Servicio ${escapeHtml(envio.servicio)}</div>
                        </div>
                        <span class="status ${escapeHtml(envio.estado_clase)}">${escapeHtml(envio.estado)}</span>
                    </div>
                    <div class="route-line">
                        <div class="route-box"><span>Origen</span><strong>${escapeHtml(envio.origen)}</strong></div>
                        <div class="route-arrow">→</div>
                        <div class="route-box"><span>Destino</span><strong>${escapeHtml(envio.destino)}</strong></div>
                    </div>
                    <div class="eta"><strong>Entrega estimada:</strong> ${escapeHtml(envio.entrega_estimada)}<br><span>${escapeHtml(envio.ultimo_movimiento)}</span></div>
                    <div class="timeline">${movimientos}</div>
                `;
            } catch (error) {
                result.innerHTML = `<div class="error-box">No se pudo completar la consulta. Asegúrate de que la aplicación esté ejecutándose con Flask.</div>`;
            } finally {
                button.disabled = false;
                button.textContent = "Consultar";
            }
        });
    });
});

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-quote-form]").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const result = form.parentElement.querySelector("[data-quote-result]");
            const submitButton = form.querySelector("button[type='submit']");
            const peso = form.querySelector("#peso").value;
            const origen = form.querySelector("#origen").value;
            const destino = form.querySelector("#destino").value;

            if (!result) return;

            submitButton.disabled = true;
            submitButton.textContent = "Calculando...";
            result.hidden = false;
            result.innerHTML = "";

            try {
                const response = await fetch("/api/cotizar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ peso, origen, destino })
                });

                const data = await response.json();

                if (!data.ok) {
                    result.innerHTML = `<div class="error-box">${escapeHtml(data.mensaje)}</div>`;
                    return;
                }

                const c = data.cotizacion;
                result.innerHTML = `
                    <div class="quote-result-card">
                        <span class="eyebrow">RESULTADO DE DEMOSTRACIÓN</span>
                        <div class="quote-total">$${Number(c.total).toLocaleString("es-MX")} <small>${escapeHtml(c.moneda)} aprox.</small></div>
                        <p>Esta es una cotización orientativa generada con los datos de la maqueta.</p>
                        <div class="quote-summary">
                            <div><span>Peso</span><strong>${escapeHtml(c.peso)} kg</strong></div>
                            <div><span>Ruta</span><strong>${escapeHtml(c.tipo_ruta)}</strong></div>
                            <div><span>Origen</span><strong>${escapeHtml(c.origen)}</strong></div>
                            <div><span>Destino</span><strong>${escapeHtml(c.destino)}</strong></div>
                            <div><span>Tiempo estimado</span><strong>${escapeHtml(c.tiempo_estimado)}</strong></div>
                            <div><span>Tarifa base</span><strong>$${Number(c.base_peso).toLocaleString("es-MX")} MXN</strong></div>
                        </div>
                    </div>
                `;
            } catch (error) {
                result.innerHTML = `<div class="error-box">No se pudo calcular la cotización. Asegúrate de que la aplicación esté ejecutándose con Flask.</div>`;
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = "Calcular cotización";
            }
        });
    });
});
