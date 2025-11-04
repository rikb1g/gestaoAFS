function resumoJogo(event, jogoId) {
    event.preventDefault();
    const url = `/jogos/estatistica_jogo/${jogoId}/`;
    
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.text())
        .then(html => {
            document.getElementById("conteudo-dinamico").innerHTML = html;
            history.pushState({ url: url }, "", url);
        })
        .catch(error => console.error("Erro na requisição:", error));


}

function eliminarJogo(event, jogoId) {
    event.preventDefault();
    const url = `/jogos/delete_jogo/${jogoId}/`;
    
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.text())
        .then(html => {
            carregarConteudo(window.urlJogosList);
            history.pushState({ url: window.urlJogosList }, "", window.urlJogosList);
        })
        .catch(error => console.error("Erro na requisição:", error));
}

$(document).on('submit', '#form-new-game', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const url = $(this).attr('data-url');
    console.log("URL:", url);

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())  // ✅ converter para JSON
    .then(data => {
        console.log("Resposta do servidor:", data);

        if (data.success) {
            carregarConteudo(urlJogosList);
            history.pushState({ url: urlJogosList }, "", urlJogosList);
        } else {
            alert(data.message || "Ocorreu um erro ao criar o jogo.");
        }
    })
    .catch(error => console.error("Erro na requisição:", error));
});


$(document).on('submit', '#form-new-team', function (event) {
    event.preventDefault();
    console.log("Form encomendas encontrado");  

    const formData = new FormData(this);
    var url = $(this).attr('data-url');

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
        .then(data => {
            if (data.success) {
                console.log("Resposta do servidor:", data);
                carregarConteudo(urlJogosList);
                history.pushState({ url: urlJogosList }, "", urlJogosList);
            } else {
                alert(data.message || 'Erro ao criar equipa.');
            }
           
            
        })
        .catch(error => console.error("Erro na requisição:", error));
    
});



function alterarEmJogo(event, idAtleta){
    event.preventDefault()
    console.log(idAtleta)
}

function iniciarJogo(event){
    event.preventDefault()
    
    const idsMarcados = Array.from(document.querySelectorAll('input[name="jogadoresEmJogo"]:checked')).map(input => input.value);
    const idJogo = document.querySelector('.atletasSelect')?.dataset.jogo;

    const url = `/jogos/iniciar_jogo/${idJogo}`;
    fetch(url, { 
        headers: { "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': getCSRFToken() },
        method: 'POST',
        body: JSON.stringify({ 
            'atletas': idsMarcados })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Resposta do servidor:", data);
                carregarConteudo('/jogos/estatistica_jogo/'+idJogo);
                
                history.pushState({ url: window.urlJogosList }, "", window.urlJogosList);
                document.getElementById('btn-inicio').classList.add('d-none');
            } else {
                alert(data.message || 'Erro ao iniciar jogo.');
            }
        })
        .catch(error => console.error("Erro na requisição:", error));
        


}


function iniciarCronometro() {
    const timerE1 = document.getElementById('game-timer');
    if (!timerE1) {
        console.warn("⏱️ Cronómetro não encontrado no DOM.");
        return;
    }

    const inicioAttr = timerE1.dataset.inicio;
    if (!inicioAttr) {
        console.warn("⚠️ Sem data de início no cronómetro.");
        return;
    }

    const inicioJogo = new Date(inicioAttr);
    console.log("🕒 Início do jogo:", inicioJogo);

    // Intervalo com revalidação do elemento
    setInterval(() => {
        const timer = document.getElementById('game-timer'); // procurar novamente
        if (!timer) return; // se o conteúdo for recarregado, evita erro

        const agora = new Date();
        const diff = agora - inicioJogo;

        if (diff > 0) {
            const totalSegundos = Math.floor(diff / 1000);
            const minutos = String(Math.floor(totalSegundos / 60)).padStart(2, '0');
            const segundos = String(totalSegundos % 60).padStart(2, '0');
            timer.textContent = `${minutos}:${segundos}`;
        }
    }, 1000);
}

document.addEventListener('DOMContentLoaded', () => {
    iniciarCronometro();
});