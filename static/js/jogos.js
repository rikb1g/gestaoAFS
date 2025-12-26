/**
 *  MÓDULO JOGOS
 */






/*
 * Cronómetros
 */

function initCronometros() {
    const elementos = document.querySelectorAll('[data-inicio]');
    const gameTimer = document.querySelector('#game-timer');
    console.log("elementos",elementos)
    const btnPause = document.querySelector('#btn-pause');
    const btnInicio = document.querySelector('#btn-inicio');




    setInterval(() => {
        elementos.forEach(el => {
            const inicioAttr = el.dataset.inicio;
            if (!inicioAttr) return;

            const inicioTempo = new Date(inicioAttr);
            const agora = new Date();
            const diff = agora - inicioTempo;

            if (diff > 0) {
                const totalSegundos = Math.floor(diff / 1000);
                const minutos = String(Math.floor(totalSegundos / 60)).padStart(2, '0');
                const segundos = String(totalSegundos % 60).padStart(2, '0');
                el.textContent = `${minutos}:${segundos}`;
            }
        });
    }, 1000);
}

/*
EVENT DELEGATION
 */

function initJogosActions(root){
    root.addEventListener('click', function(e){
        const el = e.target.closest('[data-action]');
        if (!el) return;

        const action = el.dataset.action;

        switch (action) {

        }

    })

    /*substituições no jogo*/
    root.addEventListener('change',function (e){
        console.log("alterou")
        const el = e.target.closest('[data-action="alterarEmJogo"]')
        if (!el) return;
        alterarEmJogo(el.dataset.jogo, el.dataset.atleta)

    })


}




/*OPERAÇÔES/*

 */
/*substituições no jogo*/
function alterarEmJogo( idAtleta, jogoId) {
    fetch(window.urlSubstituicaoJogo, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            'atleta': idAtleta,
            'jogo': jogoId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Recarrega a estatística do jogo
            carregarConteudo(`/jogos/estatistica_jogo/${jogoId}/`)
            .then(() => {
                initCronometros();
            });
        } else {
            alert(data.message || 'Erro ao atualizar estado do atleta.');
        }
    })
    .catch(error => console.error('Erro na requisição:', error));
}

/* carregar pagina para correr o jogo */
function resumoJogo(jogoId) {
    const url = `/jogos/estatistica_jogo/${jogoId}/`;

    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.text())
        .then(html => {
            document.getElementById("conteudo-dinamico").innerHTML = html;

            // 🔹 chama os cronometros aqui
            initCronometros();

            // atualiza URL
            history.pushState({ url: url }, "", url);
        })
        .catch(error => console.error("Erro na requisição:", error));
}

/*eliminar jogo*/
function eliminarJogo(jogoId) {
    const url = `/jogos/delete_jogo/${jogoId}/`;

    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.text())
        .then(html => {
            carregarConteudo(window.urlJogosList);
            history.pushState({ url: window.urlJogosList }, "", window.urlJogosList);
        })
        .catch(error => console.error("Erro na requisição:", error));
}

/*iniciar jogo, coloca os cronometros a correr*/
function iniciarJogo(idJogo){
    const idsMarcados = Array.from(
        document.querySelectorAll('input[name="jogadoresEmJogo"]:checked')
    ).map(input => input.value);

    const url = `/jogos/iniciar_jogo/${idJogo}`;

    fetch(url, {
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCSRFToken()
        },
        method: "POST",
        body: JSON.stringify({ atletas: idsMarcados })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Resposta do servidor:", data);
            carregarConteudo('/jogos/estatistica_jogo/'+idJogo+'/')
            history.pushState({ url: '/jogos/estatistica_jogo/'+idJogo + '/' }, "", '/jogos/estatistica_jogo/'+idJogo+'/');

        } else {
            alert(data.message || 'Erro ao iniciar jogo.');
        }
    })
    .catch(error => console.error("Erro na requisição:", error));
}


/*colocar jogo em pausa */
function intervaloJogo(idJogo){
    const idsMarcados = Array.from(
        document.querySelectorAll('input[name="jogadoresEmJogo"]:checked')).map(input => input.value);
    fetch(`/jogos/intervalo_jogo/${idJogo}/`,{
        method: 'POST',
        body: JSON.stringify({
            'atletas': idsMarcados }),
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Resposta do servidor:", data);
            carregarConteudo('/jogos/estatistica_jogo/'+idJogo+'/');

            history.pushState({ url: '/jogos/estatistica_jogo/'+idJogo + '/' }, "", '/jogos/estatistica_jogo/'+idJogo+'/');
        } else {
            alert(data.message || 'Erro ao iniciar jogo.');
        }
    })
    .catch(error => console.error("Erro na requisição:", error));
}


