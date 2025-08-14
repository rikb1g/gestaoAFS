function carregarConteudo(url) {
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.text())
        .then(html => {
            document.getElementById("conteudo-dinamico").innerHTML = html;
            history.pushState({ url: url }, "", url); // Atualiza a URL do navegador
        })
        .catch(error => console.error("Erro na requisição:", error));
}   


// ====================
// Função para apagar atleta
// ====================
function deleteAtleta(atletaId, nomeAtleta) {
    if (confirm("Tem certeza que deseja apagar o atleta " + nomeAtleta + "?")) {
        fetch('/atletas/delete_atleta/' + atletaId + '/')
            .then(response => response.json())
            .then(data => {
                if (data.success || data.message) { 
                    alert(data.message);
                    // Recarrega a lista de atletas
                    carregarConteudo(window.urlAtletasList);
                } else {
                    alert(data.message || 'Erro ao apagar atleta.');
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert('Erro inesperado.');
            });
    } else {
        alert("Operação cancelada");
    }
}

// ====================
// Delegação de clique para links .ver-atleta
// ====================
document.addEventListener("click", function(e) {
    const link = e.target.closest(".ver-atleta");
    if (!link) return;

    e.preventDefault();  // previne navegação padrão

    const url = link.getAttribute("data-url");
    carregarConteudo(url);

    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.text())
        .then(html => {
            document.getElementById("conteudo-dinamico").innerHTML = html;
        })
        .catch(error => console.error("Erro na requisição:", error));
});

// ====================
// Listener para o form de novo atleta
// ====================
$(document).on('submit', '#form-new-atleta', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    console.log("Form data:", formData);
    const url = $(this).attr('data-url');
    console.log("URL:", url);

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errData => { throw errData });
        }
        return response.json();
    })
    .then(data => {
        console.log("Resposta do servidor:", data);
        if (data.success) {
            alert(data.message);

            carregarConteudo(window.urlAtletasList);
        } else {
            alert("Erro: " + (data.message || 'Erro ao criar atleta.'));
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        if (error.errors) {
            alert("Erros no formulário: " + JSON.stringify(error.errors));
        } else {
            alert('Erro inesperado.');
        }
    });
});

