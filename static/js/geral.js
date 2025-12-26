/* =====================================
   CSRF
===================================== */
function getCSRFToken() {
    const cookie = document.cookie
        .split(';')
        .map(c => c.trim())
        .find(c => c.startsWith('csrftoken='));

    return cookie ? cookie.split('=')[1] : null;
}

/* =====================================
   MENU
===================================== */


/* =====================================
   PRELOAD
===================================== */
document.body.classList.add('preload');
window.addEventListener('load', () => {
    document.body.classList.remove('preload');
});

/* =====================================
   AJAX CENTRAL
===================================== */
function carregarConteudo(url) {
    return fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
    .then(r => r.text())
    .then(html => {
        const container = document.getElementById("conteudo-dinamico");
        if (!container) return;

        container.innerHTML = html;
        history.pushState({ url }, "", url);
    })
    .catch(err => console.error("Erro AJAX:", err));
}


/* =====================================
   EVENT DELEGATION – LINKS AJAX
===================================== */
document.addEventListener('click', function (e) {
    const link = e.target.closest('.link-ajax, .btn-menu');
    if (!link) return;

    e.preventDefault();
    const url = link.getAttribute('href');
    if (url) carregarConteudo(url);
});

/* =====================================
   THEME (DARK / LIGHT)
===================================== */
document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById("theme-toggle");
    const body = document.body;
    if (!toggleBtn) return;

    const savedTheme = localStorage.getItem("theme");

    if (
        savedTheme === "dark" ||
        (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)
    ) {
        body.classList.add("dark-mode");
        toggleBtn.textContent = "☀️ Claro";
    } else {
        toggleBtn.textContent = "🌙 Escuro";
    }

    toggleBtn.addEventListener("click", () => {
        body.classList.toggle("dark-mode");

        const dark = body.classList.contains("dark-mode");
        toggleBtn.textContent = dark ? "☀️ Claro" : "🌙 Escuro";
        localStorage.setItem("theme", dark ? "dark" : "light");
    });
});

/* =====================================
   HISTORY (BACK / FORWARD)
===================================== */
window.addEventListener('popstate', (event) => {
    if (event.state && event.state.url) {
        carregarConteudo(event.state.url);
    }
});

/* =====================================
   ORQUESTRADOR DE MÓDULOS
===================================== */
document.addEventListener('click', handleActions);
document.addEventListener('dblclick', handleActions);
document.addEventListener('change', handleActions);
document.addEventListener('submit', handleActions);

function handleActions(e) {
    const el = e.target.closest('[data-action]');
    if (!el) return;

    const action = el.dataset.action;

    switch (action) {

        case 'inicar-jogo':
            iniciarJogo(el.dataset.jogo)
            setTimeout(() => {initCronometros();
            }, 1000);
            break;
        case 'intervalo-jogo':
            intervaloJogo(el.dataset.jogo)
            setTimeout(() => {initCronometros();
            }, 1000);
            break
        case 'resumoJogo':
            resumoJogo(el.dataset.jogoid)
            setTimeout(() => {initCronometros();
            }, 1000);
            break
        case 'eliminarJogo':
            eliminarJogo(el.dataset.jogoid)
            break;

        case 'goloEquipa':
            if (e.type === 'dblclick') {
                goloEquipa(el.dataset.jogo, el.dataset.equipaid)
                setTimeout(() => {initCronometros();
            }, 1000);
            }
            break;
            /*golos atleta*/
        case 'golo':
            if (e.type === 'dblclick'){
                golo(el.dataset.atleta, el.dataset.jogo)
                setTimeout(() => {initCronometros();
            }, 1000);
            }
            break;

        case 'novo-jogo':
            initJogosFormNew()

            break;

        case 'alterarEmJogo':
            if (e.type === 'change') {
                alterarEmJogo(el.dataset.atleta, el.dataset.jogo)
            setTimeout(() => {initCronometros();
            }, 2000);
            }

            break;
    }
}

/* =====================================
   BOOTSTRAP INICIAL
===================================== */



  