/*GOLOS*/
function goloEquipa(idJogo, equipa){
    console.log(idJogo)
    console.log(equipa)

    fetch(`/jogos/golo_equipa/${idJogo}/${(equipa)}/`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Resposta do servidor:", data);
            carregarConteudo('/jogos/estatistica_jogo/'+idJogo+'/');

            history.pushState({ url: '/jogos/estatistica_jogo/'+idJogo + '/' }, "", '/jogos/estatistica_jogo/'+idJogo+'/');
        } else {
            alert(data.message || 'Erro ao marcar golo');
        }
    })
}
/* adicionar golo ao jogador e a equipa do jogador */
function golo(idAtleta, idJogo){
    console.log(idAtleta)
    console.log(idJogo)



    fetch(`/jogos/golo/${idAtleta}/${idJogo}/`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
    })
    .then(response => response.json())
    .then(data =>{
        if (data.success) {
            console.log("Resposta do servidor:", data);
            carregarConteudo('/jogos/estatistica_jogo/'+idJogo+'/');

            history.pushState({ url: '/jogos/estatistica_jogo/'+idJogo + '/' }, "", '/jogos/estatistica_jogo/'+idJogo+'/');
        } else {
            alert(data.message || 'Erro ao iniciar jogo.');
        }
    })
}


function initJogosFormNew() {
    const visitado = document.querySelector("#id_visitado");
    const visitante = document.querySelector("#id_visitante");
    const titulares = document.querySelector("#id_titulares");
    const suplentes = document.querySelector("#id_suplentes");
    const capitao = document.querySelector("#id_capitao");

    if (!visitado || !visitante || !titulares || !suplentes) return;

    function carregarAtletasSeForAVS(equipaSelect) {
        const selectedOption = equipaSelect.options[equipaSelect.selectedIndex];
        const equipaNome = selectedOption.text;
        const equipaId = equipaSelect.value;

        // Só carrega atletas se a equipa começar por "AVS"

        if ( equipaNome.startsWith("AVS")) {
            titulares.innerHTML = "";
            suplentes.innerHTML = "";
            capitao.innerHTML = "";

            fetch(`/jogos/ajax/atletas-per-jogo/${equipaId}/`)
            .then(response => response.json())
            .then(data => {
                titulares.innerHTML = "";
                suplentes.innerHTML = "";
                capitao.innerHTML = "";

                data.forEach(atleta => {
                    titulares.add(new Option(atleta.nome, atleta.id));
                    suplentes.add(new Option(atleta.nome, atleta.id));
                    capitao.add(new Option(atleta.nome, atleta.id));
                });
            });
            return
        }


    }

    visitado.addEventListener("change", () => carregarAtletasSeForAVS(visitado));
    visitante.addEventListener("change", () => carregarAtletasSeForAVS(visitante));
}



