function carregarConteudo(url) {
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.text())
        .then(html => {
            document.getElementById("conteudo-dinamico").innerHTML = html;
            history.pushState({ url: url }, "", url); // Atualiza a URL do navegador
        })
        .catch(error => console.error("Erro na requisição:", error));
}   

function formatarDataSimples(dataStr) {
  if (!dataStr) return "";
  let [ano, mes, dia] = dataStr.split("-");
  return `${dia}/${mes}/${ano}`;
}

// ====================
// Função para apagar atleta
// ====================
function deleteAtleta(atletaId, nomeAtleta) {
    if (confirm("Tem certeza que deseja apagar o atleta " + nomeAtleta + "?")) {
        fetch('/atletas/delete_atleta/' + atletaId + '/')
            .then(response => response.json())
            .then(data => {
                if (data.success) { 
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
    console.log("aqui");

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




function filterAtletasEscala(ele){
    const escalao = ele.value;
    const url = `/atletas/atletas_list_escalao/?escalao=${escalao}`

    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.json())
        .then(data => {
            if (data) {
                let resultados = data.resultados;
                var tableAtletasBody = $(".table-atletas tbody");
                tableAtletasBody.empty();

                resultados.forEach(item =>{
                    let row = `
                     <tr>
                        <td><a href="/atletas/atleta_detail/${item.id}/"
                         hx-get= "/atletas/atleta_detail/${item.id}/"
                               hx-target="#conteudo-dinamico" hx-push-url="true" class="link-ajax">${item.nome}</a></td>
                        <td>${formatarDataSimples(item.data_nascimento)}</td>
                        <td>${item.numero}</td>
                        <td>${item.nome_camisola ? item.nome_camisola : 'N/A'}</td>
                        <td><input type="checkbox" class="form-check-input" ${item.guarda_redes ? 'checked' : ''} disabled></td>
                        <td class="linha">
                            <a href="/atletas/update_atleta/${item.id}/" hx-push-url="true" class="link-ajax"><span class="material-symbols-outlined btn-operacoes"> edit</span></a>
                            <a href="#" class="link-ajax" onclick="deleteAtleta('${item.id}', '${item.nome}')"><span class="material-symbols-outlined btn-operacoes">delete</span></a>
                        </td>
                    </tr>
                `
                 tableAtletasBody.append(row);
                })
               
                
            }
        })
        .catch(error => console.error("Erro na requisição:", error));    
}


function imprimirCamisolas(event) {
    event.preventDefault()
    const filtro = document.getElementById("escalaoAtleta").value;
    console.log(filtro)
    const url = `/atletas/pdf_camisolas_atletas/?escalao=${filtro}`;
    window.open(url, '_blank');
}


function imprimirAtletas(event) {
    event.preventDefault()
    const filtro = document.getElementById("escalaoAtleta").value;
    console.log(filtro)
    const url = `/atletas/pdf_atletas_escalao_pdf/?escalao=${filtro}`;
    window.open(url, '_blank');
}