/*

function resumoJogo(event, jogoId) {
    event.preventDefault();
    const url = `/jogos/estatistica_jogo/${jogoId}/`;
    
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.text())
        .then(html => {
            document.getElementById("conteudo-dinamico").innerHTML = html;
            iniciarTodosCronometros();
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
    .then(response => response.json())  
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



function alterarEmJogo(event, idAtleta, jogoId){
    event.preventDefault()
    console.log("Atleta:", idAtleta);
    console.log("Jogo:", jogoId);
    
    fetch(window.urlSubstituicaoJogo,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            'atleta': idAtleta,
            'jogo': jogoId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Resposta do servidor:", data);
            carregarConteudo('/jogos/estatistica_jogo/'+jogoId+'/');
            iniciarTodosCronometros();
            
            history.pushState({ url: '/jogos/estatistica_jogo/'+jogoId + '/' }, "", '/jogos/estatistica_jogo/'+jogoId+'/');
            document.getElementById('btn-inicio').classList.add('d-none');
        } else {
            alert(data.message || 'Erro ao iniciar jogo.');
        }
    })
    .catch(error => console.error("Erro na requisição:", error));

   
}

function iniciarJogo(idJogo){
    const idsMarcados = Array.from(
        document.querySelectorAll('input[name="jogadoresEmJogo"]:checked')
    ).map(input => input.value);

    const url = `/jogos/iniciar_jogo/${idJogo}`;

    fetch(url, {
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCSRFToken()
        },
        method: "POST",
        body: JSON.stringify({ atletas: idsMarcados })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Resposta do servidor:", data);

            iniciarTodosCronometros(); // ✅ AQUI

            history.pushState(
                { url: window.urlJogosList },
                "",
                window.urlJogosList
            );

            document
                .getElementById('btn-inicio')
                .classList.add('d-none');

        } else {
            alert(data.message || 'Erro ao iniciar jogo.');
        }
    })
    .catch(error => console.error("Erro na requisição:", error));
}



function iniciarTodosCronometros() {
    // Seleciona QUALQUER elemento com atributo data-inicio
    const cronometros = document.querySelectorAll('[data-inicio]');

    cronometros.forEach(el => {
        const inicioAttr = el.dataset.inicio;
        if (!inicioAttr) return;

        const inicioTempo = new Date(inicioAttr);

        setInterval(() => {
            const agora = new Date();
            const diff = agora - inicioTempo;

            if (diff > 0) {
                const totalSegundos = Math.floor(diff / 1000);
                const minutos = String(Math.floor(totalSegundos / 60)).padStart(2, '0');
                const segundos = String(totalSegundos % 60).padStart(2, '0');
                el.textContent = `${minutos}:${segundos}`;
            }
        }, 1000);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    setInterval(iniciarTodosCronometros,1000)

});


function intervaloJogo(event,idJogo){
    event.preventDefault()
    const idsMarcados = Array.from(
        document.querySelectorAll('input[name="jogadoresEmJogo"]:checked')).map(input => input.value);
    fetch(`/jogos/intervalo_jogo/${idJogo}/`,{
        method: 'POST',
        body: JSON.stringify({ 
            'atletas': idsMarcados }),
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Resposta do servidor:", data);
            carregarConteudo('/jogos/estatistica_jogo/'+idJogo+'/');
            iniciarTodosCronometros();
            window.location.reload();
            
            history.pushState({ url: '/jogos/estatistica_jogo/'+idJogo + '/' }, "", '/jogos/estatistica_jogo/'+idJogo+'/');
            document.getElementById('btn-inicio').classList.add('d-none');
        } else {
            alert(data.message || 'Erro ao iniciar jogo.');
        }
    })
    .catch(error => console.error("Erro na requisição:", error));
}

function golo(idAtleta, idJogo){
    console.log(idAtleta)
    console.log(idJogo)

    fetch(`/jogos/golo/${idAtleta}/${idJogo}/`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Resposta do servidor:", data);
            carregarConteudo('/jogos/estatistica_jogo/'+idJogo+'/');
            iniciarTodosCronometros();
            window.location.reload();
            
            history.pushState({ url: '/jogos/estatistica_jogo/'+idJogo + '/' }, "", '/jogos/estatistica_jogo/'+idJogo+'/');
            document.getElementById('btn-inicio').classList.add('d-none');
        } else {
            alert(data.message || 'Erro ao iniciar jogo.');
        }
    })
}

function goloEquipa(idJogo, equipa){
    console.log(idJogo)
    console.log(equipa)

    fetch(`/jogos/golo_equipa/${idJogo}/${(equipa)}/`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Resposta do servidor:", data);
            carregarConteudo('/jogos/estatistica_jogo/'+idJogo+'/');
            iniciarTodosCronometros();
            window.location.reload();
            
            history.pushState({ url: '/jogos/estatistica_jogo/'+idJogo + '/' }, "", '/jogos/estatistica_jogo/'+idJogo+'/');
            document.getElementById('btn-inicio').classList.add('d-none');
        } else {
            alert(data.message || 'Erro ao marcar golo');
        }
    })
}


function finalizarJogo(event,jogoId){
    event.preventDefault()
    const idsMarcados = Array.from(
        document.querySelectorAll('input[name="jogadoresEmJogo"]:checked')).map(input => input.value);

    fetch(`/jogos/finalizar_jogo/${jogoId}/`,{
        method: 'POST',
        body: JSON.stringify({ 
            'atletas': idsMarcados }),
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Resposta do servidor:", data);
            carregarConteudo(window.urlJogosList);
            
            
            
            history.pushState({ url: window.urlJogosList }, "", window.urlJogosList);
            document.getElementById('btn-inicio').classList.add('d-none');
        } else {
            alert(data.message || 'Erro ao marcar golo');
        }
    })
}


function initJogosForm() {
    const visitado = document.getElementById("id_visitado");
    const visitante = document.getElementById("id_visitante");
    const titulares = document.getElementById("id_titulares");
    const suplentes = document.getElementById("id_suplentes");
    const capitao = document.getElementById("id_capitao");

    if (!visitado || !visitante || !titulares || !suplentes) return;

    function carregarAtletasSeForAVS(equipaSelect) {
        const selectedOption = equipaSelect.options[equipaSelect.selectedIndex];
        const equipaNome = selectedOption.text;
        const equipaId = equipaSelect.value;

        // Só carrega atletas se a equipa começar por "AVS"
        if ( equipaNome.startsWith("AVS")) {
            titulares.innerHTML = "";
            suplentes.innerHTML = "";
            capitao.innerHTML = "";
            
            fetch(`/jogos/ajax/atletas-per-jogo/${equipaId}/`)
            .then(response => response.json())
            .then(data => {
                titulares.innerHTML = "";
                suplentes.innerHTML = "";
                capitao.innerHTML = "";

                data.forEach(atleta => {
                    titulares.add(new Option(atleta.nome, atleta.id));
                    suplentes.add(new Option(atleta.nome, atleta.id));
                    capitao.add(new Option(atleta.nome, atleta.id));
                });
            });
            return
        }

        
    }

    visitado.addEventListener("change", () => carregarAtletasSeForAVS(visitado));
    visitante.addEventListener("change", () => carregarAtletasSeForAVS(visitante));
}

document.addEventListener("DOMContentLoaded", initJogosForm);
document.addEventListener("htmx:afterSwap", initJogosForm);
*/
